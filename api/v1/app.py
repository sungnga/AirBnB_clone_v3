#!/usr/bin/python3
"""Status endpoint for API v1"""
from flask import make_response, jsonify, Flask
from os import getenv
import models
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """teardown appcontext"""
    models.storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return json string in case of 404, Not Found"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") or '0.0.0.0'
    port = getenv("HBNB_API_PORT") or 5000
    app.run(host=host, port=port, threaded=True)
