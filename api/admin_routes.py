#!/usr/bin/env python3
# -*- coding: gbk -*-
from api.utils import *
from api import api_blue


@api_blue.route('/get_all_user_info', methods=["GET"])
def get_all_user_info():
    if not current_user.is_authenticated:
        return make_response_json(401, "请先登录")
    elif current_user.stu_userlevel!=User_level.Admin.value:
        return make_response_json(401,"您无此权限")
    need=[Student.id,Student.stu_no,Student.stu_name,Student.stu_class_fname]
    try:
        students=Student.select(*need).where(Student.stu_userlevel==User_level.Normal.value)
        student_list=[]
        for student in students:
            student_info=dict()
            student_info["id"]=student.id
            student_info["stu_no"]=student.stu_no
            student_info["stu_name"]=student.stu_name
            student_info["stu_class_fname"]=student.stu_class_fname
            student_info["stu_class_sname"]=student.stu_class_sname
            student_list.append(student_info)
        resp_json={"student_info":student_list}
        return make_response_json(200,"学生信息如下",data=resp_json)
    except Exception as e:
        return make_response_json(500,"发生如下错误"+repr(e))