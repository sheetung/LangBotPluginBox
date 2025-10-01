# menu.py - 菜单功能模块

from langbot_plugin.api.entities import context
from typing import List, Dict
import os
import importlib.util
from core import feature_disabler

# 使用get_info()函数提供模块信息
def get_info() -> Dict[str, str]:
    """
    获取模块信息
    
    Returns:
        Dict[str, str]: 包含模块信息的字典，至少包含keyword和description
    """
    return {
        "keyword": "菜单",
        "description": "显示func目录中所有可用的功能命令，以及核心功能",
        "usage": "菜单 [禁用/启用/禁用列表] [功能名]",
        "example": "菜单\n菜单 禁用 功能名\n菜单 启用 功能名\n菜单 禁用列表"
    }

async def execute(event_context: context.EventContext, request_dict: Dict) -> str:
    """
    执行帮助功能，列出所有可用的功能命令
    
    Args:
        event_context: 事件上下文
        request_dict: 包含请求信息的字典
        
    Returns:
        str: 帮助信息
    """
    # 从request_dict中获取参数列表
    args = request_dict.get('args', [])
    
    # 处理功能禁用/启用命令
    if args and len(args) >= 1:
        # 处理禁用命令
        if args[0] == "禁用" and len(args) >= 2:
            feature_name = args[1]
            # 检查功能是否存在
            from core.module_loader import find_module_by_keyword
            # 临时禁用检查，以确定功能是否存在
            original_is_disabled = feature_disabler.is_disabled(feature_name)
            if original_is_disabled:
                return f"功能 '{feature_name}' 已经被禁用"
            
            module_tuple = find_module_by_keyword(feature_name)
            if module_tuple:
                # 禁用功能
                result = feature_disabler.disable_feature(feature_name)
                if result:
                    return f"已成功禁用功能 '{feature_name}'"
                else:
                    return f"禁用功能 '{feature_name}' 失败"
            else:
                return f"未找到功能 '{feature_name}'"
        
        # 处理启用命令
        elif args[0] == "启用" and len(args) >= 2:
            feature_name = args[1]
            result = feature_disabler.enable_feature(feature_name)
            if result:
                return f"已成功启用功能 '{feature_name}'"
            else:
                return f"功能 '{feature_name}' 未被禁用或不存在"
        
        # 处理查看禁用列表命令
        elif args[0] == "禁用列表":
            disabled_list = feature_disabler.get_disabled_features()
            if disabled_list:
                return f"当前被禁用的功能：\n" + "\n".join(disabled_list)
            else:
                return "没有被禁用的功能"
    
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
        # 定义排除的文件列表，方便后续添加
        excluded_files = ["__init__.py", "module_loader.py", 
                        "message_processor.py", "feature_disabler.py"]   
        if file.endswith(".py") and file not in excluded_files:
            module_name = file[:-3]  # 去掉.py后缀
            
            try:
                # 动态导入模块
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(core_dir, file))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # 获取模块的关键词和描述
                if hasattr(module, 'get_info') and callable(module.get_info):
                    try:
                        info = module.get_info()
                        if isinstance(info, dict):
                            keyword = info.get('keyword', module_name)
                            description = info.get('description', '无描述')
                        else:
                            keyword = module_name
                            description = '无描述'
                    except Exception as e:
                        keyword = module_name
                        description = f'获取信息失败 ({str(e)})'
                else:
                    keyword = module_name
                    description = '无描述'
                
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
                    if hasattr(module, 'get_info') and callable(module.get_info):
                        try:
                            info = module.get_info()
                            if isinstance(info, dict):
                                keyword = info.get('keyword', module_name)
                                description = info.get('description', '无描述')
                            else:
                                keyword = module_name
                                description = '无描述'
                        except Exception as e:
                            keyword = module_name
                            description = f'获取信息失败 ({str(e)})'
                    else:
                        keyword = module_name
                        description = '无描述'
                    
                    help_text += f"{keyword}: {description}\n"
                except Exception as e:
                    help_text += f"{module_name}: 加载失败 ({str(e)})\n"
    help_text += "\n使用 <功能> --help 查看特定功能的使用帮助"
    return help_text