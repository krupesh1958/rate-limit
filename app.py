#!/usr/bin/env python3
"""Initialization flask application."""
from typing import Dict
from flask import Flask
from middleware import server, rate_limit, bucket

from api.views import bp as api_bp
JsonType = Dict[str, int]

app = Flask (__name__)
app.wsgi_app = bucket.RateLimit(app.wsgi_app)

app.register_blueprint(api_bp, url_prefix="/api/v1")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7861, debug=True)
