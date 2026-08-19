FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
COPY apps/api/src ./apps/api/src
COPY fixtures ./fixtures

RUN pip install --no-cache-dir .

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/apps/api/src

EXPOSE 8000

CMD ["uvicorn", "threatatlas.main:app", "--host", "0.0.0.0", "--port", "8000"]
