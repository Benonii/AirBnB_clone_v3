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


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_reviews_by_place(place_id):
    '''Handles a GET request for reviews of place'''
    reviews = []
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    for review in place.reviews:
        reviews.append(review.to_dict())

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    ''' Handles a get request for a specific review object '''
    review = storage.get(Review, review_id)
    if place:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    ''' Handles a DELETE request for a review object '''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(review_id):
    ''' Handles a POST request for review objects '''
    review = None
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json()
    if data:
        if 'name' not in data.keys():
            return 'Missing name', 400
        if 'user_id' not in data.keys():
            return 'Missing user_id', 400
        if 'text' not in data.keys():
            return 'Missing text', 400
        if 'place_id' not in data.keys() or data['place_id'] is None:
            data['place_id'] = place_id

        review = Review(**data)
        storage.new(review)
        storage.save()

        return jsonify(review.to_dict()), 201
    else:
        return 'Not a JSON', 400


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    '''Handles a PUT request for review objects'''
    review = storage.get(Reveiw, review_id)
    if not review:
        abort(404)
    data = request.get_json()

    if data:
        for key, value in data.items():
            if key in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
                continue
            else:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200

    else:
        return 'Not a JSON', 400
