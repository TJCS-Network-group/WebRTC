#!/usr/bin/env python3
# -*- coding: gbk -*-
from api.utils import *
from api import api_blue
from werkzeug.security import generate_password_hash
from flask import request

def check_and_login(stu_no, password=None):
    need=[Student.id,Student.stu_grade,Student.stu_password,Student.stu_enable]
    users = Student.select(*need).where(Student.stu_no == stu_no)
    if users.count()==0:#û�ҵ�
        return make_response_json(400, "�˺Ų�����")
    elif users.count()>1:#�ж��������grade����Ϊ׼���������ޣ�
        user=None
        user_grade=-1
        for tepuser in users:
            if user_grade<tepuser.stu_grade:
                user=tepuser
                user_grade=tepuser.stu_grade
    if users.count()==1:#����һ��
        user=users[0]
    if password != None:
        if not user.check_password(password):
            return make_response_json(400, "�������")

    if user.stu_enable == -1:
        return make_response_json(400, "�����˺��ѱ�����")

    # ��ס��¼״̬��ͬʱά��current_user

    login_user(user, True, datetime.timedelta(days=30))
    if user.check_password(stu_no):
        return make_response_json(data={"url":url_for('user.change_password')})
    if user.stu_userlevel==User_level.Normal.value:
        target_url=url_for('video')
    elif user.stu_userlevel==User_level.Admin.value:
        target_url=url_for('admin')
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



@api_blue.route("/change_password",methods=["POST"])
def change_password():
    if not current_user.is_authenticated:
        return make_response_json(400,"���ȵ�¼",data={"url":url_for('login')})
    try:
        passwd = request.get_json()["password"]
    except Exception as e:
        return make_response_json(400,"��������")
    if current_user.check_password(passwd):
        return make_response_json(400,"�����벻����ԭ����һ��")
    if not check_password_pattern(passwd):
        return make_response_json(400,"�����벻������վ��׼")
    current_user.stu_password =generate_password_hash(password=passwd,
                                                       method="pbkdf2:md5")
    current_user.save()
    return make_response_json(200,"�޸ĳɹ�",data={"url":url_for('video')})

