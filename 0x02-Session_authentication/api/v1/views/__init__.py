#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *  # nopep8
from api.v1.views.users import *  # nopep8
from api.v1.views.session_auth import *  # nopep8

User.load_from_file()
