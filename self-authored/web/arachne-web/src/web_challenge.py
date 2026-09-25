#!/usr/bin/env python3
"""
Web Challenge - Flask application with multiple chained vulnerabilities
"""

from flask import Flask, request, jsonify, render_template_string, make_response
import jwt
import os
import base64
import hashlib
import sqlite3

app = Flask(__name__)
app.secret_key = 'arachne_web_secret_2024'
DB_PATH = '/tmp/arachne.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT,
                    is_admin INTEGER DEFAULT 0
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS vault_keys (
                    id INTEGER PRIMARY KEY,
                    key_data TEXT,
                    hint TEXT
                )''')
    
    # Create admin user
    try:
        c.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                  ('admin', 'arachne_admin_pw_hash', 1))
    except:
        pass
    
    # The vault key (fragment3 is embedded here)
    vault_key = base64.b64encode(
        b'FRAGMENT3:4f9c2e87'  # The actual fragment
    ).decode()
    try:
        c.execute("INSERT INTO vault_keys (key_data, hint) VALUES (?, ?)",
                  (vault_key, 'The key is hidden in plain sight'))
    except:
        pass
    
    conn.commit()
    conn.close()

init_db()

# Weak JWT secret (known to players via source code or recon)
JWT_SECRET = 'arachne_jwt_weak_secret'

# Custom JWT encoder/decoder (vulnerable to algorithm confusion)
def create_token(username, is_admin=False):
    payload = {
        'username': username,
        'is_admin': is_admin,
        'alg': 'HS256'
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def decode_token(token):
    # Vulnerable: doesn't validate algorithm properly
    try:
        # First try normal decode
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except:
        try:
            # Then try with none algorithm (vulnerability!)
            payload = jwt.decode(token, JWT_SECRET, algorithms=['none'])
            return payload
        except:
            return None

# Routes
@app.route('/')
def index():
    return '''
    <h1>Arachne Secure Vault</h1>
    <p>Welcome to the Arachne collective's secure vault system.</p>
    <p><a href="/register">Register</a> | <a href="/login">Login</a> | <a href="/admin">Admin Panel</a></p>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, password))
            conn.commit()
            return f"Registered successfully! <a href='/login'>Login</a>"
        except sqlite3.IntegrityError:
            return "Username already exists"
        finally:
            conn.close()
    
    return '''
    <form method="POST">
        <input name="username" placeholder="Username">
        <input name="password" placeholder="Password">
        <button type="submit">Register</button>
    </form>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT is_admin FROM users WHERE username=? AND password=?",
                  (username, password))
        result = c.fetchone()
        conn.close()
        
        if result:
            token = create_token(username, bool(result[0]))
            resp = make_response(f"Login successful! Token: {token}")
            resp.set_cookie('auth_token', token)
            return resp
        else:
            return "Invalid credentials"
    
    return '''
    <form method="POST">
        <input name="username" placeholder="Username">
        <input name="password" placeholder="Password">
        <button type="submit">Login</button>
    </form>
    '''

@app.route('/profile')
def profile():
    token = request.cookies.get('auth_token')
    if not token:
        return "No token provided"
    
    payload = decode_token(token)
    if not payload:
        return "Invalid token"
    
    username = payload.get('username', '')
    
    # SSTI vulnerability - renders user-controlled data as template
    template = f'''
    <h1>Profile: {username}</h1>
    <p>Welcome back, {username}!</p>
    <p>Your account status: Active</p>
    '''
    
    return render_template_string(template)

@app.route('/admin')
def admin():
    token = request.cookies.get('auth_token')
    if not token:
        return "Access denied: No token"
    
    payload = decode_token(token)
    if not payload or not payload.get('is_admin'):
        return "Access denied: Not admin"
    
    return '''
    <h1>Admin Panel</h1>
    <p>Vault Key Fragment: 4f9c2e87</p>
    <p>Hint: The key is stored in the vault_keys table.</p>
    <p><a href="/vault">Access Vault</a></p>
    '''

@app.route('/vault')
def vault():
    token = request.cookies.get('auth_token')
    if not token:
        return "Access denied"
    
    payload = decode_token(token)
    if not payload or not payload.get('is_admin'):
        return "Access denied"
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT key_data FROM vault_keys LIMIT 1")
    result = c.fetchone()
    conn.close()
    
    if result:
        key_data = base64.b64decode(result[0]).decode()
        return f"<pre>{key_data}</pre>"
    return "No vault key found"

@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    """Decrypt endpoint - requires admin and uses the crypto key"""
    token = request.cookies.get('auth_token')
    payload = decode_token(token)
    if not payload or not payload.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    ciphertext = data.get('ciphertext', '')
    
    # The actual decryption would use the master key from crypto stage
    # For the challenge, this just returns a status
    return jsonify({'status': 'decrypted', 'fragment': '4f9c2e87'})

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        filename = request.form.get('filename', '')
        
        if file:
            # Path traversal vulnerability
            save_path = os.path.join('/tmp', filename)
            file.save(save_path)
            return f"File saved to: {save_path}"
    
    return '''
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input name="filename" placeholder="Save as...">
        <button type="submit">Upload</button>
    </form>
    '''

@app.route('/debug')
def debug():
    """Hidden debug endpoint that leaks info"""
    return {
        'env': dict(os.environ),
        'secret': app.secret_key,
        'jwt_secret': JWT_SECRET,
        'db_path': DB_PATH
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
