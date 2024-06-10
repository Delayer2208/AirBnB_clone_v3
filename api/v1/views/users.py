#!/usr/bin/python3
"""Users"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from datetime import datetime
import uuid

@app_views.route('/users/', methods=['GET'])
@app_views.route('/users', methods=['GET'])
def list_users():
    '''Retrieve a list of all User objects'''
    list_users = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(list_users)

@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    '''Retrieve a User object'''
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    return jsonify(user_obj[0])

@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    '''Delete a User object'''
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    user_obj.remove(user_obj[0])
    for obj in all_users:
        if obj.id == user_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200

@app_views.route('/users/', methods=['POST'])
def create_user():
    '''Create a User'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')
    users = []
    new_user = User(email=request.json['email'],
                    password=request.json['password'])
    storage.new(new_user)
    storage.save()
    users.append(new_user.to_dict())
    return jsonify(users[0]), 201

@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    '''Update a User object'''
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'first_name' in request.get_json():
        user_obj[0]['first_name'] = request.json['first_name']
    if 'last_name' in request.get_json():
        user_obj[0]['last_name'] = request.json['last_name']
    for obj in all_users:
        if obj.id == user_id:
            if 'first_name' in request.get_json():
                obj.first_name = request.json['first_name']
            if 'last_name' in request.get_json():
                obj.last_name = request.json['last_name']
    storage.save()
    return jsonify(user_obj[0]), 200
