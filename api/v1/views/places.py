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


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_places_by_city(city_id):
    '''Handles a GET request for places of city'''
    places = []
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    for place in city.places:
        places.append(place.to_dict())

    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
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


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
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
            return 'Missing name', 400

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


@app_views.route('places_search', strict_slashes=False, methods=['POST'])
def places_search():
    '''Handles a search of palces based on state, city and amenities'''
    if 'Content-Type' not in request.headers:
        places = storage.all(Place).values()

    else:
        if request.headers['Content-Type'] == 'application/json':
            data = request.json
        else:
            return 'Not a JSON', 400

        if not data:
            places = storage.all(Place).values()
        else:
            city_objs = []
            states_is_empty = False
            cities_is_empty = False
            if 'states' in data.keys():
                if data['states'] is not None:
                    state_ids = data['states']
                    state_objs = []
                    for state_id in state_ids:
                        state_objs.append(storage.get(State, state_id))

                    for state in state_objs:
                        for city in state.cities:
                            city_objs.append(city)
                else:
                    states_is_empty = True

            if 'cities' in data.keys():
                if data['cities'] is not None:
                    city_ids = data['cities']
                    for city_id in city_ids:
                        city = storage.get(City, city_id)
                    if city not in city_objs:
                        city_objs.append(city)
                else:
                    cities_is_empty = True

            places = []
            for city in city_objs:
                for place in city.places:
                    places.append(place)

            if (states_is_empty and cities_is_empty):
                places = storage.all(Place).values()

            if 'amenities' in data.keys():
                amenity_ids = data['amenities']
                for place in places:
                    for amenity_id in amenity_ids:
                        if amenity_id not in place.amenity_ids:
                            places.remove(place)

    places_dict = []
    for place in places:
        places_dict.append(place.to_dict())

    return jsonify(places_dict)
