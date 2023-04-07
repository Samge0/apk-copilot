#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-03-28 14:40
# describe：
import gradio as gr

from models.m_apk import ZipOption
from tabs.home import u_handler_home
from utils import u_config


def create_layout(app):
    """ 构建布局：首页-多渠道打包+签名操作 """
    zip_option_lst = [item.value for item in ZipOption]
    with gr.Row().style(equal_height=True):
        with gr.Column():
            zip_checkbox_value = gr.Checkboxgroup(label="压缩选项", choices=zip_option_lst, value=u_config.user_config.zip_checkbox_value)
            apk_file = gr.File(label="上传已加固的Apk文件", type="file", file_types=[".apk"], value=u_config.user_config.apk_path)
            button = gr.Button("开始签名")
        with gr.Column():
            txt_result = gr.Textbox(
                label="结果展示",
                placeholder="这里展示签名结果",
                lines=15,
                max_lines=15,
            )
            download_file = gr.Files(label="已签名的多渠道Apk文件", file_count="multiple")
    inputs = [apk_file, zip_checkbox_value]
    outputs = [txt_result, download_file]
    button.click(u_handler_home.handler, inputs=inputs, outputs=outputs)
    # 配置初始化
    app.load(u_handler_home.init, inputs=None, outputs=[zip_checkbox_value])
