FROM python:3.11-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
RUN useradd -r -u 1001 appuser
USER 1001
EXPOSE 5003
HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
 CMD curl -fsS http://localhost:5003/health || exit 1
CMD ["gunicorn", "--bind", "0.0.0.0:5003", "--workers", "1", "app:app"]
