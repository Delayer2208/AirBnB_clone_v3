#!/usr/bin/python3
"""Places API endpoints"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place

@app_views.route('/cities/<city_id>/places', methods=['GET'])
@app_views.route('/cities/<city_id>/places/', methods=['GET'])
def list_places_of_city(city_id):
    """Retrieves a list of all Place objects in a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a new Place object within a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, description='Missing user_id')
    if 'name' not in request.get_json():
        abort(400, description='Missing name')
    user = storage.get(User, request.json['user_id'])
    if not user:
        abort(404)
    new_place = Place(
        name=request.json['name'],
        user_id=request.json['user_id'],
        city_id=city_id,
        description=request.json.get('description', ''),
        number_rooms=request.json.get('number_rooms', 0),
        number_bathrooms=request.json.get('number_bathrooms', 0),
        max_guest=request.json.get('max_guest', 0),
        price_by_night=request.json.get('price_by_night', 0),
        latitude=request.json.get('latitude', 0.0),
        longitude=request.json.get('longitude', 0.0)
    )
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
