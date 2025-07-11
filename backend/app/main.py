import asyncio
import redis.asyncio as redis
from datetime import timedelta
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse, Response, RedirectResponse
from strawberry.asgi import GraphQL
from .graphql import schema
from . import auth
from .observability import configure_opentelemetry
from .database import engine
from .metrics import get_metrics
from .logging_config import configure_logging, get_logger
from .oauth2 import get_google_flow
import uuid
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from aiocache import caches
import structlog

configure_logging()
logger = get_logger(__name__)

app = FastAPI(title="Inbound AI Lead Qualifier")

# Configure OpenTelemetry
configure_opentelemetry(app_name="backend", app=app, db_engine=engine)

LEAD_UPDATES_CHANNEL = "lead_updates"

@app.on_event("startup")
async def startup():
    redis_connection = redis.from_url("redis://redis:6379/0", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_connection)
    
    caches.set_config({
        "default": {
            "cache": "aiocache.backends.redis.RedisCache",
            "endpoint": "redis",
            "port": 6379,
            "timeout": 1,
            "serializer": {
                "class": "aiocache.serializers.JsonSerializer"
            }
        }
    })

@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(correlation_id=correlation_id)
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response

@app.post("/token", dependencies=[Depends(RateLimiter(times=5, seconds=60))]) # 5 requests per minute
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # In a real app, you'd verify the user against a DB
    # This is a dummy check
    if form_data.username != "test" or not auth.verify_password(form_data.password, auth.get_password_hash("test")):
        logger.warning("Login failed", username=form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    logger.info("Login successful", username=form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/google")
async def google_auth():
    flow = get_google_flow()
    authorization_url, state = flow.authorization_url(access_type="offline", include_granted_scopes="true")
    return RedirectResponse(authorization_url)

@app.get("/auth/google/callback")
async def google_callback(request: Request, code: str):
    flow = get_google_flow()
    flow.fetch_token(code=code)
    credentials = flow.credentials
    # In a real app, save refresh_token to DB associated with user
    # For now, just return access token
    access_token_expires = timedelta(seconds=credentials.expires_in)
    access_token = auth.create_access_token(
        data={"sub": credentials.id_token["email"]}, expires_delta=access_token_expires
    )
    logger.info("Google OAuth successful", email=credentials.id_token["email"])
    return {"access_token": access_token, "token_type": "bearer"}

async def event_stream(request: Request):
    r = redis.Redis(host="redis", port=6379, db=0)
    pubsub = r.pubsub()
    await pubsub.subscribe(LEAD_UPDATES_CHANNEL)
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=10)
            if message:
                yield f"data: {message['data'].decode('utf-8')}\n\n"
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        logger.info("SSE client disconnected")
        await pubsub.unsubscribe(LEAD_UPDATES_CHANNEL)
        raise

@app.get("/sse/leads", dependencies=[Depends(RateLimiter(times=100, seconds=60))]) # 100 requests per minute
async def sse_leads(request: Request, current_user: dict = Depends(auth.get_current_user)):
    return StreamingResponse(event_stream(request), media_type="text/event-stream")

@app.get("/metrics")
async def metrics():
    return Response(content=get_metrics(), media_type="text/plain")

graphql_app = GraphQL(schema)

app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
