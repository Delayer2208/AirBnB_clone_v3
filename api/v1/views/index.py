#!/usr/bin/python3
"""index module for the API"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'])
def status():
    """Returns the status of the API"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Retrieves the count of all objects by type"""
    class_names = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    counts = {cls: storage.count(class_name) for cls, class_name in class_names.items()}
    return jsonify(counts)
