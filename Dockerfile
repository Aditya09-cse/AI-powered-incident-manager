FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY app/ .

RUN useradd -m appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "--timeout", "180", "app:app"]
