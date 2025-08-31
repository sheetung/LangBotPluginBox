from __future__ import annotations

from langbot_plugin.api.definition.components.common.event_listener import EventListener
from langbot_plugin.api.entities import events, context
from langbot_plugin.api.entities.builtin.platform import message as platform_message
from langbot_plugin.api.entities.builtin.provider import message as provider_message

import os
import importlib.util
import sys
import re

# 导入模块加载器
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core import module_loader


class DefaultEventListener(EventListener):

    async def initialize(self):
        await super().initialize()
        
        @self.handler(events.PersonMessageReceived)
        @self.handler(events.GroupMessageReceived)
        async def handler(event_context: context.EventContext):
            # 获取消息内容
            try:
                # 根据其他插件的实现，正确获取消息内容
                message_chain = event_context.event.message_chain
                message = "".join(
                    element.text for element in message_chain
                    if isinstance(element, platform_message.Plain)
                ).strip()
                
                if not message:
                    await event_context.reply(
                        platform_message.MessageChain([
                            platform_message.Plain(text=f"请输入有效的消息内容"),
                        ])
                    )
                    return
            except Exception as e:
                print(f"获取消息内容时出错: {str(e)}")
                await event_context.reply(
                    platform_message.MessageChain([
                        platform_message.Plain(text=f"获取消息内容时出错: {str(e)}"),
                    ])
                )
                return
            
            # 分割消息，获取关键词和参数
            # 首先获取所有可用的关键词
            available_keywords = module_loader.get_available_keywords()
            
            # 获取项目根目录
            base_dir = module_loader.get_base_dir()
            
            # 获取目录路径
            core_dir = os.path.join(base_dir, 'core')
            func_dir = os.path.join(base_dir, 'func')
            
            # 尝试匹配关键词
            keyword = None
            args_text = ""
            
            for kw in available_keywords:
                # 对于中文和英文都进行不区分大小写的匹配
                if message.lower().startswith(kw.lower()) or message.startswith(kw):
                    keyword = kw
                    args_text = message[len(kw):].strip()
                    break
            
            # 如果没有匹配到关键词，尝试使用空格分割
            if keyword is None:
                words = message.strip().split()
                if not words:
                    await event_context.reply(
                        platform_message.MessageChain([
                            platform_message.Plain(text=f"请输入有效的消息内容"),
                        ])
                    )
                    return
                
                keyword = words[0]
                args_text = message[len(keyword):].strip()
            
            # 将参数文本分割为参数列表
            args = args_text.split() if args_text else []
            
            # 查找对应的功能模块文件
            module_tuple = module_loader.find_module_by_keyword(keyword)
            
            # 如果没有找到对应的模块，返回错误信息
            if module_tuple is None:
                # await event_context.reply(
                #     platform_message.MessageChain([
                #         platform_message.Plain(text=f"未找到关键词 '{keyword}' 对应的功能"),
                #     ])
                # )
                return
            
            module_file, module_type = module_tuple
                
            # 动态导入对应的功能模块
            module = module_loader.load_module(module_file, keyword)
            if module is None:
                await event_context.reply(
                    platform_message.MessageChain([
                        platform_message.Plain(text=f"加载模块 {keyword} 失败"),
                    ])
                )
                return
            
            try:
                # 调用模块中的execute函数
                if hasattr(module, 'execute'):
                    result = await module.execute(event_context, args)
                    await event_context.reply(
                        platform_message.MessageChain([
                            platform_message.Plain(text=result),
                        ])
                    )
                else:
                    await event_context.reply(
                        platform_message.MessageChain([
                            platform_message.Plain(text=f"模块 {keyword} 中没有找到execute函数"),
                        ])
                    )
            except Exception as e:
                await event_context.reply(
                    platform_message.MessageChain([
                        platform_message.Plain(text=f"执行功能时出错: {str(e)}"),
                    ])
                )