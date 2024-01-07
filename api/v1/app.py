#!/usr/bin/python3

'''Main app module'''

from flask import Flask

app = Flask(__name__)

from models import storage
from api.v1.views import app_views
from os import getenv

app.register_blueprint(app_views, url_prefix="/api/v1")

@app.teardown_appcontext
def teardown(exception):
    storage.close()

host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')

if __name__ == "__main__":
    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
