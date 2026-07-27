FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=src \
    PORT=8000

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md manage.py ./
COPY src ./src
COPY tests ./tests

RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir .

RUN PYTHONPATH=src python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "-c", "PYTHONPATH=src python manage.py migrate && PYTHONPATH=src gunicorn events_site.wsgi:application --bind 0.0.0.0:${PORT}"]
