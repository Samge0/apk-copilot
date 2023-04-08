#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-04-05 20:11
# describe：
import json
import os
import threading
from copy import deepcopy

from models.m_apk import ApkOption
from utils import u_file, u_json

"""
该项目的配置工具类
"""

true = True
false = False
null = None


# 创建一个线程锁
lock = threading.Lock()


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
    username = username or 'default'
    save_dir = f'res/user_configs/{username}'
    u_file.makedirs(save_dir)
    return f"{save_dir}/user_config.json"


def save_config(_config: ApkOption):
    """ 保存用户配置 """
    save_txt = json.dumps(_config.dict(), indent=4, ensure_ascii=False)
    save_path = get_config_path(user_config.username)
    u_file.save(save_txt, save_path)


def init_config(username: str):
    """ 初始化用户配置 """
    lock.acquire()  # 获取线程锁
    if username and username == user_config.username:
        lock.release()  # 释放线程锁
        return
    user_config_path = get_config_path(username)
    user_config_json = u_file.read(user_config_path)
    config_dict = u_json.eval_dict(user_config_json or ApkOption.__dict__)
    user_config_option = ApkOption.parse_obj(config_dict)
    user_config_option.username = username
    update_config(user_config_option)
    lock.release()  # 释放线程锁


def update_config(_option: ApkOption):
    """ 更新用户配置 """
    global user_config
    user_config = deepcopy(_option)
    save_config(user_config)


if __name__ == '__main__':
    init_config('test')
