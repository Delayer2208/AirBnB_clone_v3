#!/usr/bin/python3
"""Users API endpoints"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
@app_views.route('/users/', methods=['GET'])
def list_users():
    """Retrieves a list of all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
@app_views.route('/users/', methods=['POST'])
def create_user():
    """Creates a User"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    
    new_user = User(email=data['email'], password=data['password'])
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    ignore_fields = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_fields:
            setattr(user, key, value)
    
    storage.save()
    return jsonify(user.to_dict()), 200
