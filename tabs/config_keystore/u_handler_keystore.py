#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-03-28 14:43
# describe：
import os
import shutil

import gradio as gr

from tabs.common import u_handler_common
from utils import u_config, u_channel, u_file


def init(request: gr.Request):
    """ 初始化 """
    username = u_handler_common.get_username(request)
    u_config.init_config(username)

    # 读取keystore的信息
    status, key_info = u_channel.read_key_info(
        u_config.user_config.key_file,
        u_config.user_config.key_alias,
        u_config.user_config.key_store_pw,
        u_config.user_config.key_pw
    )

    # 判断key_file是否存在，避免由于文件删除后，gradio读取文件时的异常
    key_file = u_config.user_config.key_file
    if not u_file.exists(key_file):
        key_file = None

    outputs = [
        gr.File.update(value=key_file),
        u_config.user_config.key_pw,
        u_config.user_config.key_alias,
        u_config.user_config.key_store_pw,
        key_info
    ]
    return outputs


def handler(_file, key_pw, key_alias, key_store_pw):
    """
    处理keystore文件的保存

    :param _file: keystore的文件路径
    :param key_pw: keystore的密码
    :param key_alias: keystore别名
    :param key_store_pw: keystore密钥库密码
    :return:
    """

    # 检查文件
    check_result = u_handler_common.check_file(_file, ['keystore', 'jks'])
    if check_result:
        return check_result

    # 检查keystore是否配置正确
    status, key_info = u_channel.read_key_info(_file.name, key_alias, key_store_pw, key_pw)
    if not status:
        return key_info

    # 将配置保存在指定用户目录下
    save_path = u_handler_common.copy_file_with_date(_file, 'res/keystores')

    # 更新配置
    u_config.user_config.key_file = os.path.abspath(save_path)  # 这里保存绝对路径，防止gradio后续读取错误
    u_config.user_config.key_pw = key_pw
    u_config.user_config.key_alias = key_alias
    u_config.user_config.key_store_pw = key_store_pw
    u_config.save_config(u_config.user_config)

    result = f"keystore配置结果：\n{key_info}"
    return result
