import sys
sys.path.append("/app")

import asyncio
import os
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from backend.app.database import Base
from backend.app import scorer, models

# Ensure tables are created
engine = create_engine(os.getenv("DATABASE_URL"))
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def run_demo():
    print("\n--- Starting Functional Demo ---")

    # Exemplo de e-mail de entrada
    email_subject = "Inquiry about your AI Lead Qualifier"
    email_body = "Hello, I am very interested in your AI Lead Qualifier system. Can you provide more details on pricing and integration? We are looking for a solution to streamline our sales process."

    print(f"\nProcessing email:\nSubject: {email_subject}\nBody: {email_body}\n")

    db: Session = SessionLocal()
    try:
        # Score the email
        ai_scorer = scorer.Scorer()
        score, stage = await ai_scorer.score_email(email_subject, email_body)

        # Create a dummy email_id for the demo
        email_id = f"demo_email_{hash(email_subject + email_body)}"

        # Create and save the lead
        lead = models.Lead(
            email_id=email_id,
            sender="demo@example.com",
            subject=email_subject,
            body=email_body,
            score=score,
            stage=stage,
            intent="N/A", # Simplified for demo
            entities={}
        )
        db.add(lead)
        db.commit()
        db.refresh(lead)

        print("\n--- Qualified Lead --- ")
        print(f"ID: {lead.id}")
        print(f"Sender: {lead.sender}")
        print(f"Subject: {lead.subject}")
        print(f"Score: {lead.score}")
        print(f"Stage: {lead.stage}")
        print(f"Created At: {lead.created_at}")

    except Exception as e:
        print(f"Error during demonstration: {e}")
        print("Make sure the OPENAI_API_KEY environment variable is configured in your .env file")
    finally:
        db.close()

if __name__ == "__main__":
    # Set a dummy OPENAI_API_KEY for local testing if not set
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = "sk-dummy-key-for-local-test"
        print("WARNING: OPENAI_API_KEY not found in environment. Using a dummy key. AI scoring will likely fail unless a valid key is provided.")

    asyncio.run(run_demo())