#!/usr/bin/env python3
# -*- coding: gbk -*-
from user import user_blue
from flask import render_template, flash, redirect, url_for, request
from user.models import Student, User_level
from flask_login import current_user, login_user, logout_user, login_required
from app import database


@user_blue.before_request
def before_request():
    if database.is_closed():
        database.connect()


@user_blue.teardown_request
def teardown_request(exc):  #exc必须写上
    if not database.is_closed():
        database.close()


@user_blue.route('/change_password', methods=['GET'])
def change_password():
    if not current_user.is_authenticated:
        return render_template('404.html', error_code=401, error_text="请先登录")
    return render_template('change_password.html')
