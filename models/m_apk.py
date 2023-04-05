#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-04-04 18:11
# describe：
import enum
from typing import Optional

from pydantic import BaseModel


class ZipOption(enum.Enum):
    """ 压缩选项 """
    ZIP_ENABLE = '压缩输出'
    ZIP_WITH_DEL = '压缩后删除源文件'


class ApkOption(BaseModel):
    """ Apk操作的参数对象 """

    # 待处理apk的文件目录
    apk_path: Optional[str] = None
    # 待处理apk的实际名字
    apk_name: Optional[str] = None
    # 是否压缩
    zip_enable: Optional[bool] = False
    # 是否在压缩后删除源文件
    zip_with_del: Optional[bool] = True
    # 压缩选项选中的值
    zip_checkbox_value: Optional[list] = None

    # keystore的文件路径
    key_file: Optional[str] = None
    # keystore的密码
    key_pw: Optional[str] = None
    # keystore别名
    key_alias: Optional[str] = None
    # keystore别名密码
    key_alias_pw: Optional[str] = None

    # 渠道配置的文件路径
    channel_file: Optional[str] = None

    # 当前登录用户名
    username: Optional[str] = None

    # 认证列表
    auth: Optional[list] = None
