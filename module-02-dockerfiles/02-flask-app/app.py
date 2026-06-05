"""
app.py — A Flask web app to Dockerize.

Three endpoints:
  GET  /        → info about this container
  GET  /health  → health check (used by load balancers, Kubernetes)
  POST /echo    → echo back whatever JSON you send
"""
from flask import Flask, jsonify, request
import os
import sys
import platform
import socket

app = Flask(__name__)


@app.route("/")
def index():
    """Root endpoint — returns info about the running environment."""
    return jsonify({
        "message": "🐳 Flask is running inside Docker!",
        "environment": os.getenv("APP_ENV", "development"),
        "container_hostname": socket.gethostname(),  # Docker sets this to the container ID
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
    })


@app.route("/health")
def health():
    """
    Health check endpoint.
    Load balancers and orchestrators (Kubernetes) call this to know if the app is ready.
    Return 200 OK when healthy.
    """
    return jsonify({
        "status": "healthy",
        "service": "flask-docker-demo",
        "version": "1.0.0",
    }), 200


@app.route("/echo", methods=["POST"])
def echo():
    """Echoes back any JSON you POST. Useful for testing."""
    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({"error": "No valid JSON body provided"}), 400
    return jsonify({
        "you_sent": data,
        "received": True,
        "container": socket.gethostname(),
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    # IMPORTANT: host="0.0.0.0" is required in Docker!
    # Without it, Flask only accepts connections from inside the container.
    app.run(host="0.0.0.0", port=port, debug=False)
