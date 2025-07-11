"""
Puxa e-mails não lidos via Gmail ou Microsoft Graph,
publica cada mensagem na fila Celery para pontuação.
"""

import os, base64, json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from kombu import Connection, Exchange, Queue

CELERY_BROKER = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
exchange = Exchange("leads", type="direct")
queue    = Queue("raw_emails", exchange, routing_key="raw")

def fetch_gmail():
        # In a production environment, consider a more secure way to handle credentials,
    # such as OAuth 2.0 flows without storing token.json directly in the filesystem.
    # For this POC, we'll assume credentials are handled externally or via environment variables.
    # creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/gmail.readonly"])
    # Placeholder for demonstration purposes:
    raise NotImplementedError("Gmail authentication needs to be implemented securely. token.json removed for security.")
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    for msg in results.get("messages", []):
        data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = base64.urlsafe_b64decode(data['payload']['body']['data']).decode()
        with Connection(CELERY_BROKER) as conn:
            producer = conn.Producer(serializer='json')
            producer.publish({
                "email_id": msg['id'],
                "sender": next(h['value'] for h in data['payload']['headers'] if h['name']=="From"),
                "subject": data['snippet'],
                "body": payload
            }, exchange=exchange, routing_key="raw")
