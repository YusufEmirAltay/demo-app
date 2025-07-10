FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y sqlite3 && \
    pip install -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

COPY app.py .
RUN mkdir /data

VOLUME ["/data"]

CMD ["python", "app.py"]
