from flask import Flask, jsonify
from datetime import datetime, timezone
app = Flask(__name__)
users = {
 '1': {'id': '1', 'name': 'Alice DevOps', 'email': 'alice@example.com',
 'role': 'DevOps Engineer', 'created_at': '2024-01-15'},
 '2': {'id': '2', 'name': 'Bob SRE', 'email': 'bob@example.com',
 'role': 'SRE', 'created_at': '2024-01-20'}
}
@app.route('/health')
def health():
 return jsonify(status='healthy', service='user-service',
 timestamp=datetime.now(timezone.utc).isoformat()), 200
@app.route('/users/<user_id>')
def get_user(user_id):
 user = users.get(user_id)
 return (jsonify(user), 200) if user else (jsonify(error='User not found'), 404)
@app.route('/users')
def list_users():
 return jsonify(count=len(users), users=list(users.values())), 200
if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5002)
