# backend/app.py
from flask import Flask, request
from flask_cors import CORS
from posts.routes import posts_bp
from auth.routes import auth_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

CORS(app,
     resources={r"/api/*": {"origins": "http://localhost:4200"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# ✅ Respond with 200 OK to preflight OPTIONS requests
@app.before_request
def handle_options_requests():
    if request.method == 'OPTIONS':
        return '', 200

# Blueprints
app.register_blueprint(posts_bp, url_prefix='/api/posts')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

@app.route('/')
def home():
    return "Backend running..."

if __name__ == '__main__':
    app.run(debug=True, port=3000)
