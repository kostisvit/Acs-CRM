#!/usr/bin/env bash

set -e

echo "Starting Python server..."

# Start server in background
python3 -m http.server 8000 > server.log 2>&1 &
SERVER_PID=$!

# Give the server a moment to start
sleep 2

echo "Server started with PID $SERVER_PID"

# Create or update virtual environment
echo "Creating/updating virtual environment..."
uv sync

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Start Django server
echo "Starting Django server..."
uv run --env-file=.env python manage.py runserver \
    --settings=config.settings.production

# Example shell commands
echo "Running additional commands..."
mkdir -p output
cp input.txt output/

echo "Done."

