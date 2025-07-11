# Architectural and Stack Decisions

This document outlines the key architectural and technology stack decisions made during the development of the Inbound AI Lead Qualifier Proof of Concept (POC), along with the rationale behind each choice.

## 1. Overall Architecture: Microservices with Asynchronous Processing

**Decision:** The system is designed as a microservices-oriented architecture, with distinct services for backend API, asynchronous worker tasks, and email ingestion. Asynchronous processing is heavily utilized for email qualification.

**Rationale:**
*   **Scalability:** Allows individual components to scale independently based on their load (e.g., more workers for email processing without affecting the API).
*   **Resilience:** Failure in one service (e.g., AI scoring) does not bring down the entire system. Retries and message queues ensure robustness.
*   **Maintainability:** Smaller, focused services are easier to develop, test, and deploy.
*   **Decoupling:** Services communicate via well-defined interfaces (API, message queues), reducing interdependencies.

## 2. Backend Framework: FastAPI (Python)

**Decision:** FastAPI was chosen for the main backend API.

**Rationale:**
*   **High Performance:** Built on Starlette and Pydantic, it offers performance comparable to Node.js and Go.
*   **Developer Experience:** Excellent documentation, automatic OpenAPI (Swagger UI) generation, and type hints for better code quality and autocompletion.
*   **Asynchronous Support:** Native `async/await` support, crucial for non-blocking I/O operations like database calls and external API integrations.
*   **Python Ecosystem:** Access to a rich ecosystem of libraries for AI/ML, data processing, and other utilities.

## 3. Asynchronous Task Queue: Celery with Redis Broker

**Decision:** Celery is used for managing background tasks, with Redis serving as both the message broker and result backend.

**Rationale:**
*   **Reliability:** Ensures that email processing tasks are executed reliably, even if the worker service temporarily goes down (tasks are queued).
*   **Scalability:** Easily allows adding more worker instances to handle increased email processing load.
*   **Decoupling:** Separates the immediate API response from long-running tasks like AI scoring and database persistence.
*   **Redis Efficiency:** Redis is a fast, in-memory data store, making it an efficient choice for a message broker.

## 4. Database: PostgreSQL

**Decision:** PostgreSQL is used as the primary relational database.

**Rationale:**
*   **Robustness & Reliability:** A mature, ACID-compliant relational database known for its data integrity and reliability.
*   **Feature Rich:** Supports advanced features like JSONB for flexible schema, full-text search, and strong indexing capabilities.
*   **Community & Ecosystem:** Large, active community and extensive tooling support.
*   **Scalability:** Can be scaled vertically and horizontally with appropriate strategies.

## 5. Caching: Redis with aiocache

**Decision:** Redis is utilized for caching frequently accessed data, integrated via `aiocache`.

**Rationale:**
*   **Performance:** Reduces database load and improves API response times by serving data from fast in-memory cache.
*   **Versatility:** Redis can be used for various caching patterns (e.g., full-page, object, query results).
*   **Asynchronous Support:** `aiocache` provides seamless asynchronous caching integration with FastAPI.

## 6. Frontend Framework: React with Tailwind CSS

**Decision:** React is used for the frontend, styled with Tailwind CSS.

**Rationale:**
*   **Component-Based:** React's component-based architecture promotes reusability and maintainability.
*   **Rich Ecosystem:** Large community, extensive libraries, and development tools.
*   **Tailwind CSS:** A utility-first CSS framework that enables rapid UI development and consistent design without writing custom CSS.
*   **Interactive UI:** Ideal for building dynamic and real-time user interfaces like the Kanban board.

## 7. AI Model Integration: OpenAI GPT-4o-mini (with fine-tuning option)

**Decision:** Initially integrates with OpenAI's GPT-4o-mini for AI scoring, with a clear path for fine-tuning open-source models.

**Rationale:**
*   **Rapid Prototyping:** Leverages a powerful, pre-trained model for quick demonstration of AI capabilities.
*   **Cost-Effectiveness:** GPT-4o-mini offers a good balance of performance and cost for a POC.
*   **Flexibility:** The architecture allows for easy swapping or fine-tuning of AI models (e.g., using QLoRA for open-source models) to optimize for cost or specific domain needs in a production environment.

## 8. Containerization: Docker and Docker Compose

**Decision:** All services are containerized using Docker, orchestrated with Docker Compose for local development.

**Rationale:**
*   **Environment Consistency:** Ensures that the development, testing, and production environments are identical, eliminating "it works on my machine" issues.
*   **Isolation:** Each service runs in its own isolated container, preventing dependency conflicts.
*   **Ease of Deployment:** Simplifies the setup and deployment process, especially for multi-service applications.
*   **Portability:** The entire application stack can be easily moved and run on any Docker-compatible host.

## 9. Observability: OpenTelemetry, Prometheus, Structured Logging

**Decision:** Implemented distributed tracing with OpenTelemetry, custom metrics with Prometheus, and structured logging with correlation IDs.

**Rationale:**
*   **Troubleshooting:** Provides deep insights into application behavior, making it easier to identify and diagnose issues across services.
*   **Performance Monitoring:** Metrics help track key performance indicators (KPIs) and identify bottlenecks.
*   **Root Cause Analysis:** Tracing allows following requests across service boundaries, crucial in a microservices architecture.
*   **Proactive Alerting:** Enables setting up alerts for anomalies or critical failures.

## 10. Security: JWT, OAuth2, Rate Limiting

**Decision:** Incorporated JWT for authentication, OAuth2 for external identity providers (Google), and rate limiting.

**Rationale:**
*   **Authentication & Authorization:** Securely verifies user identities and controls access to resources.
*   **External Identity:** OAuth2 simplifies user login and leverages trusted identity providers.
*   **DDoS Protection:** Rate limiting protects against abuse and denial-of-service attacks.
*   **Best Practices:** Adheres to common security best practices for web applications.

## 11. CI/CD: GitHub Actions

**Decision:** GitHub Actions is used for the Continuous Integration pipeline.

**Rationale:**
*   **Automation:** Automates the build, test, and linting processes on every push and pull request.
*   **Integration:** Native integration with GitHub repositories.
*   **Consistency:** Ensures code quality and prevents regressions by running checks automatically.
*   **Visibility:** Provides immediate feedback on the health of the codebase through status badges.
