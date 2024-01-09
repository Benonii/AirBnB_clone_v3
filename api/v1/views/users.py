#!/usr/bin/python3

'''Users module'''

import requests
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.state import State
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    '''Handles a get request for user objects'''
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())

    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    ''' Handles a get request for a specific user object '''
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    ''' Handles a DELTE request for a user object '''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    ''' Handles a POST request for user objects '''
    data = request.get_json()
    if data:
        if 'email' not in data.keys():
            return 'Missing email', 400
        if 'password' not in data.keys():
            return 'Missing password', 400
        user = User(**data)
        storage.new(user)
        storage.save()

        return jsonify(user.to_dict()), 201
    else:
        return 'Not a JSON', 400


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    '''Handles a PUT request for state objects'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()

    if data:
        for key, value in data.items():
            if key == 'id' or key == 'created_at' or key == 'updated_at':
                continue
            else:
                setattr(user, key, value)
        storage.save()

        return jsonify(user.to_dict()), 200
    else:
        return 'Not a JSON', 400
