# Use the official Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set the working directory
WORKDIR /app

# Set environment variables
ENV UV_SYSTEM_PYTHON=1
ENV PATH="/root/.local/bin:$PATH"

# Copy the rest of the application code
COPY . .

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install -r requirements.txt

# Ensure container will run when prefect worker start is called from docker compose
RUN prefect --version