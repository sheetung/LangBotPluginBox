# test.py - 测试功能模块

from langbot_plugin.api.entities import context
from typing import List, Dict
import os

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
        "need_at": True
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
    
    # 示例图片URL（使用网络上的公开图片）
    example_image_url = "https://static.moontung.top/2024/202405141832929.jpeg"
    
    if not args:
        # 如果没有参数，返回默认的文本和图片组合
        # 使用括号和字符串连接实现多行字符串
        return (
            f"本地图片示例：![本地图片]({os.path.join('/home/sheetung/langbot-plugin-all/LangBotPluginBox/assets', 'icon.png')})\n"
            f"这是一个测试消息，包含文本和图片：\n"
            f"网络示例图片1：![示例图片]({example_image_url})\n"
            f"文本2\n"
            f"网络示例图片2：![示例图片]({example_image_url})\n"
        )
    
    # 如果有参数，返回参数内容加上图片
    args_content = " ".join(args)
    return f"\n测试结果: {args_content}\n包含一张示例图片：![示例图片]({example_image_url})\n{args_content}\n"
