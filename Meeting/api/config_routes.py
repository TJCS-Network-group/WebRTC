#!/usr/bin/env python3
# -*- coding: gbk -*-
from api.utils import *
from api import api_blue
import configparser


def get_config(path: str) -> dict:
    """获取用户配置文件中的配置

    Args:
        path (str): 用户配置文件的路径

    Returns:
        dict: {"": }
    """
    data = dict()
    cf = configparser.ConfigParser(allow_no_value=True)#没有值，特殊处理
    cf.read(path)
    secs = cf.sections()
    for section in secs:  #获取每个[section]
        if section=="root-dir":#没有值，特殊处理
            print(cf.options(section))
            data[section]=cf.options(section)[0]
        option_data = dict()
        for option, value in cf.items(section):  #对每个section里的items
            option_data[option] = value
        data[section] = option_data
    return data


@api_blue.route('/get_config', methods=['GET'])
def _get_config():
    """api路由/api/get_config, GET方法传入用户表主键id
    沈坚pdf里面说文件名为webrtc-*.conf
    这里的*直接就取主键id了，因为学号可能会重复

    Returns:
        flask json response
    """
    #if not current_user.is_authenticated:
    #    return make_response_json(401, "当前用户未登录")
    data = dict(request.args)
    try:
        id = int(data["id"])
    except:
        return make_response_json(400, "请求格式不对")
    try:
        user = Student.get(Student.id == id)
    except:
        return make_response_json(404, "用户不存在")
    target_path = f"./etc/webrtc-{id}.conf"  #配置文件存在哪里，这个之后可以改
    data = get_config(target_path)
    return make_response_json(data)
