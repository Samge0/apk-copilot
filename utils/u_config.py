#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-04-05 20:11
# describe：
import json
import os
from copy import deepcopy

from models.m_apk import ApkOption
from utils import u_file, u_json

"""
该项目的配置工具类
"""

true = True
false = False
null = None

# 全局公共配置
g_config = ApkOption.parse_obj(u_json.eval_dict(u_file.read('config.json') or {}))
# 尝试从环境变量中读取auth配置，配置格式为：user1:pw1|user2:pw2
env_auth_config = os.environ.get("APK_COPILOT_AUTH") or ''
if env_auth_config:
    g_config.auth = g_config.auth or []
    for auth_str in env_auth_config.split('|'):
        auth_user = auth_str.split(':') or []
        if len(auth_user) < 2:
            continue
        g_config.auth.append(auth_user)

# 全局用户配置
user_config = ApkOption()


def get_config_path(username: str) -> str:
    return f"config_{username}.json" if username else "config_default.json"


def save_config(_config: ApkOption):
    """ 保存用户配置 """
    save_data = deepcopy(_config)
    # apk信息每次都需要上传，不需要保存到配置
    save_data.apk_path = None
    save_data.apk_name = None
    u_file.save(json.dumps(save_data.dict(), indent=4, ensure_ascii=False), get_config_path(user_config.username))


def init_config(username: str):
    """ 初始化用户配置 """
    if username and username == user_config.username:
        return
    user_config_path = get_config_path(username)
    user_config_json = u_file.read(user_config_path)
    config_dict = u_json.eval_dict(user_config_json or ApkOption.__dict__)
    user_config_option = ApkOption.parse_obj(config_dict)
    user_config_option.username = username
    update_config(user_config_option)


def update_config(_option: ApkOption):
    """ 更新用户配置 """
    global user_config
    user_config = deepcopy(_option)
    # 不需要保存apk路径信息，因为apk都是临时上传的
    save_config(user_config)


if __name__ == '__main__':
    init_config('test')
