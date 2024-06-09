#!/usr/bin/python3
"""Handles all RESTful API actions for City objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'])
def list_cities_of_state(state_id):
    """Retrieves all City objects for a given state"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a new City object for a given state"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    new_city = City(name=request.json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a specific City object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a specific City object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a specific City object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' in request.json:
        city.name = request.json['name']
    storage.save()
    return jsonify(city.to_dict()), 200
