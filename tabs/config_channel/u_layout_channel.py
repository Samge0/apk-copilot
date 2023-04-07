#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-03-28 14:40
# describe：
import gradio as gr

from tabs.config_channel import u_handler_channel


def create_layout(app):
    """ 构建布局：多渠道配置 """
    with gr.Row().style(equal_height=True):
        with gr.Column():
            channel_file = gr.File(label="上传多渠道文件（暂只支持友盟，格式：渠道号#渠道别名，一行一个渠道信息）", type="file", file_types=[".txt"], interactive=True)
            button = gr.Button("保存配置")
        with gr.Column():
            txt_result = gr.Textbox(
                label="结果展示",
                placeholder="这里展示配置结果",
                lines=30,
                max_lines=30
            )
    inputs = [channel_file]
    outputs = [txt_result]
    button.click(u_handler_channel.handler, inputs=inputs, outputs=outputs)
    # 配置初始化
    app.load(u_handler_channel.init, inputs=None, outputs=[channel_file, txt_result])
