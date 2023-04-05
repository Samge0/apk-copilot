#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# author：samge
# data：2023-04-04 17:50
# describe：
import gradio as gr

from tabs.common import u_handler_common
from tabs.config_channel import u_layout_channel
from tabs.config_keystore import u_layout_keystore
from tabs.home import u_layout_home
from utils.u_config import g_config

"""
gradio界面
参考：https://blog.csdn.net/LuohenYJ/article/details/127489768
官方文档：https://github.com/gradio-app/gradio
"""


with gr.Blocks() as app:
    gr_config = gr.State({})
    app_title = gr.Markdown(value="", elem_id="app_title")
    with gr.Tab("首页"):
        u_layout_home.create_layout(gr_config)
    with gr.Tab("签名配置"):
        u_layout_keystore.create_layout(gr_config)
    with gr.Tab("渠道配置"):
        u_layout_channel.create_layout(gr_config)
    app.load(u_handler_common.init_title_with_user_info, inputs=None, outputs=[app_title])


app.launch(
    share=False,
    inbrowser=False,
    debug=True,
    auth=g_config.auth,
    server_name="0.0.0.0",
)
