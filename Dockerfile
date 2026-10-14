# Install uv 
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim
WORKDIR /app

# Install locked dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Copy application code

COPY app ./app
COPY alembic.ini ./
COPY alembic/ ./alembic/

# Make the container's virtual environment available
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]