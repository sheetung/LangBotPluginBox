# echo.py - 回显功能模块

from langbot_plugin.api.entities import context
from typing import List

# 功能描述和触发关键词
KEYWORD = "测试"
DESCRIPTION = "测试功能，回显用户输入的内容"

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
