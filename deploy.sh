#!/usr/bin/env bash

set -e

echo "Pulling latest Docker images..."
docker compose pull

echo "Starting Docker Compose services and waiting for health checks..."
#docker compose down -v
docker compose up -d --wait

echo "Docker services are ready."

echo "Starting Python server..."

python3 -m http.server 8000 > server.log 2>&1 &
SERVER_PID=$!

sleep 2

echo "Server started with PID $SERVER_PID"

echo "Creating/updating virtual environment..."
uv sync

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Running Django migrations..."

uv run --env-file=.env python manage.py migrate \
    --settings=config.settings.production

# Start Django server
echo "Starting Django server..."
uv run --env-file=.env python manage.py runserver \
    --settings=config.settings.production
