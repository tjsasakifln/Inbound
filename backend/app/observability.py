from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.celery import CeleryInstrumentor

def configure_opentelemetry(app_name: str, app=None, celery_app=None, db_engine=None):
    resource = Resource.create({"service.name": app_name})
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    if app:
        FastAPIInstrumentor.instrument_app(app)
        if db_engine: # Pass engine explicitly for FastAPI
            SQLAlchemyInstrumentor().instrument(engine=db_engine)
        RedisInstrumentor().instrument()
    
    if celery_app:
        CeleryInstrumentor().instrument(tracer_provider=provider, app=celery_app)
        if db_engine: # Pass engine explicitly for Celery
            SQLAlchemyInstrumentor().instrument(engine=db_engine)
        RedisInstrumentor().instrument()