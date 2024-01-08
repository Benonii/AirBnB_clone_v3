#!/usr/bin/python3

'''Index file'''

from flask import jsonify
from api.v1.views import app_views
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    ''' Returns the status '''
    return jsonify({'status': 'OK'})


@app_views.route("stats", strict_slashes=False)
def get_stats():
    '''Get statistics '''
    stats = {
            "amemites": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
    }
    return jsonify(stats)
