# help.py - 帮助功能模块

from langbot_plugin.api.entities import context
from typing import List
import os
import importlib.util

# 功能描述和触发关键词
KEYWORD = "菜单"
DESCRIPTION = "显示func目录中所有可用的功能命令，以及核心功能"

async def execute(event_context: context.EventContext, args: List[str]) -> str:
    """
    执行帮助功能，列出所有可用的功能命令
    
    Args:
        event_context: 事件上下文
        args: 参数列表
        
    Returns:
        str: 帮助信息
    """
    # 获取项目根目录
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    # 获取func目录路径
    func_dir = os.path.join(base_dir, 'func')
    
    # 获取所有功能模块
    help_text = "可用的功能命令:\n\n"
    
    # 添加核心功能模块
    help_text += "核心功能:\n"
    core_dir = os.path.dirname(__file__)
    for file in os.listdir(core_dir):
        if file.endswith(".py") and file != "__init__.py":
            module_name = file[:-3]  # 去掉.py后缀
            
            try:
                # 动态导入模块
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(core_dir, file))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # 获取模块的关键词和描述
                keyword = getattr(module, "KEYWORD", module_name)
                description = getattr(module, "DESCRIPTION", "无描述")
                
                help_text += f"{keyword}: {description}\n"
            except Exception as e:
                help_text += f"{module_name}: 加载失败 ({str(e)})\n"
    
    # 添加普通功能模块
    help_text += "\n普通功能:\n"
    if os.path.exists(func_dir):
        for file in os.listdir(func_dir):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]  # 去掉.py后缀
                
                try:
                    # 动态导入模块
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(func_dir, file))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # 获取模块的关键词和描述
                    keyword = getattr(module, "KEYWORD", module_name)
                    description = getattr(module, "DESCRIPTION", "无描述")
                    
                    help_text += f"{keyword}: {description}\n"
                except Exception as e:
                    help_text += f"{module_name}: 加载失败 ({str(e)})\n"
    
    return help_text