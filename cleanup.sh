#!/bin/bash

echo "🧹 Cleaning up project for GitHub submission..."

# Remove local environment files and artifacts
rm -rf \
  __pycache__ \
  .pytest_cache \
  .venv \
  .env \
  breeds.pdf \
  pdf/ \
  poetry.lock 

# Clean up Docker containers and image
echo "🐳 Removing Docker containers and volumes..."
docker-compose down -v

echo "🧼 Removing built Docker image (if exists)..."
docker image rm dog-breads-api-api 2>/dev/null || true

echo "✅ Cleanup complete."
