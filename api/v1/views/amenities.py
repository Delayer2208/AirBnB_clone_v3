#!/usr/bin/python3
"""Handles all RESTful API actions for Amenity objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities/', methods=['GET'])
def list_amenities():
    """Retrieves a list of all Amenity objects"""
    amenities_list = [amenity.to_dict() for amenity in storage.all("Amenity").values()]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves a single Amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a specific Amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """Creates a new Amenity"""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an existing Amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' in request.json:
        amenity.name = request.json['name']
    storage.save()
    return jsonify(amenity.to_dict()), 200
