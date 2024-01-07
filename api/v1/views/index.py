#!/usr/bin/python3

''' Index file '''
from . import app_views

@app_views.route('/status', strict_slashes=False)
def status():
    return jsonify('{status: OK}')
