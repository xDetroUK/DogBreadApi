# Dog Breeds API

This is the full technical documentation for the Dog Breeds API project.

---

## Overview

This RESTful API provides:

- 🔍 **Breed filtering by lifespan**
- 🔤 **Alphabetical listing**
- 📝 **PDF export of full breed data**

---

## Setup

- Clone the repo and run `./startup.sh`
- The app runs on: `http://localhost:8000`
- Swagger docs: `/docs`
- ReDoc: `/redoc`

---

## Configuration

Environment variables in `.env`:

```
DOG_API_URL=https://api.thedogapi.com/v1
REDIS_HOST=redis
REDIS_PORT=6379
LOG_LEVEL=info
```

---

## Tech Stack

- Python 3.11
- FastAPI
- Poetry
- Docker + Docker Compose
- Redis (optional extension)
- WeasyPrint for PDF generation
