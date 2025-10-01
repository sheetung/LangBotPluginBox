# request_dict_demo.py - 使用request_dict参数的示例模块

from langbot_plugin.api.entities import context
from typing import Dict

# 使用get_info()函数提供模块信息
def get_info() -> dict:
    """
    获取模块信息
    
    Returns:
        dict: 包含模块信息的字典
    """
    return {
        "keyword": "req_demo",
        "description": "展示如何使用request_dict参数获取请求信息",
        "usage": "req_demo [任意参数]",
        "need_at": True
    }

async def execute(event_context: context.EventContext, request_dict: Dict) -> str:
    """
    执行示例功能，展示如何从request_dict中获取各种信息
    
    Args:
        event_context: 事件上下文
        request_dict: 包含请求信息的字典
        
    Returns:
        str: 包含请求信息的字符串
    """
    
    # 初始化结果消息
    result = ["request_dict参数使用示例:"]
    result.append("")
    
    # 显示request_dict中的所有键值对
    result.append("1. request_dict中的所有信息:")
    for key, value in request_dict.items():
        result.append(f"   - {key}: {value}")
    result.append("")
    
    # 演示如何从request_dict中提取常用信息
    result.append("2. 从request_dict中提取常用信息:")
    
    # 获取原始参数列表
    args = request_dict.get('args', [])
    result.append(f"   - 原始参数列表 (args): {args}")
    
    # 获取原始参数字符串
    args_text = request_dict.get('args_text', '')
    result.append(f"   - 原始参数字符串 (args_text): {args_text}")
    
    # 获取发送者ID
    sender_id = request_dict.get('sender_id', '')
    result.append(f"   - 发送者ID (sender_id): {sender_id}")
    
    # 获取完整消息内容
    message = request_dict.get('message', '')
    result.append(f"   - 完整消息内容 (message): {message}")
    result.append("")
    
    # 提供使用request_dict的代码示例
    result.append("3. 功能模块中使用request_dict的示例代码:")
    result.append("   from typing import Dict")
    result.append("")
    result.append("   async def execute(event_context, request_dict: Dict) -> str:")
    result.append("       # 获取参数列表")
    result.append("       args = request_dict.get('args', [])")
    result.append("       ")
    result.append("       # 获取发送者ID")
    result.append("       sender_id = request_dict.get('sender_id', '')")
    result.append("       ")
    result.append("       # 获取完整消息")
    result.append("       full_message = request_dict.get('message', '')")
    result.append("       ")
    result.append("       # 处理业务逻辑")
    result.append("       if args:")
    result.append("           response = f'收到参数: {args}'")
    result.append("       else:")
    result.append("           response = '未收到参数'")
    result.append("       ")
    result.append("       return response")
    result.append("")
    
    # 解释为什么使用request_dict
    result.append("4. 使用request_dict的优势:")
    result.append("   - 更灵活：可以轻松添加新的字段而不破坏现有功能")
    result.append("   - 更清晰：通过键名可以直观了解数据含义")
    result.append("   - 易于扩展：未来可以根据需要添加更多信息到request_dict中")
    result.append("   - 向后兼容：可以在request_dict中包含原有的args信息")
    
    return "\n".join(result)