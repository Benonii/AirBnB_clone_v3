#!/usr/bin/python3

'''States module'''

import requests
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['GET'])
def get_cities_by_state(state_id):
    '''Handles a GET request for cities of state'''
    cities = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    for city in state.cities.values():
        cities.append(city.to_dict())

    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    ''' Handles a get request for a specific city object '''
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    ''' Handles a DELTE request for a city object '''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<state_id>/', strict_slashes=False, methods=['POST'])
def create_city():
    ''' Handles a POST request for state objects '''
    city = None
    data = request.get_json()
    if data:
        if 'name' not in data.keys():
            return 'Not a JSON', 400
        state = State(data)

    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_city(state_id):
    '''Handles a PUT request for state objects'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()

    if data:
        for key, value in data.items():
            if key == 'id' or key == 'created_at' or key == 'updated_at':
                continue
            else:
                setattr(state, key, value)

        return jsonify(state.to_dict()), 200
    else:
        return 'Not a JSON', 400
