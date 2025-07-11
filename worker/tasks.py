import redis
import time
import uuid
from celery import Celery
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal, engine, Base
from backend.app import scorer, models
from backend.app.schemas import LeadOut
from backend.app.observability import configure_opentelemetry
from backend.app.metrics import EMAIL_PROCESSING_TOTAL, EMAIL_PROCESSING_LATENCY, LEAD_THROUGHPUT
from backend.app.logging_config import configure_logging, get_logger
import structlog
from fuzzywuzzy import fuzz
import asyncio
from textblob import TextBlob

configure_logging()
logger = get_logger(__name__)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = Celery("inbound", broker="redis://redis:6379/0", backend="redis://redis:6379/0")
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)

# Configure OpenTelemetry for Celery worker
configure_opentelemetry(app_name="worker", celery_app=app, db_engine=engine)

redis_client = redis.Redis(host="redis", port=6379, db=0)
LEAD_UPDATES_CHANNEL = "lead_updates"

@app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 3})
def classify_email(self, email):
    start_time = time.time()
    status = "failed"
    correlation_id = str(uuid.uuid4()) # Generate a new correlation ID for the task
    with structlog.contextvars.bind_contextvars(correlation_id=correlation_id):
        logger.info("Email classification started", email_id=email["email_id"])
        try:
            """
            email = dict(email_id, sender, subject, body)
            """
            db: Session = SessionLocal()
            # Deduplication check with fuzzy matching
            existing_leads = db.query(models.Lead).all()
            is_duplicate = False
            for existing_lead in existing_leads:
                sender_match = fuzz.ratio(email["sender"].lower(), existing_lead.sender.lower())
                subject_match = fuzz.ratio(email["subject"].lower(), existing_lead.subject.lower())
                if sender_match > 80 and subject_match > 70: # Thresholds for fuzzy matching
                    is_duplicate = True
                    break

            if is_duplicate:
                db.close()
                EMAIL_PROCESSING_TOTAL.labels(status='deduplicated').inc()
                logger.info("Email deduplicated (fuzzy match)", email_id=email["email_id"])
                return {"lead_id": existing_lead.id, "status": "deduplicated"}

            score, stage = asyncio.run(scorer.score_email(email["subject"], email["body"])) # Call async function
            
            # Sentiment Analysis and Entity Extraction
            blob = TextBlob(email["body"])
            sentiment = blob.sentiment.polarity # -1 to 1
            entities = {str(word): str(tag) for word, tag in blob.tags if tag.startswith('NN') or tag.startswith('JJ')}

            lead = models.Lead(
                email_id=email["email_id"],
                sender=email["sender"],
                subject=email["subject"],
                body=email["body"],
                score=score,
                stage=stage,
                intent=str(sentiment),
                entities=entities
            )
            db.add(lead)
            db.commit()
            db.refresh(lead)
            
            # Publish update to Redis Pub/Sub
            lead_data = LeadOut.from_orm(lead).json()
            redis_client.publish(LEAD_UPDATES_CHANNEL, lead_data)
            
            db.close()
            status = "success"
            LEAD_THROUGHPUT.labels(stage=stage).inc()
            logger.info("Email classification successful", email_id=email["email_id"], lead_id=lead.id, stage=stage)
            return {"lead_id": lead.id, "status": "processed"}
        except Exception as e:
            logger.error("Email classification failed", email_id=email["email_id"], exc_info=True)
            self.retry(exc=e)
        finally:
            EMAIL_PROCESSING_TOTAL.labels(status=status).inc()
            EMAIL_PROCESSING_LATENCY.labels(status=status).observe(time.time() - start_time)

