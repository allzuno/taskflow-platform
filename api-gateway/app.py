from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from datetime import datetime, timezone
import os
import time
import requests

app = Flask(__name__)

TASK_SERVICE_URL = os.getenv('TASK_SERVICE_URL', 'http://task-service:5001')
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://user-service:5002')
NOTIFICATION_SERVICE_URL = os.getenv('NOTIFICATION_SERVICE_URL', 'http://notification-service:5003')

# Real Prometheus metrics. Weekend 9 scrapes these for SLOs -- so the
# label set matters. Never put a task id or user id in a label: that is
# unbounded cardinality and it will take your Prometheus down.
REQUESTS = Counter(
    'http_requests_total', 'Total HTTP requests',
    ['method', 'endpoint', 'status']
)
LATENCY = Histogram(
    'http_request_duration_seconds', 'Request latency',
    ['method', 'endpoint']
)

def now():
    return datetime.now(timezone.utc).isoformat()

@app.before_request
def _start_timer():
    request._start = time.perf_counter()

@app.after_request
def _record(response):
    endpoint = request.url_rule.rule if request.url_rule else 'unmatched'
    REQUESTS.labels(request.method, endpoint, response.status_code).inc()
    LATENCY.labels(request.method, endpoint).observe(
        time.perf_counter() - getattr(request, '_start', time.perf_counter())
    )
    return response

@app.route('/health')
def health():
    return jsonify(status='healthy', service='api-gateway', timestamp=now()), 200

@app.route('/version')
def version():
    return jsonify(version=os.getenv('APP_VERSION', '1.0.0')), 200

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/api/v1/tasks', methods=['GET'])
def get_tasks():
    try:
        r = requests.get(f'{TASK_SERVICE_URL}/tasks', timeout=5)
        return r.json(), r.status_code
    except requests.RequestException as e:
        return jsonify(error=str(e)), 503

@app.route('/api/v1/tasks', methods=['POST'])
def create_task():
    try:
        r = requests.post(f'{TASK_SERVICE_URL}/tasks', json=request.json, timeout=5)
        return r.json(), r.status_code
    except requests.RequestException as e:
        return jsonify(error=str(e)), 503

@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        r = requests.get(f'{USER_SERVICE_URL}/users/{user_id}', timeout=5)
        return r.json(), r.status_code
    except requests.RequestException as e:
        return jsonify(error=str(e)), 503

@app.route('/api/v1/notify', methods=['POST'])
def notify():
    try:
        r = requests.post(f'{NOTIFICATION_SERVICE_URL}/notify', json=request.json, timeout=5)
        return r.json(), r.status_code
    except requests.RequestException as e:
        return jsonify(error=str(e)), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
