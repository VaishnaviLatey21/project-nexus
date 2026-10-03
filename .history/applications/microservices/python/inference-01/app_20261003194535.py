from flask import Flask
import os

app = Flask(__name__)


@app.get("/")
def hello():
    return {
        "application": "project-nexus",
        "service": "python-service",
        "version": os.getenv("APP_VERSION", "dev"),
        "message": "Hello from Project Nexus!"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)