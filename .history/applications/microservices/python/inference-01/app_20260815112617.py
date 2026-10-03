from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify({"service": "inference-01", "status": "ok"})

@app.get("/ready")
def ready():
    return jsonify({"service": "inference-01", "ready": True})

@app.get("/")
def home():
    return jsonify({"service": "inference-01", "message": "Project Nexus Python worker"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
