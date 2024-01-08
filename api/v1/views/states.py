#!/usr/bin/python3

'''States module'''

import requests
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.state import State


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
    data = requests.get_json()
    if data.is_json:
        if 'name' not in data.keys():
            return 'Not a JSON', 400
        state = State(data)

    return jsonify(state), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    '''Handles a PUT request for state objects'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()

    if data.is_json:
        for key, value in data.items():
            if key == 'id' or key == 'created_at' or key == 'updated_at':
                continue
            else:
                state[key] = value
    else:
        return 'Not a JSON', 400
