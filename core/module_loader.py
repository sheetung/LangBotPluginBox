# module_loader.py - 模块加载器

import os
import importlib.util
import sys
from typing import List, Dict, Tuple, Optional, Any
from core import feature_disabler


def get_base_dir() -> str:
    """
    获取项目根目录
    """
    # 获取当前文件所在目录的上一级目录（即项目根目录）
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_module_keyword(module) -> str:
    """
    获取模块的关键词
    仅支持通过定义get_info()函数返回包含keyword的字典
    """
    if hasattr(module, 'get_info') and callable(module.get_info):
        try:
            info = module.get_info()
            if isinstance(info, dict) and 'keyword' in info:
                return info['keyword']
        except Exception as e:
            print(f"Error calling get_info(): {e}")
    
    return None


def get_module_description(module) -> str:
    """
    获取模块的描述
    仅支持通过定义get_info()函数返回包含description的字典
    """
    if hasattr(module, 'get_info') and callable(module.get_info):
        try:
            info = module.get_info()
            if isinstance(info, dict) and 'description' in info:
                return info['description']
        except Exception as e:
            print(f"Error calling get_info(): {e}")
    
    return "无描述"


def get_available_keywords() -> List[str]:
    """
    获取所有可用的关键词
    仅返回实现了get_info()函数的模块的关键词，排除module_loader自身
    """
    available_keywords = []
    
    # 获取项目根目录
    base_dir = get_base_dir()
    
    # 获取core目录中的关键词
    core_dir = os.path.join(base_dir, 'core')
    if os.path.exists(core_dir):
        for file in os.listdir(core_dir):
            # 跳过__init__.py和module_loader.py自身
            if file.endswith(".py") and file != "__init__.py" and file != "module_loader.py":
                try:
                    # 动态导入模块
                    module_name = file[:-3]
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(core_dir, file))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # 检查是否实现了get_info()函数
                    if hasattr(module, 'get_info') and callable(module.get_info):
                        # 获取关键词
                        keyword = get_module_keyword(module)
                        if keyword:
                            available_keywords.append(keyword)
                except Exception as e:
                    print(f"Error loading keyword from {file}: {e}")
    
    # 获取func目录中的关键词
    func_dir = os.path.join(base_dir, 'func')
    if os.path.exists(func_dir):
        for file in os.listdir(func_dir):
            if file.endswith(".py") and file != "__init__.py":
                try:
                    # 动态导入模块
                    module_name = file[:-3]
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(func_dir, file))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # 检查是否实现了get_info()函数
                    if hasattr(module, 'get_info') and callable(module.get_info):
                        # 获取关键词
                        keyword = get_module_keyword(module)
                        if keyword:
                            available_keywords.append(keyword)
                except Exception as e:
                    print(f"Error loading keyword from {file}: {e}")
    
    # 按长度降序排序关键词，以便优先匹配较长的关键词
    available_keywords.sort(key=len, reverse=True)
    return available_keywords


def get_module_info() -> Dict[str, Dict[str, str]]:
    """
    获取所有模块的信息，包括关键词和描述
    仅处理实现了get_info()函数的模块，排除module_loader自身
    返回格式：{keyword: {"description": description, "type": "core|func"}}
    """
    module_info = {}
    
    # 获取项目根目录
    base_dir = get_base_dir()
    
    # 获取core目录中的模块信息
    core_dir = os.path.join(base_dir, 'core')
    if os.path.exists(core_dir):
        for file in os.listdir(core_dir):
            # 跳过__init__.py和module_loader.py自身
            if file.endswith(".py") and file != "__init__.py" and file != "module_loader.py":
                try:
                    # 动态导入模块
                    module_name = file[:-3]
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(core_dir, file))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # 检查是否实现了get_info()函数
                    if hasattr(module, 'get_info') and callable(module.get_info):
                        # 获取关键词和描述
                        keyword = get_module_keyword(module)
                        if not keyword:
                            keyword = module_name
                        
                        description = get_module_description(module)
                        
                        # 获取额外信息
                        extra_info = {}
                        try:
                            info = module.get_info()
                            if isinstance(info, dict):
                                # 移除已处理的关键词和描述
                                info_copy = info.copy()
                                info_copy.pop('keyword', None)
                                info_copy.pop('description', None)
                                extra_info = info_copy
                        except Exception as e:
                            print(f"Error getting extra info from {file}: {e}")
                        
                        module_info[keyword] = {
                            "description": description,
                            "type": "core",
                            **extra_info
                        }
                except Exception as e:
                    print(f"Error loading module info from {file}: {e}")
    
    # 获取func目录中的模块信息
    func_dir = os.path.join(base_dir, 'func')
    if os.path.exists(func_dir):
        for file in os.listdir(func_dir):
            if file.endswith(".py") and file != "__init__.py":
                try:
                    # 动态导入模块
                    module_name = file[:-3]
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(func_dir, file))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # 检查是否实现了get_info()函数
                    if hasattr(module, 'get_info') and callable(module.get_info):
                        # 获取关键词和描述
                        keyword = get_module_keyword(module)
                        if not keyword:
                            keyword = module_name
                        
                        description = get_module_description(module)
                        
                        # 获取额外信息
                        extra_info = {}
                        try:
                            info = module.get_info()
                            if isinstance(info, dict):
                                # 移除已处理的关键词和描述
                                info_copy = info.copy()
                                info_copy.pop('keyword', None)
                                info_copy.pop('description', None)
                                extra_info = info_copy
                        except Exception as e:
                            print(f"Error getting extra info from {file}: {e}")
                        
                        module_info[keyword] = {
                            "description": description,
                            "type": "func",
                            **extra_info
                        }
                except Exception as e:
                    print(f"Error loading module info from {file}: {e}")
    
    return module_info


def find_module_by_keyword(keyword: str, admin_id: str = None, sender_id: str = None) -> Optional[Tuple[str, str]]:
    """
    根据关键词查找对应的模块文件
    仅考虑实现了get_info()函数的模块，排除module_loader自身
    返回格式：(module_file, module_type) 或 None
    """
    # 首先检查功能是否被禁用
    if feature_disabler.is_disabled(keyword):
        print(f"功能 {keyword} 已被禁用")
        return 'feature_disabler'
        
    # 获取项目根目录
    base_dir = get_base_dir()
    core_dir = os.path.join(base_dir, 'core')
    func_dir = os.path.join(base_dir, 'func')
    
    module_file = None
    module_type = None
    
    # 优先在core目录中查找
    if os.path.exists(core_dir):
        for file in os.listdir(core_dir):
            # 跳过__init__.py和module_loader.py自身
            if file.endswith(".py") and file != "__init__.py" and file != "module_loader.py":
                try:
                    # 动态导入模块
                    module_name = file[:-3]
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(core_dir, file))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # 检查是否实现了get_info()函数
                    if hasattr(module, 'get_info') and callable(module.get_info):
                        # 检查关键词是否匹配
                        module_keyword = get_module_keyword(module)
                        if not module_keyword:
                            module_keyword = module_name
                            
                        if module_keyword == keyword:
                            module_file = os.path.join(core_dir, file)
                            module_type = "core"
                            break
                except Exception as e:
                    print(f"Error checking module {file}: {e}")
    
    # 如果在core目录中没有找到，则在func目录中查找
    if module_file is None and os.path.exists(func_dir):
        for file in os.listdir(func_dir):
            if file.endswith(".py") and file != "__init__.py":
                try:
                    # 动态导入模块
                    module_name = file[:-3]
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(func_dir, file))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # 检查是否实现了get_info()函数
                    if hasattr(module, 'get_info') and callable(module.get_info):
                        # 检查关键词是否匹配
                        module_keyword = get_module_keyword(module)
                        if not module_keyword:
                            module_keyword = module_name
                            
                        if module_keyword == keyword:
                            module_file = os.path.join(func_dir, file)
                            module_type = "func"
                            break
                except Exception as e:
                    print(f"Error checking module {file}: {e}")
    
    # 不再尝试使用文件名作为关键词的方式查找，因为没有get_info()函数的模块不被视为功能脚本
    if module_file is None:
        return None
    
    return (module_file, module_type)


def load_module(module_file: str, keyword: str):
    """
    动态加载模块
    """
    try:
        spec = importlib.util.spec_from_file_location(keyword, module_file)
        module = importlib.util.module_from_spec(spec)
        sys.modules[keyword] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Error loading module {module_file}: {e}")
        return None


async def execute(event_context, args: List[str]) -> str:
    """
    执行模块加载器功能
    """
    if not args:
        return "模块加载器：请提供要执行的操作，如 list, info, load"
    
    operation = args[0]
    
    if operation == "list":
        keywords = get_available_keywords()
        return "可用的关键词：\n" + "\n".join(keywords)
    
    elif operation == "info":
        module_info = get_module_info()
        result = "模块信息：\n"
        for keyword, info in module_info.items():
            result += f"{keyword} ({info['type']}): {info['description']}\n"
        return result
    
    elif operation == "load" and len(args) > 1:
        keyword = args[1]
        module_tuple = find_module_by_keyword(keyword)
        if module_tuple:
            module_file, module_type = module_tuple
            module = load_module(module_file, keyword)
            if module:
                return f"成功加载模块 {keyword} (类型: {module_type})"
            else:
                return f"加载模块 {keyword} 失败"
        else:
            return f"未找到关键词 '{keyword}' 对应的模块"
    
    return "未知操作，可用操作：list, info, load <keyword>"