import openai
import os
import json
import time
from backend.app.metrics import AI_SCORING_LATENCY
from aiocache import cached, Cache
from backend.app.database import SessionLocal
from backend.app.models import PromptHistory

class Scorer:
    def __init__(self, model="gpt-4o-mini", temperature=0.0):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.temperature = temperature
        self.prompt = """You are an SDR assistant. 
Classify the following e-mail into Hot (score 0.9), Warm (0.6) or Cold (0.2) 
and output JSON with fields: score and stage ("QUALIFIED" if score
0.6 else "NEW")."""

    @cached(ttl=3600, cache=Cache.REDIS, key_builder=lambda f, *args, **kwargs: f"ai_score:{kwargs.get('subject')}:{kwargs.get('body')}") # Cache for 1 hour
    async def score_email(self, subject: str, body: str) -> tuple[float, str]:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        openai.api_key = self.api_key

        content = f"""Subject: {subject}
Body: {body}"""
        start_time = time.time()
        response_content = ""
        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.prompt},
                    {"role": "user", "content": content}
                ],
                temperature=self.temperature,
                response_format={"type": "json_object"},
            )
            response_content = resp.choices[0].message.content
            data = json.loads(response_content)
            AI_SCORING_LATENCY.labels(model=self.model).observe(time.time() - start_time)
            
            # Persist prompt history
            db = SessionLocal()
            prompt_history = PromptHistory(
                prompt={"prompt": self.prompt + "User Content: " + content},
                response=response_content,
                model_used=self.model
            )
            db.add(prompt_history)
            db.commit()
            db.close()

            return float(data["score"]), data["stage"]
        except Exception as e:
            # In a real app, you'd have more robust error handling and logging
            print(f"Error scoring email: {e}")
            AI_SCORING_LATENCY.labels(model=self.model).observe(time.time() - start_time)
            
            # Persist prompt history even on error
            db = SessionLocal()
            prompt_history = PromptHistory(
                prompt={"prompt": self.prompt + "User Content: " + content},
                response=f"ERROR: {e}",
                model_used=self.model
            )
            db.add(prompt_history)
            db.commit()
            db.close()

            return 0.0, "NEW"

# For compatibility with the old code
async def score_email(subject: str, body: str) -> tuple[float, str]:
    scorer = Scorer()
    return await scorer.score_email(subject, body)
