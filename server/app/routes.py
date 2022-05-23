#!/usr/bin/env python3
# -*- coding: GBK -*-
###��Ҫ��ע���¼����
from app import app, database
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from user.models import Student  #ģ��
from werkzeug.security import generate_password_hash

from flask_login import LoginManager

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(id):  #loginʱ����
    try:
        user = Student.get(Student.id==id)  
    except:
        user = None
    return user


@app.before_request
def before_request():
    if database.is_closed():
        database.connect()


@app.teardown_request
def teardown_request(exc):  #exc����д��
    if not database.is_closed():
        database.close()


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/")
def rootindex():
    return redirect(url_for('index'))  # �ض���


@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    return render_template('password_login.html')

@app.route('/login', methods=['GET'])
def login():
    # �жϵ�ǰ�û��Ƿ���֤�����ͨ���Ļ�������ҳ
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    return render_template('password_login.html')