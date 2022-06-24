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
    #û��ֵ�����⴦������ע��
    cf = configparser.ConfigParser(allow_no_value=True,
                                   comment_prefixes=('#', ';'),
                                   inline_comment_prefixes=(';', '#'))
    cf.read(path,encoding="gbk")
    secs = cf.sections()
    for section in secs:  #��ȡÿ��[section]
        if section == "root-dir":  #û��ֵ�����⴦��
            #print(cf.options(section))
            data[section] = cf.options(section)[0]
            continue
        option_data = dict()
        for option, value in cf.items(section):  #��ÿ��section���items
            try:
                value=int(value)
            except:
                pass
            option_data[option] = value  #frame�Ͷ���ʱ�䶼��int
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
    # data = dict(request.args)
    # try:
    #     id = int(data["id"])
    # except:
    #     return make_response_json(400, "�����ʽ����")
    # try:
    #     user = Student.get(Student.id == id)
    # except:
    #     return make_response_json(404, "�û�������")
    # target_path = f"./etc/webrtc-{id}.conf"  #�����ļ�����������֮����Ը�
    # if not os.path.exists(target_path):
    #     return make_response_json(404,"δ�ҵ����û��������ļ�")
    # try:
    #     data = get_config(target_path)
    # except Exception as e:
    #     return make_response_json(500, "����������"+repr(e))
    # return make_response_json(data=data)
    if request.args.get('id') is None:
        id = current_user.id
    else:
        id = request.args.get('id')
    target_path = BASE_DIR+f"/etc/webrtc-{id}.conf"  #�����ļ�����������֮����Ը�
    if not os.path.exists(target_path):
        data = get_config(BASE_DIR+"./etc/webrtc-default.conf")
        print(data)
        # return make_response_json(404,"δ�ҵ����û��������ļ�")
    else:
        try:
            data = get_config(target_path)
        except Exception as e:
            return make_response_json(500, "����������"+repr(e))
    return make_response_json(data=data)
