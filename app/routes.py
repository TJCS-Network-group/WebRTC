#!/usr/bin/env python3
# -*- coding: gbk -*-
###主要是注册登录管理
from app import app, database
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from user.models import Student  #模型
from werkzeug.security import generate_password_hash

from flask_login import LoginManager

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(id):  #login时传入
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
def teardown_request(exc):  #exc必须写上
    if not database.is_closed():
        database.close()


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/")
def rootindex():
    return redirect(url_for('index'))  # 重定向


@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    return render_template('password_login.html')

@app.route('/login', methods=['GET'])
def login():
    # 判断当前用户是否验证，如果通过的话返回录屏页
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    return render_template('password_login.html')


@app.route('/video', methods=['GET'])
def video():
    return render_template('video.html')

@app.route('/video_websocket', methods=['GET'])
def video_websocket():
    return render_template('video_websocket.html')



@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", message=error, error_code=404)

