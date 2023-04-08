#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-04-05 17:23
# describe：
import os
import shutil

import gradio as gr

from utils import u_channel, u_config, u_file, u_date

true = True
false = False
null = None


def init(request: gr.Request):
    """ 初始化标题与用户信息 """
    username = get_username(request)
    u_config.init_config(username)
    return gr.Markdown.update(value=f"## Apk Copilot 多渠道打包&签名（当前登录账号：{u_config.user_config.username}）")


def get_username(request):
    """
    从gradio中获取用户名
    :param request:
    :return:
    """
    if hasattr(request, "username") and request.username:
        username = request.username
    else:
        username = ""
    return username


def check_channel(filepath: str) -> str:
    """ 检查渠道信息是否配置正确 """
    channel_dict = u_channel.get_channel_dict(filepath)
    if len(channel_dict.keys()) == 0:
        return f'渠道配置解析为空列表，请上传 "渠道号#渠道名" 这样格式的渠道配置文件，多个渠道需要换行。'
    return None


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

    if not u_file.exists(filename):
        return "【温馨提示】文件上传中，请等待文件上传完毕后再进行操作"

    return None


def copy_file_with_date(_file, save_dir: str) -> str:
    """
    复制临时文件到指定目录，并返回复制后的文件相对地址

    :param _file: gradio中的临时文件对象
    :param save_dir: 文件保存目录
    :return: 复制后的文件相对地址
    """
    # 从file中读取文件名
    filename = str(_file.orig_name or _file.name).replace(os.path.sep, '/').split('/')[-1]
    # 判断并创建多级目录
    u_file.makedirs(save_dir, need_clean=True)
    # 拼接需要保存的目标文件路径
    save_path = f'{save_dir}/{filename}'
    # 开始复制
    shutil.copy(_file.name, save_path)
    return save_path
