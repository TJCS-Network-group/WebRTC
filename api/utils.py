#!/usr/bin/env python3
# -*- coding: gbk -*-
#����ֵ�淶
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
    """��flaskģ���make_response������һ����װ
    Args:
        statusCode (int, optional):  Defaults to 200.
        message (str, optional):  Defaults to "".
        data (dict, optional):  Defaults to {}.
        success (bool, optional):  Defaults to None.
        quick_response (list, optional):  Defaults to None.

    Returns:
        flask json response

    ### json��ʽ
    #### { success: boolean, statusCode: int, message: string, data: object }
    ### statusCode:
    #### 200�������ɹ����ء�
    #### 201����ʾ�����ɹ���POST ������ݳɹ�����뷵�ش�״̬�롣
    #### 400�������ʽ���ԡ�
    #### 401��δ��Ȩ����User/Admin����
    #### 404���������Դδ�ҵ���
    #### 500���ڲ��������

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
