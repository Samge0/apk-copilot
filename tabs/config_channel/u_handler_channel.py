#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-03-28 14:43
# describe：
from tabs.common import u_handler_common
from utils import u_config


def handler(_file):
    """
    处理多渠道文件的保存

    :param _file: 多渠道配置文件
    :return:
    """
    check_result = u_handler_common.check_file(_file, ['txt'])
    if check_result:
        return check_result

    # 检查配置是否正确

    # 更新配置
    u_config.g_config.channel_file = _file.name

    result = "【成功】多渠道信息已配置"
    return result, u_config.g_config
