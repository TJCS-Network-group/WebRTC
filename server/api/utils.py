#返回值规范
from typing import Dict, List
#flask
from flask_login import current_user, login_user, logout_user, login_required
from flask import make_response, request, jsonify, render_template, flash, redirect, url_for
#enum
from user.models import User_level

#model
from user.models import Student

#common
import copy
import os
import re
import json
import datetime
import time
import random

# statusCode:
# 200：操作成功返回。
# 201：表示创建成功，POST 添加数据成功后必须返回此状态码。
# 400：请求格式不对。
# 401：未授权。（User/Admin）等
# 404：请求的资源未找到。
# 500：内部程序错误。


def make_response_json(statusCode: int = 200,
                       message: str = "",
                       data: dict = {},
                       success: bool = None,
                       quick_response: list = None):

    if type(quick_response) == list and len(quick_response) == 2:
        statusCode = quick_response[0]
        if statusCode == 0:
            statusCode = 200
        message = quick_response[1]
    if success == None:
        success = True if statusCode // 100 == 2 else False
    return make_response(
        jsonify({
            'success': success,
            'statusCode': statusCode,
            'message': message,
            'data': data
        }))
