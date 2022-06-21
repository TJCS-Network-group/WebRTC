#!/usr/bin/env python3
# -*- coding: gbk -*-
#返回值规范
from typing import Dict, List
#flask
from flask_login import current_user, login_user, logout_user, login_required
from flask import make_response, request, jsonify, render_template, flash, redirect, url_for, session
#enum
from user.models import User_level

#model
from user.models import Student


#common
import copy
import os
import re
import json
import time
import random
import threading
from datetime import datetime, timedelta


def make_response_json(statusCode: int = 200,
                       message: str = "",
                       data: dict = {},
                       success: bool = None,
                       quick_response: list = None):
    """对flask模块的make_response函数进一步封装
    Args:
        statusCode (int, optional):  Defaults to 200.
        message (str, optional):  Defaults to "".
        data (dict, optional):  Defaults to {}.
        success (bool, optional):  Defaults to None.
        quick_response (list, optional):  Defaults to None.

    Returns:
        flask json response

    ### json格式
    #### { success: boolean, statusCode: int, message: string, data: object }
    ### statusCode:
    #### 200：操作成功返回。
    #### 201：表示创建成功，POST 添加数据成功后必须返回此状态码。
    #### 400：请求格式不对。
    #### 401：未授权。（User/Admin）等
    #### 404：请求的资源未找到。
    #### 500：内部程序错误。

    """
    if type(quick_response) == list and len(quick_response) == 2:
        statusCode = quick_response[0]
        if statusCode == 0:
            statusCode = 200
        message = quick_response[1]
    if success == None:
        if statusCode // 100 == 2:
            success = True
            if message == "":
                message = "success"
        else:
            success = False
            if message == "":
                message = "fail"
    return make_response(
        jsonify({
            'success': success,
            'statusCode': statusCode,
            'message': message,
            'data': data
        }))
