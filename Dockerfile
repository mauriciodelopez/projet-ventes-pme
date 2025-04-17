# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY scripts/ ./scripts/

CMD ["python", "./scripts/main.py"]
