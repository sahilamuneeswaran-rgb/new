from flask import Flask, render_template, request, jsonify
from functools import wraps
import uuid

app = Flask(__name__)
app.secret_key = 'replace-this-secret-key'

users = []
tokens = {}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token not in tokens:
            return jsonify({'error': 'Missing or invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register')
def reg():
    return render_template('register.html')

@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not name or not email or not password:
        return jsonify({'error': 'All fields required'}), 400
    for u in users:
        if u['email'] == email:
            return jsonify({'error': 'Email exists'}), 400
    uid = str(uuid.uuid4())
    user = {'id': uid, 'name': name, 'email': email, 'password': password}
    users.append(user)
    return jsonify({'message': 'Registered', 'user_id': uid}), 201

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    for u in users:
        if u['email'] == email and u['password'] == password:
            token = f'token-{u["id"]}-{uuid.uuid4()}'
            tokens[token] = u['id']
            return jsonify({'token': token, 'user': {'id': u['id'], 'name': u['name'], 'email': u['email']}})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/users', methods=['GET'])
@token_required
def api_users():
    return jsonify({'users': [{k:v for k,v in u.items() if k!='password'} for u in users]})

@app.route('/api/users/<uid>', methods=['PUT'])
@token_required
def api_user_update(uid):
    data = request.get_json()
    for u in users:
        if u['id'] == uid:
            u['name'] = data.get('name', u['name'])
            u['email'] = data.get('email', u['email'])
            return jsonify({'message': 'Updated', 'user': u})
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/users/<uid>', methods=['DELETE'])
@token_required
def api_user_delete(uid):
    global users
    users = [u for u in users if u['id'] != uid]
    return jsonify({'message': 'Deleted'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
