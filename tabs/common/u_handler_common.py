#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-04-05 17:23
# describe：
import os

import gradio as gr

from models.m_apk import ApkOption
from utils import u_file
from utils.u_config import g_config

true = True
false = False
null = None


def init_title_with_user_info(request: gr.Request):
    """ 初始化标题与用户信息 """
    if hasattr(request, "username") and request.username:  # is not None or is not ""
        g_config.username = request.username
    else:
        g_config.username = "default_user"
    return gr.Markdown.update(value=f"## Apk Copilot 多渠道打包&签名（当前登录账号：{g_config.username}）")


def check_file(file_obj, suffix_lst: list) -> str:
    """
    检查文件是否符合要求
    :param file_obj:
    :param suffix_lst:
    :return:
    """
    suffix_str = '、'.join(suffix_lst)
    if not file_obj:
        return f"【温馨提示】请上传后缀为 {suffix_str} 的文件"

    filename = file_obj.name or ''
    filename_suffix = filename.split('.')[-1]
    if filename_suffix not in suffix_lst:
        return f"【温馨提示】请上传后缀为 {suffix_str} 的文件"

    if not os.path.exists(filename):
        return "【温馨提示】文件上传中，请等待文件上传完毕后再进行操作"

    return None


def handler_reload_config():
    """
    重新加载配置，当前方法还需调整 TODO
    :return:
    """

    # 全局的gr配置
    _gr_config = gr.State(eval(u_file.read('config.json') or {}))
    # 全局配置
    _g_config = ApkOption.parse_obj(_gr_config.value)
    return _g_config.zip_checkbox_value, _g_config
