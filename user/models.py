#!/usr/bin/env python3
# -*- coding: gbk -*-

from app import BaseModel
import peewee as pw
from werkzeug.security import check_password_hash
from hashlib import md5
from flask_login import UserMixin

from enum import Enum, unique


#��� unique װ����
@unique
class User_level(Enum):
    #�û�״̬��0Ϊ������1Ϊ�����
    Normal = 0
    Admin = 1


class Student(UserMixin, BaseModel):
    """
    �û���
    �̳���UserMixin�����Է����ʹ�ø���flask_login��API
    ͬʱ�̳���BaseModel��ֱ�ӹ���db������Ҳ�̳���Model Model���ṩ��ɾ��ĵĺ���
    """
    #id = pw.AutoField()  # ����������ʽ����Ļ�peeweeĬ�϶���һ��������id
    stu_grade = pw.IntegerField(verbose_name="�꼶", null=False)
    stu_no = pw.CharField(verbose_name="ѧ��", max_length=8, null=False)
    stu_name = pw.CharField(verbose_name="����", max_length=16, null=False)
    stu_password = pw.CharField(verbose_name="�����md5��",
                                max_length=128,
                                null=False)
    stu_sex = pw.CharField(verbose_name="�Ա�",
                           max_length=2,
                           null=False,
                           default="��")
    stu_class_fname = pw.CharField(verbose_name="רҵȫ��",
                                   max_length=32,
                                   null=False)
    stu_class_sname = pw.CharField(verbose_name="רҵ���",
                                   max_length=16,
                                   null=False)
    stu_term = pw.CharField(verbose_name="ѧ��", max_length=11)
    stu_cno = pw.CharField(verbose_name="�γ̴���", max_length=8)
    stu_wtype = pw.IntegerField(verbose_name="��Ŀ���", default=0)  #��������Щѧ�����������⣩
    stu_userlevel = pw.IntegerField(
        verbose_name="ѧ�����", default=User_level.Normal.value)  #��0��ʾ������1��ʾ����ߣ�
    stu_enable = pw.BooleanField("�Ƿ������¼", default=False)

    def check_password(self, password):
        return check_password_hash(self.stu_password, password)

    def __repr__(self):
        return '<Student�� ѧ��ѧ��:{}��������{}>'.format(self.stu_no, self.stu_name)

    #class Meta:
    #    primary_key = pw.CompositeKey('stu_grade', 'stu_no')  #�������
