#!/usr/bin/python3

'''Index file'''

from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    ''' Returns the status '''
    eturn jsonify({'status': 'OK'})
