#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-03-28 14:40
# describe：
import gradio as gr

from tabs.config_channel import u_handler_channel
from utils.u_config import g_config


def create_layout(gr_config):
    """ 构建布局：工期评估 """
    with gr.Row().style(equal_height=True):
        with gr.Column():
            channel_file = gr.File(label="上传多渠道文件（暂只支持友盟）", type="file", file_types=[".txt"], value=g_config.channel_file)
            button = gr.Button("保存配置")
        with gr.Column():
            txt_result = gr.Textbox(
                label="结果展示",
                placeholder="这里展示配置结果",
                lines=12,
                interactive=True
            )
    inputs = [channel_file]
    outputs = [txt_result, gr_config]
    button.click(u_handler_channel.handler, inputs=inputs, outputs=outputs)
