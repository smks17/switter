# Switter

Switter is a simple **RESTful social network project** built with **Django** and designed with a **microservices-friendly architecture**. The project uses **Apache Kafka** for asynchronous communication between services and is fully runnable using **Docker Compose**.

---

## Features

* REST APIs built with **Django** and **Django REST Framework**
* Microservice-style separation (posts, feed, interactions, etc.)
* **Apache Kafka** for event-driven communication
* **PostgreSQL** as the main database
* Fully containerized with **Docker & Docker Compose**
* Easy local development setup

---

## Requirements

* Python3.12
* Go
* Postgres
* Redis
* Kafka

---

## Running the Project (Docker – Recommended)

### Clone the Repository

```bash
git clone https://github.com/smks17/switter.git
cd switter
```

### Environment Variables

Create a `.env` file based on `.env.example`

For example:

```env
SECRET_KEY=your_secret_key
DEBUG=1
POSTGRES_DB=switter
POSTGRES_USER=switter_user
POSTGRES_PASSWORD=switter_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
```

---

### Build & Run with Docker Compose

```bash
docker compose up --build
```

The API will be available at:

```
http://localhost:8000
```

---

## Database & Migrations

Migrations are automatically applied on container startup. If you need to run them manually:

```bash
docker exec -it switter_app python manage.py migrate
```

To seed the database with sample data:

```bash
docker exec -it switter_app python seed_db.py
```

---

## Kafka Architecture

Kafka is used for **event-driven communication** between services.

Examples of events:

* User created
* Post published
* Post liked or commented

Topics was defined in `kafka-init/`

---

## Services Overview

| Service      | Description                 |
| ------------ | --------------------------- |
| switter      | Main Django API             |
| users        | User management             |
| posts        | Post creation and retrieval |
| feed-service | User feed generation        |
| interactions | Likes and comments          |
| kafka        | Event streaming             |
| db           | PostgreSQL database         |

---

## Development Without Docker

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Kafka and PostgreSQL must be running separately in this mode.

---

## Example API Endpoints

| Endpoint                                     | Method     | Description          |
| -------------------------------------------- | ---------- | -------------------- |
| `/api/users/`                                | GET / POST | List or create users |
| `/api/social/posts/`                         | GET / POST | List or create posts |
| `/api/social/feed/`                          | GET        | User feed            |
| `/api/social/posts/<post_id>/<like|comment>` | POST       | Like or comment      |

---

## TODO:

- [ ] Better error handling
- [ ] Using better context in feed-service
- [ ] More API for user profile and settings
- [ ] Complicated feed explore
- [ ] Using celery or Kafka for background task
- [ ] Using socket with feed-service
- [ ] Github CI/CD
- [ ] Using Kubernetes

