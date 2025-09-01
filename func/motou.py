import requests
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
        "keyword": "摸头",
        "description": "获取摸头图片",
        "usage": "摸头 [QQ号]  # 如 摸头 1001 获取指定QQ号的摸头图片"
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

async def execute(event_context: context.EventContext, args: List[str]) -> str:
    """
    执行摸头功能
    
    Args:
        event_context: 事件上下文
        args: 参数列表
        
    Returns:
        str: 包含摸头图片的Markdown格式文本或错误信息
    """
    # 默认使用10001作为QQ号
    qq_number = "10001"
    
    # 检查是否有参数传入
    if args:
        # 从参数中获取QQ号
        qq_number = args[0]
    
    # 获取摸头图片链接
    motou_image_url = await get_motou_image_url(qq=qq_number)
    
    # 检查是否获取成功
    if motou_image_url.startswith("http"):
        # 成功获取到图片链接，返回Markdown格式
        return f"![摸头]({motou_image_url})"
    else:
        # 获取失败，返回错误信息
        return motou_image_url