#!/usr/bin/env python3
# -*- coding: GBK -*-
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


@user_blue.route("/", methods=['GET', 'POST'])
def root_index():
    return redirect(url_for('user.index'))  # 重定向到/user/index


@user_blue.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html',current_user=current_user)