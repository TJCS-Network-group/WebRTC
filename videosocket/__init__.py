#!/usr/bin/env python3
# -*- coding: gbk -*-

from flask import Blueprint

video_blue = Blueprint('videosocket',
                       __name__,
                       template_folder="templates",
                       static_folder='static')
# from . import models
# from . import routes
from . import events
