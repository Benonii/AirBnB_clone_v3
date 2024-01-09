#!/usr/bin/python3

'''Places module'''

import requests
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.state import State
from models.city import City
from models.place import Place 
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def get_amenities_by_place(place_id):
    '''Handles a GET request for amenities of place'''
    amenities = []
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    for amenity in place.amenities:
        amenities.append(review.to_dict())

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenities(place_id, amenity_id):
    ''' Handles a DELETE request for an amenity object '''
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place:
        abort(404)
    if not amenity or amenity not in place.amenites:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route('/api/v1/places/<place_id>/amenities/<amenity_id>', strict_slashes=False,
                 methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    ''' Handles a POST request for amenity objects '''
    amenity = storage.get(Amenity, amenity_id)
    place = storage.get(Place, place_id)

    if not place:
        abort(404)
    if not amenity:
        abort(404)
    amenity_list = place.amenities
    if amenity not in amenity_list:
        amenity_list.append(amenity)
        return jsonify(amenity.to_dict()), 201
    else:
        return jsonify(amenity.to_dict()), 200
