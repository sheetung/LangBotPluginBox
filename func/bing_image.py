from langbot_plugin.api.entities import context
from typing import List, Dict
import requests

# 使用get_info()函数提供模块信息
def get_info() -> Dict[str, str]:
    """
    获取模块信息
    
    Returns:
        Dict[str, str]: 包含模块信息的字典，至少包含keyword和description
    """
    return {
        "keyword": "bing",
        "description": "获取Bing每日图片",
        "usage": "bing [day] [size]",
        "example": "bing\nbing 0 1920×1080\nbing 1"
    }

async def execute(event_context: context.EventContext, args: List[str]) -> str:
    """
    执行Bing图片获取功能
    
    Args:
        event_context: 事件上下文
        args: 参数列表，可选参数：
              - day: 表示获取哪一天的图片，0表示今天，1表示昨天，最多支持7天
              - size: 表示图片大小，如1920×1080
    
    Returns:
        str: 包含图片链接的消息
    """
    # 解析参数
    day = 0  # 默认获取今天的图片
    size = None  # 默认使用API返回的大小
    
    if len(args) >= 1:
        try:
            day = int(args[0])
            # 限制day的取值范围为0-7
            if day < 0:
                day = 0
            elif day > 7:
                day = 7
        except ValueError:
            pass
        
        if len(args) >= 2:
            size = args[1]
    
    # 获取Bing图片URL
    image_url = get_bing_image_url(day, size)
    
    if image_url:
        # 返回Markdown格式的图片链接
        return f"今日Bing图片：\n![Bing Image]({image_url})"
    else:
        return "获取Bing图片失败，请稍后再试"

def get_bing_image_url(day=0, size=None):
    """
    获取Bing图片的URL
    
    Args:
        day: 表示获取哪一天的图片，0表示今天，1表示昨天
        size: 表示图片大小，如1920×1080
    
    Returns:
        str: 图片的URL，如果获取失败则返回None
    """
    api_url = "https://uapis.cn/api/bing"
    params = {
        "rand": "false",  # 确保获取的图片是确定的
        "day": day
    }
    
    if size:
        params["size"] = size

    try:
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            # 直接使用该URL链接的图片
            return response.url
        else:
            print(f"获取Bing图片失败，状态码：{response.status_code}")
            return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None