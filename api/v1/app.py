#!/usr/bin/python3

'''Main app module'''

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://0.0.0.0"}})
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown(exception):
    ''' Handles teardown '''
    storage.close()


host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')


@app.errorhandler(404)
def page_not_found(error):
    '''Returns a JSON 404'''
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
