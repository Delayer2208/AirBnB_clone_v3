#!/usr/bin/python3
"""Places Amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from datetime import datetime
import uuid
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    @app_views.route('/places/<place_id>/amenities', methods=['GET'])
    @app_views.route('/places/<place_id>/amenities/', methods=['GET'])
    def list_amenities_of_place(place_id):
        '''Retrieve a list of all Amenity objects of a Place'''
        all_places = storage.all("Place").values()
        place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
        if place_obj == []:
            abort(404)
        list_amenities = []
        for obj in all_places:
            if obj.id == place_id:
                for amenity in obj.amenities:
                    list_amenities.append(amenity.to_dict())
        return jsonify(list_amenities)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'])
    def create_place_amenity(place_id, amenity_id):
        '''Create an Amenity'''
        all_places = storage.all("Place").values()
        place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
        if place_obj == []:
            abort(404)

        all_amenities = storage.all("Amenity").values()
        amenity_obj = [obj.to_dict() for obj in all_amenities
                       if obj.id == amenity_id]
        if amenity_obj == []:
            abort(404)

        amenities = []
        for place in all_places:
            if place.id == place_id:
                for amenity in all_amenities:
                    if amenity.id == amenity_id:
                        place.amenities.append(amenity)
                        storage.save()
                        amenities.append(amenity.to_dict())
                        return jsonify(amenities[0]), 200
        return jsonify(amenities[0]), 201

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'])
    def delete_place_amenity(place_id, amenity_id):
        '''Delete an Amenity object'''
        all_places = storage.all("Place").values()
        place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
        if place_obj == []:
            abort(404)

        all_amenities = storage.all("Amenity").values()
        amenity_obj = [obj.to_dict() for obj in all_amenities
                       if obj.id == amenity_id]
        if amenity_obj == []:
            abort(404)
        amenity_obj.remove(amenity_obj[0])

        for obj in all_places:
            if obj.id == place_id:
                if obj.amenities == []:
                    abort(404)
                for amenity in obj.amenities:
                    if amenity.id == amenity_id:
                        storage.delete(amenity)
                        storage.save()
        return jsonify({}), 200
else:
    # Non-DB storage implementation
    @app_views.route('/places/<place_id>/amenities', methods=['GET'])
    @app_views.route('/places/<place_id>/amenities/', methods=['GET'])
    def list_amenities_of_place(place_id):
        '''Retrieve a list of all Amenity objects of a Place'''
        all_places = storage.all("Place").values()
        place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
        if place_obj == []:
            abort(404)
        list_amenities = []
        for obj in all_places:
            if obj.id == place_id:
                for amenity in obj.amenities:
                    list_amenities.append(amenity.to_dict())
        return jsonify(list_amenities)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'])
    def create_place_amenity(place_id, amenity_id):
        '''Create an Amenity'''
        all_places = storage.all("Place").values()
        place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
        if place_obj == []:
            abort(404)

        all_amenities = storage.all("Amenity").values()
        amenity_obj = [obj.to_dict() for obj in all_amenities
                       if obj.id == amenity_id]
        if amenity_obj == []:
            abort(404)

        amenities = []
        for place in all_places:
            if place.id == place_id:
                for amenity in all_amenities:
                    if amenity.id == amenity_id:
                        place.amenities.append(amenity)
                        storage.save()
                        amenities.append(amenity.to_dict())
                        return jsonify(amenities[0]), 200
        return jsonify(amenities[0]), 201

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'])
    def delete_place_amenity(place_id, amenity_id):
        '''Delete an Amenity object'''
        all_places = storage.all("Place").values()
        place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
        if place_obj == []:
            abort(404)

        all_amenities = storage.all("Amenity").values()
        amenity_obj = [obj.to_dict() for obj in all_amenities
                       if obj.id == amenity_id]
        if amenity_obj == []:
            abort(404)
        amenity_obj.remove(amenity_obj[0])

        for obj in all_places:
            if obj.id == place_id:
                if obj.amenities == []:
                    abort(404)
                for amenity in obj.amenities:
                    if amenity.id == amenity_id:
                        storage.delete(amenity)
                        storage.save()
        return jsonify({}), 200
