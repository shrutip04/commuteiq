"""
app.py — Flask entry point for CommuteIQ.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

from database import init_db
from routes import api

app = Flask(__name__)
app.secret_key = "commuteiq-flask-secret-2024"

# CORS — allow all origins
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Handle ALL OPTIONS preflight requests globally — before any auth/parsing
@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers["Access-Control-Allow-Origin"]  = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response, 200

# Add CORS headers to every response
@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

app.register_blueprint(api, url_prefix="/api")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "CommuteIQ API v1.0"})

if __name__ == "__main__":
    print("=" * 50)
    print("  CommuteIQ Backend Starting...")
    print("  http://localhost:5000")
    print("=" * 50)
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)