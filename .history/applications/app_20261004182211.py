from flask import Flask, Response, request
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
import os
import time

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "project_nexus_http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "project_nexus_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
)


@app.before_request
def before_request():
    request._project_nexus_request_start_time = time.time()


@app.after_request
def after_request(response):
    duration = (
        time.time() -
        request._project_nexus_request_start_time
    )

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.path,
    ).observe(duration)

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code,
    ).inc()

    return response


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


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST,
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
    )