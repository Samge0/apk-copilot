#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-03-28 14:43
# describe：
from models.m_apk import ZipOption
from tabs.common import u_handler_common
from utils import u_channel
from utils.u_config import g_config


def handler(_file, zip_checkbox_value):

    # 更新配置：压缩选项
    g_config.zip_enable = ZipOption.ZIP_ENABLE.value in zip_checkbox_value
    g_config.zip_with_del = ZipOption.ZIP_WITH_DEL.value in zip_checkbox_value
    g_config.zip_checkbox_value = zip_checkbox_value

    # 检查文件
    check_result = u_handler_common.check_file(_file, ['apk'])
    if check_result:
        return check_result, None, g_config

    # 更新配置：待处理的apk文件
    g_config.apk_path = _file.name
    g_config.apk_name = _file.orig_name

    # 处理多渠道打包&签名
    file_path_lst = u_channel.parse_channel_with_sign()
    msg = f"处理完毕：\nzip_enable = {g_config.zip_enable}\nfile_path_lst={file_path_lst}"

    return msg, file_path_lst, g_config
