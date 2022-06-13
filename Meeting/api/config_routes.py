#!/usr/bin/env python3
# -*- coding: gbk -*-
from api.utils import *
from api import api_blue
import configparser


def get_config(path: str) -> dict:
    """��ȡ�û������ļ��е�����

    Args:
        path (str): �û������ļ���·��

    Returns:
        dict: {"": }
    """
    data = dict()
    cf = configparser.ConfigParser(allow_no_value=True)#û��ֵ�����⴦��
    cf.read(path)
    secs = cf.sections()
    for section in secs:  #��ȡÿ��[section]
        if section=="root-dir":#û��ֵ�����⴦��
            print(cf.options(section))
            data[section]=cf.options(section)[0]
        option_data = dict()
        for option, value in cf.items(section):  #��ÿ��section���items
            option_data[option] = value
        data[section] = option_data
    return data


@api_blue.route('/get_config', methods=['GET'])
def _get_config():
    """api·��/api/get_config, GET���������û�������id
    ���pdf����˵�ļ���Ϊwebrtc-*.conf
    �����*ֱ�Ӿ�ȡ����id�ˣ���Ϊѧ�ſ��ܻ��ظ�

    Returns:
        flask json response
    """
    #if not current_user.is_authenticated:
    #    return make_response_json(401, "��ǰ�û�δ��¼")
    data = dict(request.args)
    try:
        id = int(data["id"])
    except:
        return make_response_json(400, "�����ʽ����")
    try:
        user = Student.get(Student.id == id)
    except:
        return make_response_json(404, "�û�������")
    target_path = f"./etc/webrtc-{id}.conf"  #�����ļ�����������֮����Ը�
    data = get_config(target_path)
    return make_response_json(data)
