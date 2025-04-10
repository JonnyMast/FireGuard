FROM python:3.13-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y curl build-essential

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copy backend code
COPY pyproject.toml poetry.lock README.md ./
COPY App ./App
COPY run.py .

# Install dependencies
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

CMD ["poetry", "run", "python", "run.py"]
