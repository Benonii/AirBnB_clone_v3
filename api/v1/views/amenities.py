#!/usr/bin/python3

'''States module'''

import requests
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.state import State


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    '''Handles a get request for amenity objects'''
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())

    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id):
    ''' Handles a get request for an amenity object '''
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    ''' Handles a DELTE request for amenity objects '''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    ''' Handles a POST request for amenity objects '''
    data = request.get_json()
    if data:
        if 'name' not in data.keys():
            return 'Not a JSON', 400
        amenity = Amenity(**data)
        storage.new(amenity)
        storage.save()

        return jsonify(amenity.to_dict()), 201
    else:
        return 'Not a JSON', 400


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    '''Handles a PUT request for amenity objects'''
    amenity = storage.get(Amenity, state_id)
    if not amenity:
        abort(404)
    data = request.get_json()

    if data:
        for key, value in data.items():
            if key == 'id' or key == 'created_at' or key == 'updated_at':
                continue
            else:
                setattr(amenity, key, value)
        storage.save()

        return jsonify(amenity.to_dict()), 200
    else:
        return 'Not a JSON', 400
