#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-03-28 14:40
# describe：
import gradio as gr

from tabs.config_keystore import u_handler_keystore


def create_layout(app):
    """ 构建布局：秘钥配置 """
    with gr.Row().style(equal_height=True):
        with gr.Column():
            key_file = gr.File(label="上传keystore文件", type="file", file_types=[".keystore", ".jks"], interactive=True)
            with gr.Row().style(equal_height=True):
                key_pw = gr.Textbox(label="秘钥密码", lines=1, type="password", interactive=True)
                key_alias = gr.Textbox(label="秘钥别名", lines=1, interactive=True)
                key_store_pw = gr.Textbox(label="密钥库密码", lines=1, type="password", interactive=True)
            button = gr.Button("保存配置")
        with gr.Column():
            txt_result = gr.Textbox(
                label="结果展示",
                placeholder="这里展示keystore配置结果",
                lines=30,
                max_lines=30,
            )
    inputs = [key_file, key_pw, key_alias, key_store_pw]
    outputs = [txt_result]
    button.click(u_handler_keystore.handler, inputs=inputs, outputs=outputs)
    # 配置初始化
    app.load(u_handler_keystore.init, inputs=None, outputs=[key_file, key_pw, key_alias, key_store_pw, txt_result])
