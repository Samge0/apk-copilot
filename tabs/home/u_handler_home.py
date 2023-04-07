#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-03-28 14:43
# describe：
import gradio as gr
from models.m_apk import ZipOption
from tabs.common import u_handler_common
from utils import u_channel, u_config


def init(request: gr.Request):
    """ 初始化 """
    username = u_handler_common.get_username(request)
    u_config.init_config(username)
    return u_config.user_config.zip_checkbox_value


def handler(_file, zip_checkbox_value):

    # 更新配置：压缩选项
    u_config.user_config.zip_enable = ZipOption.ZIP_ENABLE.value in zip_checkbox_value
    u_config.user_config.zip_with_del = ZipOption.ZIP_WITH_DEL.value in zip_checkbox_value
    u_config.user_config.zip_checkbox_value = zip_checkbox_value
    u_config.save_config(u_config.user_config)

    # 检查文件 & 渠道
    check_result = u_handler_common.check_file(_file, ['apk']) or u_handler_common.check_channel(u_config.user_config.channel_file)
    if check_result:
        return check_result, None

    # 更新配置：待处理的apk文件
    u_config.user_config.apk_path = _file.name
    u_config.user_config.apk_name = _file.orig_name
    u_config.save_config(u_config.user_config)

    # 处理多渠道打包&签名
    error_msg, file_path_lst = u_channel.parse_channel_with_sign()
    if error_msg:
        return error_msg, None

    msg = f"处理完毕：\nzip_enable = {u_config.user_config.zip_enable}\nfile_path_lst={file_path_lst}"
    return msg, file_path_lst
