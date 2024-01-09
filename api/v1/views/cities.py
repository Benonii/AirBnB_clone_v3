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

    for city in state.cities.values():
        cities.append(city.to_dict())

    return jsonify(cities)

@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    '''Handles a get request for state objects'''
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())

    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    ''' Handles a get request for a specific state object '''
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    ''' Handles a DELTE request for state objects '''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        return jsonify({})


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    ''' Handles a POST request for state objects '''
    state = None
    data = request.get_json()
    if data:
        if 'name' not in data.keys():
            return 'Not a JSON', 400
        state = State(data)

    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
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
