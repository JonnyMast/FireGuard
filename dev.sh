#!/bin/bash

# Step 1: Copy backend .env file if needed
if [ ! -f backend/.env ]; then
  echo "🔧 Creating backend/.env from root .env.example..."
  cp .env.example backend/.env
fi

# Step 2: Start Docker containers
echo "🚀 Starting FireGuard backend and frontend..."
docker compose up --build
