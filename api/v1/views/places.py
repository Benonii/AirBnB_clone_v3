#!/usr/bin/python3

'''Places module'''

import requests
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.state import State
from models.city import City
from models.place import Place


@app_views.route('/citites/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_places_by_city(city_id):
    '''Handles a GET request for places of city'''
    places = []
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    for place in city.places:
        palces.append(place.to_dict())

    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(city_id):
    ''' Handles a get request for a specific place object '''
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    ''' Handles a DELETE request for a place object '''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route('/citites/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    ''' Handles a POST request for place objects '''
    place = None
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    data = request.get_json()
    if data:
        if 'name' not in data.keys():
            return 'Missing name', 400i

        if 'user_id' not in data.keys():
            return 'Missing user_id', 400
        user = storage.get(User, data['user_id'])

        if not user:
            abort(404)

        if 'city_id' not in data.keys() or data['city_id'] is None:
            data['city_id'] = city_id

        place = Place(**data)
        storage.new(place)
        storage.save()

        return jsonify(place.to_dict()), 201
    else:
        return 'Not a JSON', 400


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    '''Handles a PUT request for place objects'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()

    if data:
        for key, value in data.items():
            if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                continue
            else:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200

    else:
        return 'Not a JSON', 400
