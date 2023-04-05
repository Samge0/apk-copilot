#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-03-28 14:40
# describe：
import gradio as gr

from models.m_apk import ZipOption
from tabs.common import u_handler_common
from tabs.home import u_handler_home
from utils.u_config import g_config


def create_layout(gr_config):
    """ 构建布局：工期评估 """
    zip_option_lst = [item.value for item in ZipOption]
    with gr.Row().style(equal_height=True):
        with gr.Column():
            apk_file = gr.File(label="上传已加固的Apk文件", type="file", file_types=[".apk"], value=g_config.apk_path)
            zip_checkbox_value = gr.Checkboxgroup(label="压缩选项", choices=zip_option_lst, value=g_config.zip_checkbox_value)
            button = gr.Button("开始签名")
            button_reload = gr.Button("重新加载配置")
        with gr.Column():
            txt_result = gr.Textbox(
                label="结果展示",
                placeholder="这里展示签名结果",
                lines=12,
                interactive=True
            )
            download_file = gr.Files(label="已签名的多渠道Apk文件", file_count="multiple")
    inputs = [apk_file, zip_checkbox_value]
    outputs = [txt_result, download_file, gr_config]
    button.click(u_handler_home.handler, inputs=inputs, outputs=outputs)
    button_reload.click(u_handler_common.handler_reload_config, outputs=[zip_checkbox_value, gr_config])
