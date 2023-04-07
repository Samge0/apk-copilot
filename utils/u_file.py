#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/4/20 下午5:35
# @Author  : Samge
import base64
import os
import shutil
import threading

"""
文件操作相关工具类
"""

# 创建一个线程锁
lock = threading.Lock()


def save_base64(_base64: str, _path: str) -> bool:
    """保存base64到文件"""
    lock.acquire()  # 获取线程锁
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
    finally:
        lock.release()  # 释放线程锁


def save(_txt: str, _path: str, _type: str = 'w+') -> bool:
    """保存文件"""
    lock.acquire()  # 获取线程锁
    try:
        with open(_path, _type, encoding='utf-8') as f:
            f.write(_txt)
            f.flush()
            f.close()
        return True
    except:
        return False
    finally:
        lock.release()  # 释放线程锁


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


def remove(_path: str):
    """删除文件"""
    try:
        if not exists(_path):
            return
        os.remove(_path)
    except:
        pass


def remove_dir_all_file(_path: str):
    """删除文件夹一级所有文件"""
    try:
        files = os.listdir(_path)
        for file in files:
            file_path = os.path.join(_path, file)
            remove(file_path)
    except:
        pass


def remove_dir(_path: str):
    """删除该文件夹及里面所有子文件"""
    try:
        if not exists(_path) or not os.path.isdir(_path):
            return
        shutil.rmtree(_path)
    except:
        pass


def makedirs(_path: str, need_clean: bool = False):
    """
    创建多层级目录，如果已存在则跳过
    :param _path: 需要创建的文件夹路径
    :param need_clean: 是否需要清空文件夹
    :return:
    """
    if need_clean:
        remove_dir(_path)
    if not exists(_path):
        os.makedirs(_path)


def exists(filepath: str) -> bool:
    """
    判断文件路径是否存在
    :param filepath:
    :return:
    """
    return filepath and os.path.exists(filepath)

