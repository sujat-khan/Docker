"""app.py — Simple Flask API used to demonstrate CI/CD."""
from flask import Flask, jsonify, request
import os
import sys

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({
        "service": "cicd-demo",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "python": sys.version.split()[0],
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/add", methods=["POST"])
def add():
    data = request.get_json(force=True, silent=True) or {}
    a = data.get("a")
    b = data.get("b")
    if a is None or b is None:
        return jsonify({"error": "Provide 'a' and 'b' in JSON body"}), 400
    return jsonify({"result": a + b})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
