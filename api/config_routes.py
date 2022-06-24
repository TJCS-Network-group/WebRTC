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
    #没有值，特殊处理；处理注释
    cf = configparser.ConfigParser(allow_no_value=True,
                                   comment_prefixes=('#', ';'),
                                   inline_comment_prefixes=(';', '#'))
    cf.read(path,encoding="gbk")
    secs = cf.sections()
    for section in secs:  #获取每个[section]
        if section == "root-dir":  #没有值，特殊处理
            #print(cf.options(section))
            data[section] = cf.options(section)[0]
            continue
        option_data = dict()
        for option, value in cf.items(section):  #对每个section里的items
            try:
                value=int(value)
            except:
                pass
            option_data[option] = value  #frame和断联时间都是int
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
    # data = dict(request.args)
    # try:
    #     id = int(data["id"])
    # except:
    #     return make_response_json(400, "请求格式不对")
    # try:
    #     user = Student.get(Student.id == id)
    # except:
    #     return make_response_json(404, "用户不存在")
    # target_path = f"./etc/webrtc-{id}.conf"  #配置文件存在哪里，这个之后可以改
    # if not os.path.exists(target_path):
    #     return make_response_json(404,"未找到该用户的配置文件")
    # try:
    #     data = get_config(target_path)
    # except Exception as e:
    #     return make_response_json(500, "程序发生错误："+repr(e))
    # return make_response_json(data=data)
    if request.args.get('id') is None:
        id = current_user.id
    else:
        id = request.args.get('id')
    target_path = BASE_DIR+f"/etc/webrtc-{id}.conf"  #配置文件存在哪里，这个之后可以改
    if not os.path.exists(target_path):
        data = get_config(BASE_DIR+"./etc/webrtc-default.conf")
        print(data)
        # return make_response_json(404,"未找到该用户的配置文件")
    else:
        try:
            data = get_config(target_path)
        except Exception as e:
            return make_response_json(500, "程序发生错误："+repr(e))
    return make_response_json(data=data)
