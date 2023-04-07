#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-03-28 14:43
# describe：
import os
import shutil

import gradio as gr

from tabs.common import u_handler_common
from utils import u_config, u_file, u_date, u_channel


def init(request: gr.Request):
    """ 初始化 """
    username = u_handler_common.get_username(request)
    u_config.init_config(username)

    # 判断channel_file是否存在，避免由于文件删除后，gradio读取文件时的异常
    channel_file = u_config.user_config.channel_file
    if not u_file.exists(channel_file):
        channel_file = None

    # 去取渠道信息
    channel_txt = u_file.read(channel_file) if channel_file else None

    outputs = [
        gr.File.update(value=channel_file),
        channel_txt
    ]
    return outputs


def handler(_file):
    """
    处理多渠道文件的保存

    :param _file: 多渠道配置文件
    :return:
    """

    # 检查文件 & 渠道
    check_result = u_handler_common.check_file(_file, ['txt']) or u_handler_common.check_channel(_file.name)
    if check_result:
        return check_result

    # 将配置保存在指定用户目录下
    today_str = u_date.get_today_str(f='%Y-%m-%d')
    filename = u_channel.get_filename(_file.orig_name or _file.name)
    suffix = str(_file.orig_name or _file.name).split('.')[-1]
    save_dir = f'res/channels/{today_str}'
    if not u_file.exists(save_dir):
        os.makedirs(save_dir)
    save_path = f'{save_dir}/{u_config.user_config.username}_{filename}.{suffix}'
    shutil.copy(_file.name, save_path)

    # 更新配置
    u_config.user_config.channel_file = os.path.abspath(save_path)  # 这里保存绝对路径，防止gradio后续读取错误
    u_config.save_config(u_config.user_config)

    result = f"【成功】多渠道信息已配置\n{u_file.read(save_path)}"
    return result
