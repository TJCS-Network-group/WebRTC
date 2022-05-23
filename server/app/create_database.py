#!/usr/bin/env python3
# -*- coding: GBK -*-

import pymysql


def create_database(database_name="user",
                    password='tj_market',
                    user="root",
                    host="127.0.0.1",
                    charset="gbk"):
    """python + pymysql �������ݿ�"""

    # ��������
    conn = pymysql.connect(host=host,
                           user=user,
                           password=password,
                           charset=charset)
    # �����α�
    cursor = conn.cursor()

    # �������ݿ��sql(������ݿ���ھͲ���������ֹ�쳣)
    sql = "DROP DATABASE IF EXISTS " + database_name
    # ִ��ɾ�����ݿ��sql
    cursor.execute(sql)

    sql = "CREATE DATABASE IF NOT EXISTS " + database_name
    # ִ�д������ݿ��sql
    cursor.execute(sql)
