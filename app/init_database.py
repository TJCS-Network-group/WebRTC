#!/usr/bin/env python3
# -*- coding: gbk -*-

#model
from user.models import Student, User_level


def drop_tables():
    if Student.table_exists:
        Student.drop_table()


def create_tables():
    Student.create_table()


from werkzeug.security import generate_password_hash


def fake_data():  #填一些假数据进去
    
    Student.create(stu_grade="2019",
                   stu_no="1234567",
                   stu_name="张三",
                   stu_password=generate_password_hash(password="1234567",
                                                       method="pbkdf2:md5"),
                   stu_sex="男",
                   stu_class_fname="计算机科学与技术",
                   stu_class_sname="计科",
                   stu_term="2021/2022/2",
                   stu_cno="10106203",
                   stu_wtype=0,
                   stu_userlevel=User_level.Normal.value,
                   stu_enable=True)
    
    Student.create(stu_grade="2019",
                   stu_no="1950638",
                   stu_name="陈冠忠",
                   stu_password=generate_password_hash(password="1950638",
                                                       method="pbkdf2:md5"),
                   stu_sex="男",
                   stu_class_fname="计算机科学与技术",
                   stu_class_sname="计科",
                   stu_term="2021/2022/2",
                   stu_cno="10106203",
                   stu_wtype=0,
                   stu_userlevel=User_level.Normal.value,
                   stu_enable=True)
    Student.create(stu_grade="2019",
                   stu_no="1951705",
                   stu_name="高曾谊",
                   stu_password=generate_password_hash(password="1951705",
                                                       method="pbkdf2:md5"),
                   stu_sex="男",
                   stu_class_fname="计算机科学与技术",
                   stu_class_sname="计科",
                   stu_term="2021/2022/2",
                   stu_cno="10106203",
                   stu_wtype=0,
                   stu_userlevel=User_level.Normal.value,
                   stu_enable=True)
    Student.create(stu_grade="2019",
                   stu_no="1953493",
                   stu_name="程森",
                   stu_password=generate_password_hash(password="1953493",
                                                       method="pbkdf2:md5"),
                   stu_sex="男",
                   stu_class_fname="计算机科学与技术",
                   stu_class_sname="计科",
                   stu_term="2021/2022/2",
                   stu_cno="10106203",
                   stu_wtype=0,
                   stu_userlevel=User_level.Normal.value,
                   stu_enable=True)
    Student.create(stu_grade="0000",
                   stu_no="9999999",
                   stu_name="监控",
                   stu_password=generate_password_hash(password="9999999",
                                                       method="pbkdf2:md5"),
                   stu_sex="男",
                   stu_class_fname="计算机",
                   stu_class_sname="计算机",
                   stu_term="0000",
                   stu_cno="0000",
                   stu_wtype=0,
                   stu_userlevel=User_level.Admin.value,
                   stu_enable=True)


def init_database(drop_database: bool):
    if drop_database == True:
        drop_tables()
        create_tables()
        fake_data()
