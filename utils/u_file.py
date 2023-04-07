#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/4/20 下午5:35
# @Author  : Samge
import base64
import os

"""
文件操作相关工具类
"""


def save_base64(_base64: str, _path: str) -> bool:
    """保存base64到文件"""
    try:
        if exists(_path):
            return True
        filedata = base64.b64decode(_base64.replace('\n', ''))
        with open(_path, "wb") as fh:
            fh.write(filedata)
            fh.close()
        return True
    except Exception as e:
        print(f'保存base64到文件错误：{e}')
        return False


def save(_txt: str, _path: str, _type: str = 'w+') -> bool:
    """保存文件"""
    try:
        with open(_path, _type, encoding='utf-8') as f:
            f.write(_txt)
            f.flush()
            f.close()
        return True
    except:
        return False


def read(_path: str) -> str:
    """读取文件"""
    if not _path:
        return ''
    if exists(_path) is False:
        return ''
    with open(_path, "r", encoding='utf-8') as f:
        txt = f.read()
        f.close()
        return txt or ''


def size(file_path) -> float:
    """读取文件大小，单位：M"""
    if not file_path or exists(file_path) is False:
        return 0
    return os.path.getsize(file_path) / 1024 / 1024


def remove(file_path: str):
    """删除文件"""
    try:
        if not file_path:
            return
        os.remove(file_path)
    except:
        pass


def exists(filepath: str) -> bool:
    """
    判断文件路径是否存在
    :param filepath:
    :return:
    """
    return filepath and os.path.exists(filepath)

