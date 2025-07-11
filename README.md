# AI Lead Qualifier - Automated Lead Qualification System 🚀

[![CI Status](https://github.com/tjsasakifln/Inbound/actions/workflows/ci.yml/badge.svg)](https://github.com/tjsasakifln/Inbound/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/docker-compose-blue.svg)](https://docker.com)

## 🎯 About the System

**AI-powered lead qualification system** that transforms inbound emails into qualified sales opportunities automatically. This solution processes prospect emails, applies intelligent scoring using OpenAI GPT-4, and visualizes qualified leads on a real-time Kanban dashboard.

### 🏆 Key Benefits

- **Complete Automation**: 24/7 inbound email processing
- **Intelligent Scoring**: Precise evaluation using GPT-4o-mini AI
- **Real-time Updates**: Dashboard with instant updates via SSE
- **Scalability**: Robust architecture with Redis and Celery
- **Easy Integration**: Gmail and Microsoft Graph API support
- **Observability**: Metrics with OpenTelemetry and Prometheus

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenAI API Key
- Python 3.9+ (for development)

### Installation

```bash
# Clone the repository
git clone https://github.com/tj-sasaki/Inbound.git
cd Inbound

# Configure environment variables
cp .env.example .env
# Edit .env with your configurations

# Start all services
make up
```

### System Access

- **Frontend**: http://localhost:3000
- **GraphQL API**: http://localhost:8000/graphql
- **API Documentation**: http://localhost:8000/docs
- **Metrics**: http://localhost:9090

## 📊 System Architecture

```mermaid
graph TD
    A[Inbound Email] --> B[Ingestor Service]
    B --> C[Redis Queue]
    C --> D[Celery Worker]
    D --> E[AI Scorer OpenAI]
    E --> F[PostgreSQL DB]
    F --> G[FastAPI Backend]
    G --> H[React Frontend]
    G --> I[GraphQL API]
    G --> J[SSE Real-time]
```

### Core Components

| Component | Technology | Function |
|-----------|------------|----------|
| **Ingestor** | Python, Redis | Email capture and queuing |
| **Worker** | Celery, OpenAI | AI processing and scoring |
| **Backend** | FastAPI, GraphQL | API and business logic |
| **Frontend** | React, Tailwind | User interface |
| **Database** | PostgreSQL | Lead storage |
| **Cache** | Redis | Queues and caching |

## 🤖 Functional Demonstration

Run the demo script to see lead qualification in action:

```bash
# Ensure OPENAI_API_KEY is configured in .env
python demo.py
```

**Expected Output:**

```
--- Starting Functional Demo ---

Processing email:
Subject: Inquiry about your AI Lead Qualifier
Body: Hello, I am very interested in your AI Lead Qualifier system. Can you provide more details on pricing and integration? We are looking for a solution to streamline our sales process.

--- Qualified Lead --- 
ID: abc123-def456-ghi789
Sender: demo@example.com
Subject: Inquiry about your AI Lead Qualifier
Score: 0.9
Stage: QUALIFIED
Created At: 2024-01-15T10:30:00Z
------------------------
```

## 🧪 Testing

Execute the test suite:

```bash
make test
```

## 🛠️ Technology Stack

### Backend Technologies
- **FastAPI**: High-performance API framework
- **Strawberry GraphQL**: Modern GraphQL implementation
- **PostgreSQL**: Reliable database for lead storage
- **Redis**: Message broker and caching layer
- **Celery**: Distributed task queue for background processing
- **OpenTelemetry**: Observability and tracing
- **Prometheus**: Metrics collection and monitoring

### Frontend Technologies
- **React**: Modern UI framework
- **Tailwind CSS**: Utility-first CSS framework
- **React Query**: Data fetching and state management
- **Dnd-kit**: Drag and drop functionality

### AI & Machine Learning
- **OpenAI GPT-4o-mini**: Advanced language model for lead scoring
- **TextBlob**: Natural language processing
- **fuzzywuzzy**: String matching and deduplication

### Infrastructure
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container orchestration
- **GitHub Actions**: CI/CD pipeline

## 📈 Performance Features

- **Rate Limiting**: API protection with `fastapi-limiter`
- **Caching**: Intelligent caching with `aiocache`
- **Deduplication**: Automatic lead deduplication
- **Real-time Updates**: Server-sent events for live dashboard
- **Scalable Architecture**: Horizontal scaling support

## 🔧 Configuration

### Environment Variables

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/leaddb

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Email Integration
GMAIL_CREDENTIALS=path/to/gmail/credentials.json
MSGRAPH_CLIENT_ID=your_msgraph_client_id
MSGRAPH_CLIENT_SECRET=your_msgraph_client_secret
```

## 📊 Monitoring & Observability

The system includes comprehensive monitoring:

- **Health Checks**: Service availability monitoring
- **Performance Metrics**: Response time and throughput
- **Error Tracking**: Detailed error logging and alerting
- **AI Model Metrics**: Scoring accuracy and confidence levels

## 🚀 Production Deployment

For production deployment:

1. **Environment Setup**: Configure production environment variables
2. **Database Migration**: Run database migrations
3. **SSL Configuration**: Setup HTTPS certificates
4. **Load Balancing**: Configure reverse proxy
5. **Monitoring**: Setup alerting and log aggregation

## 📧 Contact & Support

**Ready to transform your lead management process?**

This repository demonstrates a complete, production-ready lead qualification system. Explore the code, review the architecture, and discover the impact on your sales operations.

- **Email**: [tiago.sasaki@gmail.com](mailto:tiago.sasaki@gmail.com)
- **Demo Request**: Contact us for a personalized demonstration
- **Custom Solutions**: Discuss adaptation to your specific needs

---

*Transform inbound emails into qualified opportunities with AI-powered automation.*