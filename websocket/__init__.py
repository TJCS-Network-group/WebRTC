#!/usr/bin/env python3
# -*- coding: gbk -*-

from flask import Blueprint

websocket_blue = Blueprint('websocket',
                       __name__,
                       template_folder="templates",
                       static_folder='static')
# from . import models
# from . import routes
from . import events
