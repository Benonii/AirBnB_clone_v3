#!/usr/bin/python3

''' Init '''

from flask import Blueprint
from .index import *

app_views = Blueprint('app_views', url_prefix='/api/v1')
