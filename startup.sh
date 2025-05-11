#!/bin/bash
set -euo pipefail

echo "🚀 Starting Dog Breeds API setup..."

# Step 1: Create or confirm .env file
echo "🔧 Checking .env file..."
if [ -f ".env" ]; then
    echo "ℹ️  .env already exists. Overwriting with configured values..."
fi

cat <<EOF > .env
DOG_API_URL=https://api.thedogapi.com/v1
REDIS_HOST=redis
REDIS_PORT=6379
LOG_LEVEL=info
OPENAI_API_KEY=""
EOF

# Step 2: Check and install Poetry
echo "📦 Checking Poetry installation..."
if ! command -v poetry &> /dev/null; then
    echo "📦 Poetry not found. Installing..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
else
    echo "✅ Poetry is already installed."
fi

# Step 3: Install dependencies
echo "📦 Installing Python dependencies with Poetry..."
poetry install

# Step 4: Ensure lock file exists
if [ ! -f "poetry.lock" ]; then
    echo "🔁 Generating poetry.lock..."
    poetry lock
else
    echo "🔒 poetry.lock already exists."
fi

# Step 5: Restart Docker stack
echo "🧼 Cleaning up previous Docker environment..."
docker-compose down -v --remove-orphans

echo "🐳 Rebuilding and launching containers..."
docker-compose up --build -d

# Optional: Tail logs for diagnostics
echo "📡 Tailing Docker logs (Press Ctrl+C to stop)..."
docker-compose logs -f
