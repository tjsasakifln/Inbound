# Stage 1: Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY backend/ .
ENV PATH=/root/.local/bin:$PATH
