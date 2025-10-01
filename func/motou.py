import requests
from langbot_plugin.api.entities import context
from typing import Dict
import requests

# 使用get_info()函数提供模块信息
def get_info() -> Dict[str, str]:
    """
    获取模块信息
    
    Returns:
        Dict[str, str]: 包含模块信息的字典，至少包含keyword和description
    """
    return {
        "keyword": "摸头",
        "description": "获取摸头图片",
        "usage": "摸头 @好友 或者 摸头 @1001 或者 摸头"
    }

async def get_motou_image_url(qq=None):
    """获取摸头图片链接"""
    api_url = f"https://uapis.cn/api/mt?qq={qq}"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return api_url
        else:
            return "获取摸头图片失败\n输入的格式是:摸头@好友 或者摸头 1001"
    except Exception as e:
        return "发生错误喵~"

async def execute(event_context: context.EventContext, request_dict) -> str:
    """
    执行摸头功能
    
    Args:
        event_context: 事件上下文
        request_dict: 请求字典，包含args、args_text、sender_id、message等信息
        
    Returns:
        str: 包含摸头图片的Markdown格式文本或错误信息
    """
    # 从request_dict中获取参数列表
    args = request_dict.get('args', [])

    # 获取参数中的请求者QQ号
    qq_number = '1001'  # 默认值
    
    # 首先从args_text中尝试获取ID（去除@符号）
    args_text = request_dict.get('args_text', '')
    if args_text.startswith('@'):
        qq_number = args_text[1:]  # 去掉@符号
    else:
        # 如果args_text中没有@，则使用sender_id
        sender_id = request_dict.get('sender_id', '')
        if sender_id:
            qq_number = sender_id

    # 获取摸头图片链接
    motou_image_url = await get_motou_image_url(qq=qq_number)
    
    # 检查是否获取成功
    if motou_image_url.startswith("http"):
        # 成功获取到图片链接，返回Markdown格式
        return f"![摸头]({motou_image_url})"
    else:
        # 获取失败，返回错误信息
        return motou_image_url