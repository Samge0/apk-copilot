#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/4/19 下午6:57
# @Author  : Samge
import datetime
import time


"""
日期操作工具类，可获取指定长度时间戳、当前日期字符串、判断日期左右、重新格式化日期字符串等
"""


def get_timestamp() -> int:
    """
    获取当前时间戳
    :return:
    """
    return int(time.time())


def get_timestamp_with_size(length: int = 10) -> int:
    """
    获取当前时间戳

    :param length: 指定长度
    :return:
    """
    if length < 1:
        raise ValueError("length must > 0")
    time_str = str(time.time()).replace('.', '')
    return int(time_str[:length])


def get_today_str(f='%Y-%m-%d %H:%M:%S') -> str:
    """
    获取当天年月日字符串
    :param f:
    :return:
    """
    return time.strftime(f, time.localtime(time.time()))


def is_today_left(c_date):
    """判断日期是否在今天之前，包含今天"""
    try:
        return (datetime.datetime.strptime(c_date[:10], '%Y-%m-%d') - datetime.datetime.now()).days <= 0
    except:
        return False


def is_today_right(c_date):
    """判断日期是否在今天之后，不包含今天"""
    try:
        if not c_date:
            return False
        return (datetime.datetime.strptime(c_date[:10], '%Y-%m-%d') - datetime.datetime.now()).days > 0
    except:
        return False


def differ_days(c_date) -> int:
    """判断今天与某个日期 相差几天 """
    try:
        if not c_date:
            return -9999
        return (datetime.datetime.now() - datetime.datetime.strptime(c_date[:10], '%Y-%m-%d')).days
    except:
        return -9999


def get_curr_year() -> int:
    """获取当前年份"""
    return datetime.datetime.now().year


def convert_date_format(date_str, old_format: str, new_format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    转换日期格式

    :param date_str: 当前 old_format 所对应的日期字符串
    :param old_format: 旧的日期格式
    :param new_format: 新的日期格式
    :return:
    """
    if not date_str:
        return ''
    date_time = datetime.datetime.strptime(date_str, old_format)
    return date_time.strftime(new_format)
