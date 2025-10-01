# calc.py - 简单计算器功能模块

from langbot_plugin.api.entities import context
from typing import List, Dict

# 使用get_info()函数提供模块信息，替代直接定义KEYWORD和DESCRIPTION变量
def get_info() -> Dict[str, str]:
    """
    获取模块信息
    
    Returns:
        Dict[str, str]: 包含模块信息的字典，至少包含keyword和description
    """
    return {
        "keyword": "calc",
        "description": "简单计算器，支持加减乘除",
        "usage": "calc 1+2*3"
    }

async def execute(event_context: context.EventContext, request_dict) -> str:
    """
    执行计算器功能，计算简单的数学表达式
    
    Args:
        event_context: 事件上下文
        request_dict: 请求字典，包含args、args_text、sender_id、message等信息
        
    Returns:
        str: 计算结果
    """
    # 从request_dict中获取参数列表
    args = request_dict.get('args', [])
    
    if not args:
        return "请输入要计算的表达式，例如: calc 1 + 2"
    
    try:
        # 将参数列表合并为表达式字符串
        expression = " ".join(args)
        
        # 安全地计算表达式
        # 注意：这里使用eval有安全风险，实际应用中应该使用更安全的方法
        # 这里仅作为示例
        allowed_chars = set("0123456789+-*/() .")
        if not all(c in allowed_chars for c in expression):
            return "表达式包含不允许的字符，只允许数字和 +、-、*、/、(、) 运算符"
        
        result = eval(expression)
        return f"计算结果: {expression} = {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"