#!/usr/bin/env python3
# -*- coding: gbk -*-

from flask import Blueprint

api_blue = Blueprint('api',
                     __name__,
                     template_folder="templates",
                     static_folder='static')

from . import login_routes
from . import video_routes
from . import config_routes
from . import admin_routes