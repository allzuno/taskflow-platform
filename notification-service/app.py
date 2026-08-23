from flask import Flask, request, jsonify
from datetime import datetime, timezone
app = Flask(__name__)
notifications = []
@app.route('/health')
def health():
 return jsonify(status='healthy', service='notification-service',
 timestamp=datetime.now(timezone.utc).isoformat()), 200
@app.route('/notify', methods=['POST'])
def send_notification():
 data = request.json or {}
 n = {
 'id': len(notifications) + 1,
 'recipient': data.get('recipient'),
 'message': data.get('message'),
 'type': data.get('type', 'info'),
 'sent_at': datetime.now(timezone.utc).isoformat(),
 'status': 'sent'
 }
 notifications.append(n)
 return jsonify(n), 201
@app.route('/notifications')
def get_notifications():
 return jsonify(count=len(notifications), notifications=notifications), 200
if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5003)
