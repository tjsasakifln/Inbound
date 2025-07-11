from prometheus_client import Counter, Histogram, generate_latest

# Define custom metrics
EMAIL_PROCESSING_TOTAL = Counter(
    'email_processing_total', 'Total number of emails processed',
    ['status']
)

EMAIL_PROCESSING_LATENCY = Histogram(
    'email_processing_latency_seconds', 'Latency of email processing',
    ['status']
)

AI_SCORING_LATENCY = Histogram(
    'ai_scoring_latency_seconds', 'Latency of AI scoring',
    ['model']
)

LEAD_THROUGHPUT = Counter(
    'lead_throughput_total', 'Total number of leads created/updated',
    ['stage']
)

def get_metrics():
    return generate_latest()
