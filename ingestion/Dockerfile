FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ingestion_batch.py .
COPY database.py .
COPY models.py .

RUN mkdir -p /app/landing_zone

CMD ["python", "ingestion_batch.py"]