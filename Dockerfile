FROM python:3.14-slim AS base

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src/ ./src/
# COPY config.toml ./
RUN uv sync --frozen --no-dev 

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080

CMD ["python", "-m", "main"]
