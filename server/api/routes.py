#!/usr/bin/env python3
# -*- coding: GBK -*-
from api.utils import *
from api import api_blue


def judge_password(password: str):
    if type(password) != str:
        return [400, "密码格式错误"]
    if len(password) < 6:
        return [400, "密码过短"]
    if len(password) > 32:
        return [400, "密码过长"]
    pattern = re.compile(r'[a-zA-Z0-9_-]')
    result = pattern.findall(password)
    if len(result) != len(password):
        return [400, "密码含有非法字符"]
    return [0, "验证通过"]


def _login(stu_no, password=None):
    try:
        user = Student.get(Student.stu_no == stu_no)  # 此处还可以添加判断用户是否时管理员
    except:
        return make_response_json(400, "账号不存在")

    if password != None:
        if not user.check_password(password):
            return make_response_json(400, "密码错误")

    if user.stu_enable == -1:
        return make_response_json(400, "您的账号已被冻结")

    # 记住登录状态，同时维护current_user
    login_user(user, True, datetime.timedelta(days=30))

    return make_response_json(data={"url": url_for('user.index')})


@api_blue.route('/login_using_password', methods=['POST'])
def login_using_password():
    user_id = request.form.get('user_no')
    password = request.form.get('password')
    jp = judge_password(password)
    if jp[0] != 0:
        return make_response_json(quick_response=jp)
    return _login(user_id, password)
