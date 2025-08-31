# test.py - 测试功能模块

from langbot_plugin.api.entities import context
from typing import List, Dict

# 使用get_info()函数提供模块信息
def get_info() -> Dict[str, str]:
    """
    获取模块信息
    
    Returns:
        Dict[str, str]: 包含模块信息的字典，至少包含keyword和description
    """
    return {
        "keyword": "测试",
        "description": "测试功能，回显用户输入的内容",
        "usage": "测试 内容",
        "example": "测试 Hello World"
    }

async def execute(event_context: context.EventContext, args: List[str]) -> str:
    """
    执行测试功能，将用户输入的内容返回
    
    Args:
        event_context: 事件上下文
        args: 参数列表
        
    Returns:
        str: 回显的内容
    """

    print(f'test args: {args}')
    if not args:
        return "请在测试后面输入要回显的内容"
    
    return "测试结果: " + " ".join(args)
