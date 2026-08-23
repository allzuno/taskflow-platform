FROM python:3.11-slim
# curl is required by HEALTHCHECK and by the compose healthcheck.
# python:3.11-slim does NOT ship it -- without this line every
# healthcheck exits 127 and the container is marked unhealthy forever.
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
# Non-root: kubelet does not enforce this for you, the image must do it
RUN useradd -r -u 1001 appuser
USER 1001
EXPOSE 5000
HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
 CMD curl -fsS http://localhost:5000/health || exit 1
# 2 workers, not 4. On a 4 GiB node, 4 gunicorn workers x 2 replicas
# is roughly 800 MiB of Python interpreters doing nothing.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "30", "app:app"]
