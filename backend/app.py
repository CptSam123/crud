# backend/app.py
from flask import Flask
from flask_cors import CORS
from posts.routes import posts_bp

app = Flask(__name__)

# ✅ DO NOT use supports_credentials=True with wildcard origin
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

# ✅ Register API routes
app.register_blueprint(posts_bp, url_prefix='/api/posts')

@app.route('/')
def home():
    return "Backend running..."

if __name__ == '__main__':
    app.run(debug=True, port=3000)
