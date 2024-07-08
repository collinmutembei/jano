FROM python:3.12-slim

LABEL org.opencontainers.image.title="collinmutembei/jano" \
  org.opencontainers.image.description="Personal journaling API service" \
  org.opencontainers.image.url="ghcr.io/collinmutembei/jano" \
  org.opencontainers.image.source="https://github.com/collinmutembei/jano" \
  org.opencontainers.image.revision="$COMMIT_ID" \
  org.opencontainers.image.version="$PROJECT_VERSION" \
  org.opencontainers.image.authors="Collin Mutembei" \
  org.opencontainers.image.licenses="MIT"

WORKDIR /usr/src/app

ENV PORT 8000

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

COPY ./src ./src

EXPOSE 8000

CMD uvicorn src.main:app --host 0.0.0.0 --port $PORT
