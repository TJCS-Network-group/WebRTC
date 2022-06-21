#!/usr/bin/env python3
# -*- coding: gbk -*-
from api.utils import *
from api import api_blue
from werkzeug.security import generate_password_hash
from flask import request

def check_and_login(stu_no, password=None):
    need=[Student.id,Student.stu_grade,Student.stu_password,Student.stu_enable,Student.stu_userlevel]
    users = Student.select(*need).where(Student.stu_no == stu_no)
    if users.count()==0:#没找到
        return make_response_json(400, "账号不存在")
    elif users.count()>1:#有多个，则以grade最大的为准（考虑重修）
        user=None
        user_grade=-1
        for tepuser in users:
            if user_grade<tepuser.stu_grade:
                user=tepuser
                user_grade=tepuser.stu_grade
    if users.count()==1:#仅仅一个
        user=users[0]
    if password != None:
        if not user.check_password(password):
            return make_response_json(400, "密码错误")

    if user.stu_enable == -1:
        return make_response_json(400, "您的账号已被冻结")

    # 记住登录状态，同时维护current_user

    login_user(user, True, timedelta(days=30))
    print(user.stu_userlevel)
    if user.check_password(stu_no):
        return make_response_json(data={"url":"/ChangePassword"})
    if user.stu_userlevel==User_level.Normal.value:
        target_url="/Video"
    elif user.stu_userlevel==User_level.Admin.value:
        target_url="/Admin"
    resp = make_response_json(data={"url": target_url})
    resp.set_cookie("account", stu_no)
    return resp

def check_password_pattern(password:str) -> bool:
    num = re.compile("[0-9]")
    small_letter = re.compile("[a-z]")
    big_letter = re.compile("[A-Z]")
    special = re.compile("[+\-\*_&%]")
    # s = [reps.findall(password) for reps in [num,small_letter,big_letter,special]]
    result = [len(reps.findall(password)) for reps in [num,small_letter,big_letter,special]]
    # print(s,result)
    if 0 in result or sum(result) != len(password):
        return False
    return True

@api_blue.route('/login_using_password', methods=['POST'])
def login_using_password():
    user_no = request.form.get('user_no')
    password = request.form.get('password')
    session['account'] = str(user_no)
    return check_and_login(user_no, password)

@api_blue.route('/logout')
def logout():
    logout_user()
    resp = make_response_json(data={"url": "/Login"})
    resp.delete_cookie("account")
    return resp

@api_blue.route("/myinfo",methods=["GET"])
def myinfo():
    if not current_user.is_authenticated:
        return make_response_json(400,"请先登录",data={"url":"Login"})
    return make_response_json(200,"信息",data={"stu_no":current_user.stu_no,"stu_name":current_user.stu_name})
    

@api_blue.route('/get_identity', methods=['GET'])
def get_identity():
    retData={}
    if not current_user.is_authenticated:
        retData['isLogin']=False
        return make_response_json(200,"",data=retData)
    else:
        retData['isLogin']=True
    if current_user.stu_userlevel == User_level.Admin.value:
        retData['isAdmin']=True
    else:
        retData['isAdmin']=False
    return make_response_json(200,"",data=retData)


@api_blue.route("/change_password",methods=["POST"])
def change_password():
    if not current_user.is_authenticated:
        return make_response_json(400,"请先登录",data={"url":"/Login"})
    try:
        passwd = request.form.get('password')
    except Exception as e:
        return make_response_json(400,"无新密码")
    if current_user.check_password(passwd):
        return make_response_json(400,"新密码不能与原密码一致")
    if not check_password_pattern(passwd):
        return make_response_json(400,"新密码不符合网站标准")
    current_user.stu_password =generate_password_hash(password=passwd,
                                                       method="pbkdf2:md5")
    current_user.save()
    if current_user.stu_userlevel == User_level.Admin.value:
        return make_response_json(200,"修改成功",data={"url":"/Admin"})
    else:
        return make_response_json(200,"修改成功",data={"url":"/Video"})

