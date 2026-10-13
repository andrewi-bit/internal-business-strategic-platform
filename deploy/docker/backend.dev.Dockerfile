FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY src/backend/pyproject.toml ./pyproject.toml
COPY src/backend/alembic.ini ./alembic.ini
COPY src/backend/app ./app
COPY src/backend/db_migrations ./db_migrations

RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]