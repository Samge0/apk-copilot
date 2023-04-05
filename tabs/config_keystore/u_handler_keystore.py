#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-03-28 14:43
# describe：

from tabs.common import u_handler_common
from utils import u_config


def handler(_file, key_pw, key_alias, key_alias_pw):
    """
    处理keystore文件的保存

    :param _file: keystore的文件路径
    :param key_pw: keystore的密码
    :param key_alias: keystore别名
    :param key_alias_pw: keystore别名密码
    :return:
    """

    # 检查文件
    check_result = u_handler_common.check_file(_file, ['keystore'])
    if check_result:
        return check_result

    # 检查keystore是否配置正确

    # 更新配置
    u_config.g_config.key_file = _file.name
    u_config.g_config.key_pw = _file.key_pw
    u_config.g_config.key_alias = _file.key_alias
    u_config.g_config.key_alias_pw = _file.key_alias_pw

    result = "【成功】keystore已配置"
    return result, u_config.g_config_config
