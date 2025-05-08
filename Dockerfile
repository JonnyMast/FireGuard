FROM python:3.13-slim

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y curl build-essential

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Install Python dependencies using Poetry
COPY pyproject.toml poetry.lock README.md ./
COPY src ./src
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

# Copy the rest of your project files
COPY . .

# Expose the app port
EXPOSE 8000

# Start the FastAPI app with uvicorn
CMD ["uvicorn", "fireguard2.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
