FROM ghcr.io/astral-sh/uv:0.6.14-python3.10-bookworm

# Set working directory inside the container
WORKDIR /app

# Install additional system dependencies for Python packages like lxml, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    libavif-dev pkg-config \
    libjpeg-dev \
    gcc unzip zip \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set UV cache dir (helps prevent cache permission issues)
ENV UV_HTTP_CACHE_DIR=/tmp/uv-cache

# Copy requirements file
COPY src/requirements.txt .

# Install torch separately due to its size and complexity
RUN uv pip install torch==2.7.0 --system --no-cache-dir

# Install remaining dependencies
RUN uv pip install -r requirements.txt --system --no-cache-dir

# Copy application code
COPY src/ .

# Create directory structure for Alembic (optional: could be handled in code)
RUN mkdir -p /app/models/db_schemas/misrlex/

# Copy alembic.ini config
COPY docker/misrlex/alembic.ini /app/models/db_schemas/misrlex/alembic.ini

# Copy and set executable permissions on the entrypoint script
COPY docker/misrlex/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the container's entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command to start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
