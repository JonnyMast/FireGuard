#!/bin/bash

# Step 1: Copy .env.example to .env if it doesn't already exist
if [ ! -f .env ]; then
  echo "Creating .env from .env.example..."
  cp .env.example .env
fi

# Step 2: Build and start the Docker container
echo "Starting FireGuard dev environment..."
docker compose up --build
