# 🐶 Dog Breeds API – FastAPI Integration

A RESTful API built with **FastAPI**, integrating [The Dog API](https://thedogapi.com), and offering:

- ✅ Lifespan filtering
- ✅ Alphabetical listing
- ✅ PDF export of breed data

---

## What startup.sh Does:

This script bootstraps the entire development and deployment environment in one command.
🔹 Step-by-step explanation:

    Creates a .env file
    Injects required environment variables automatically so no manual config is needed:

DOG_API_URL=https://api.thedogapi.com/v1
REDIS_HOST=redis
REDIS_PORT=6379
LOG_LEVEL=info

Checks if Poetry is installed

    If not, installs it using the official installer

    Ensures the Poetry binary is added to the system PATH

Generates poetry.lock (if missing)

    Ensures all dependency versions are pinned and reproducible

Tears down any running Docker containers

    Fully cleans up volumes and previous images using docker-compose down -v

Builds and runs Docker containers

    Rebuilds the FastAPI and Redis containers using docker-compose up --build

    Launches the app ready to serve requests at:
    http://localhost:8000

## 🔧 Quick Start

```bash
git clone https://github.com/xdetrouk/dog-breeds-api.git
cd dog-breeds-api
chmod +x startup.sh
./startup.sh
'''

