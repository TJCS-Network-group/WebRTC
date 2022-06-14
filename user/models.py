#!/usr/bin/env python3
# -*- coding: gbk -*-

from app import BaseModel
import peewee as pw
from werkzeug.security import check_password_hash
from hashlib import md5
from flask_login import UserMixin

from enum import Enum, unique


#添加 unique 装饰器
@unique
class User_level(Enum):
    #用户状态：0为考生，1为监控者
    Normal = 0
    Admin = 1


class Student(UserMixin, BaseModel):
    """
    用户类
    继承自UserMixin，可以方便地使用各种flask_login的API
    同时继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    """
    #id = pw.AutoField()  # 主键，不显式定义的话peewee默认定义一个自增的id
    stu_grade = pw.IntegerField(verbose_name="年级", null=False)
    stu_no = pw.CharField(verbose_name="学号", max_length=8, null=False)
    stu_name = pw.CharField(verbose_name="名字", max_length=16, null=False)
    stu_password = pw.CharField(verbose_name="密码的md5码",
                                max_length=128,
                                null=False)
    stu_sex = pw.CharField(verbose_name="性别",
                           max_length=2,
                           null=False,
                           default="男")
    stu_class_fname = pw.CharField(verbose_name="专业全称",
                                   max_length=32,
                                   null=False)
    stu_class_sname = pw.CharField(verbose_name="专业简称",
                                   max_length=16,
                                   null=False)
    stu_term = pw.CharField(verbose_name="学期", max_length=11)
    stu_cno = pw.CharField(verbose_name="课程代码", max_length=8)
    stu_wtype = pw.IntegerField(verbose_name="题目类别", default=0)  #（考虑有些学生单独做大题）
    stu_userlevel = pw.IntegerField(
        verbose_name="学生身份", default=User_level.Normal.value)  #（0表示考生，1表示监控者）
    stu_enable = pw.BooleanField("是否允许登录", default=False)

    def check_password(self, password):
        return check_password_hash(self.stu_password, password)

    def __repr__(self):
        return '<Student类 学生学号:{}，姓名：{}>'.format(self.stu_no, self.stu_name)

    #class Meta:
    #    primary_key = pw.CompositeKey('stu_grade', 'stu_no')  #组合主键
