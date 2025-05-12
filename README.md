# Dog Breeds API

RESTful API developed with FastAPI that integrates with [TheDogAPI](https://thedogapi.com) to provide data about dog breeds. 
API includes lifespan filtering, alphabetical listing, PDF export, AI-driven breed matching, and vision-based breed analysis.

---

## Core Features

| Feature                        | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| `/breeds/lifespan`            | Filter breeds by minimum and maximum lifespan                              |
| `/breeds/alphabetical`        | Return all breed names in alphabetical order                               |
| `/breeds/export/pdf`          | Export complete breed data as a downloadable, formatted PDF                |
| `/breeds/match`               | Get best dog breed match based on user preference via GPT-4.1              |
| `/breeds/analyze-image`       | Send image URL to analyze the breed using GPT-4.1 vision model             |
| `/health`                     | Lightweight health check endpoint                                          |

---

## Architecture

```
src/
├── api/               # FastAPI routers
├── config/            # Environment configuration using pydantic-settings
├── models/            # Pydantic models used for input/output
├── repositories/      # Dog API integration + Redis caching logic
├── services/          # Logic layer (lifespan, alphabetical, PDF, etc.)
├── utils/             # Logging setup, PDF export, AI tools (OpenAI GPT, vision)
└── main.py            # FastAPI entrypoint
```

---

## Environment Configuration

`.env` file example:

```env
DOG_API_URL=https://api.thedogapi.com/v1
REDIS_HOST=redis
REDIS_PORT=6379
LOG_LEVEL=info
OPENAI_API_KEY=sk-...
```

These are injected using `pydantic-settings` for typed config management.

---

## System Requirements

- Python 3.11+
- Docker + Docker Compose
- Redis (for caching)
- Poetry (dependency management)

---

## Docker Setup

```bash
docker-compose up --build
```

This will:
- Start the FastAPI app on port `8000`
- Launch a Redis container for breed data caching

---

## Development & Testing

### Local Run

```bash
poetry install
./startup.sh
```

### Run Tests

```bash
poetry run pytest
```

Includes:
- Unit and async tests (`pytest`, `pytest-asyncio`)
- Formatting enforced with `black`
- Linting via `flake8`

---

## PDF Export Layout

- Alphabetically sorted breed data
- Paginated output with breed attributes:
  - Name
  - Life Span
  - Bred For
  - Breed Group
  - Temperament

Generated via `reportlab` and delivered as streaming FastAPI response.

---

## AI Integrations (OpenAI)

### Match Breed (`/breeds/match`)

Uses GPT-4.1 to match dog breeds based on user preference (e.g., temperament, energy level).

### Image Analysis (`/breeds/analyze-image`)

Uses GPT-4.1 vision model to describe or identify breed from a provided image URL.

---

## Observability

Structured logging is powered by `structlog`, exporting JSON logs with timestamps, levels, and contexts:

```json
{
  "event": "Filtered breeds by lifespan",
  "count": 12,
  "timestamp": "2025-05-11T11:15:23.123Z",
  "level": "info"
}
```

---

## Documentation

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- MkDocs for static site: run `mkdocs serve`
  MANUAL:
  curl http://localhost:8000/health

  curl http://localhost:8000/breeds/alphabetical

  curl -X GET /breeds/lifespan?min_years=10&max_years=15

  curl -X GET http://localhost:8000/breeds/export/pdf --output breeds.pdf

  curl -X POST http://localhost:8000/breeds/analyze-image   -F "image_url=https://cdn.pixabay.com/photo/2016/12/13/05/15/puppy-1903313_640.jpg"

  curl -X POST http://localhost:8000/breeds/match \
  -H "Content-Type: application/json" \
  -d '{"preferences": "active lifestyle, good with kids, low shedding"}'


---

## Dependencies (from `pyproject.toml`)

| Package           | Purpose                        |
|-------------------|--------------------------------|
| fastapi           | API framework                  |
| httpx             | Async HTTP client              |
| redis             | Redis support via asyncio      |
| structlog         | Structured logging             |
| openai            | GPT-4 text + vision models     |
| reportlab         | PDF generation                 |
| pydantic-settings | Env var configuration          |
| uvicorn           | ASGI server                    |

---



---
