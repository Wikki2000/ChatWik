#!/usr/bin/python3
"""Define application blueprint"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.auth import * 
from api.v1.views.index import *
from api.v1.views.messages import *
from api.v1.views.users import *
