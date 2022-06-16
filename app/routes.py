#!/usr/bin/env python3
# -*- coding: gbk -*-
###主要是注册登录管理
from urllib3 import Retry
from app import app, database
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from user.models import Student, User_level  #模型
from werkzeug.security import generate_password_hash
from flask_login import LoginManager

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(id):  #login时传入
    try:
        user = Student.get(Student.id == id)
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


@app.route("/")
def rootindex():
    # 判断当前用户是否验证，如果通过的话直接进入录屏页
    if current_user.is_authenticated:
        return redirect(url_for('video'))
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    #登出
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET'])
def login():
    # 判断当前用户是否登录，如果已登录的话直接让它去对应的用户主页
    if current_user.is_authenticated:
        if current_user.stu_userlevel == User_level.Admin.value:
            return redirect(url_for('admin'))
        elif current_user.stu_userlevel == User_level.Normal.value:
            return redirect(url_for('video'))
    return render_template('password_login.html')


@app.route('/admin', methods=['GET'])
def admin():
    if not current_user.is_authenticated:
        return render_template('404.html', error_code=401, error_text="请先登录")
    elif current_user.stu_userlevel != User_level.Admin.value:
        return render_template('404.html', error_code=401, error_text="您不是管理员")
    return render_template('admin.html')


@app.route('/admin_video/<stu_no>', methods=['GET'])
def admin_video(stu_no):
    if not current_user.is_authenticated:
        return render_template('404.html', error_code=401, error_text='请先登录')
    elif current_user.stu_userlevel != User_level.Admin.value:
        return render_template('404.html', error_code=401, error_text="您不是管理员")
    return render_template('admin_video.html', stu_no=stu_no)


@app.route('/video', methods=['GET'])
def video():
    if not current_user.is_authenticated:
        return render_template('404.html', error_code=401, error_text="请先登录")
    if current_user.stu_userlevel == User_level.Admin.value:
        return redirect('admin')
    return render_template('video.html')


@app.route('/video_websocket', methods=['GET'])
def video_websocket():
    if not current_user.is_authenticated:
        return render_template('404.html', error_code=401, error_text="请先登录")
    return render_template('video_websocket.html')


@app.errorhandler(404)
def page_not_found(error_message):
    return render_template("404.html",
                           error_text=error_message,
                           error_code=404)
