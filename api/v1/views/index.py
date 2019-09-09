#!/usr/bin/python3
"""Index file for views module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Status route of API v1"""
    d = {"status": "OK"}
    return jsonify(d)


@app_views.route('/stats')
def stats():
    """Stats route of API v1"""
    d = {"amenities": storage.count("Amenity"),
         "cities": storage.count("City"),
         "places": storage.count("Place"),
         "reviews": storage.count("Review"),
         "states": storage.count("State"),
         "users": storage.count("User")}
    return jsonify(d)
