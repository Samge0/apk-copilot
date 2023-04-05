#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-03-28 14:40
# describe：
import gradio as gr

from tabs.config_keystore import u_handler_keystore
from utils.u_config import g_config


def create_layout(gr_config):
    """ 构建布局：工期评估 """
    with gr.Row().style(equal_height=True):
        with gr.Column():
            key_file = gr.File(label="上传keystore文件", type="file", file_types=[".keystore"], value=g_config.key_file)
            with gr.Row().style(equal_height=True):
                key_pw = gr.Textbox(label="key密码", lines=1, value=g_config.key_pw)
                key_alias = gr.Textbox(label="key别名", lines=1, value=g_config.key_alias)
                key_alias_pw = gr.Textbox(label="key别名密码", lines=1, value=g_config.key_alias_pw)
            button = gr.Button("保存配置")
        with gr.Column():
            txt_result = gr.Textbox(
                label="结果展示",
                placeholder="这里展示keystore配置结果",
                lines=12,
                interactive=True
            )
    inputs = [key_file, key_pw, key_alias, key_alias_pw]
    outputs = [txt_result, gr_config]
    button.click(u_handler_keystore.handler, inputs=inputs, outputs=outputs)
