#!/usr/bin/env python3
# -*- coding: gbk -*-

###�û����ղء���ʷ

from flask import Blueprint

user_blue = Blueprint('user',
                      __name__,
                      template_folder="templates",
                      static_folder="static")

from . import models
from . import routes
