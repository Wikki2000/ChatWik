#!/usr/bin/python3
"""Create the Blueprint of Flask"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__)

from api.v1.views.auth.login import *
from api.v1.views.auth.send_token import *
from api.v1.views.auth.register import *
from api.v1.views.messages import *
from api.v1.views.users import *
from api.v1.views.index import *
