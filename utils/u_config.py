#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-04-05 20:11
# describe：
import gradio as gr

from models.m_apk import ApkOption
from utils import u_file

"""
该项目的配置工具类
"""

true = True
false = False
null = None

# 全局的gr配置
gr_config = gr.State(eval(u_file.read('config.json') or {}))

# 全局配置
g_config = ApkOption.parse_obj(gr_config.value)
