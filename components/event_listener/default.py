from __future__ import annotations

from langbot_plugin.api.definition.components.common.event_listener import EventListener
from langbot_plugin.api.entities import events, context
from langbot_plugin.api.entities.builtin.platform import message as platform_message
from langbot_plugin.api.entities.builtin.provider import message as provider_message

import os
import importlib.util
import sys
import re


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
            available_keywords = []
            
            # 获取项目根目录
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            
            # 获取core目录中的关键词
            core_dir = os.path.join(base_dir, 'core')
            if os.path.exists(core_dir):
                for file in os.listdir(core_dir):
                    if file.endswith(".py") and file != "__init__.py":
                        try:
                            # 动态导入模块以获取KEYWORD
                            module_name = file[:-3]
                            spec = importlib.util.spec_from_file_location(module_name, os.path.join(core_dir, file))
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            if hasattr(module, 'KEYWORD'):
                                available_keywords.append(module.KEYWORD)
                            else:
                                available_keywords.append(module_name)
                        except Exception as e:
                            available_keywords.append(file[:-3])
                            print(f"Error loading keyword from {file}: {e}")
            
            # 获取func目录中的关键词
            func_dir = os.path.join(base_dir, 'func')
            if os.path.exists(func_dir):
                for file in os.listdir(func_dir):
                    if file.endswith(".py") and file != "__init__.py":
                        try:
                            # 动态导入模块以获取KEYWORD
                            module_name = file[:-3]
                            spec = importlib.util.spec_from_file_location(module_name, os.path.join(func_dir, file))
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            if hasattr(module, 'KEYWORD'):
                                available_keywords.append(module.KEYWORD)
                            else:
                                available_keywords.append(module_name)
                        except Exception as e:
                            available_keywords.append(file[:-3])
                            print(f"Error loading keyword from {file}: {e}")
            
            # 按长度降序排序关键词，以便优先匹配较长的关键词
            available_keywords.sort(key=len, reverse=True)
            
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
            module_file = None
            
            # 优先在core目录中查找
            if os.path.exists(core_dir):
                for file in os.listdir(core_dir):
                    if file.endswith(".py") and file != "__init__.py":
                        try:
                            # 动态导入模块以检查KEYWORD
                            module_name = file[:-3]
                            spec = importlib.util.spec_from_file_location(module_name, os.path.join(core_dir, file))
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            if hasattr(module, 'KEYWORD') and module.KEYWORD == keyword:
                                module_file = os.path.join(core_dir, file)
                                break
                        except Exception as e:
                            print(f"Error checking module {file}: {e}")
            
            # 如果在core目录中没有找到，则在func目录中查找
            if module_file is None and os.path.exists(func_dir):
                for file in os.listdir(func_dir):
                    if file.endswith(".py") and file != "__init__.py":
                        try:
                            # 动态导入模块以检查KEYWORD
                            module_name = file[:-3]
                            spec = importlib.util.spec_from_file_location(module_name, os.path.join(func_dir, file))
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            if hasattr(module, 'KEYWORD') and module.KEYWORD == keyword:
                                module_file = os.path.join(func_dir, file)
                                break
                        except Exception as e:
                            print(f"Error checking module {file}: {e}")
            
            # 如果仍然没有找到，尝试使用文件名作为关键词
            if module_file is None:
                core_file = os.path.join(core_dir, f"{keyword}.py")
                func_file = os.path.join(func_dir, f"{keyword}.py")
                
                if os.path.exists(core_file):
                    module_file = core_file
                elif os.path.exists(func_file):
                    module_file = func_file
            
            # 如果没有找到对应的模块，返回错误信息
            if module_file is None:
                await event_context.reply(
                    platform_message.MessageChain([
                        platform_message.Plain(text=f"未找到关键词 '{keyword}' 对应的功能"),
                    ])
                )
                return
                
            # 动态导入对应的功能模块
            try:
                spec = importlib.util.spec_from_file_location(keyword, module_file)
                module = importlib.util.module_from_spec(spec)
                sys.modules[keyword] = module
                spec.loader.exec_module(module)
                
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