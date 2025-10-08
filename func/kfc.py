import requests
import json
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
        "keyword": "kfc",
        "description": "获取肯德基疯狂星期四文案",
        "usage": "kfc",
        "need_at": False
    }

async def execute(event_context: context.EventContext, request_dict: Dict) -> str:
    """
    执行获取肯德基疯狂星期四文案的功能
    
    Args:
        event_context: 事件上下文
        request_dict: 包含请求信息的字典
        
    Returns:
        str: 肯德基疯狂星期四文案
    """
    try:
        url = "https://api.ahfi.cn/api/kfcv50?type=json"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        if data and data.get("code") == 200:
            return data.get("data", {}).get("copywriting", "获取肯德基疯狂星期四文案失败")
        else:
            return f"获取肯德基疯狂星期四文案失败: {data.get('msg', '未知错误')}"
            
    except requests.exceptions.RequestException as e:
        return f"请求出错: {str(e)}"
    except json.JSONDecodeError:
        return "解析响应失败: 返回的不是有效的JSON格式"
    except Exception as e:
        return f"获取肯德基疯狂星期四文案时发生未知错误: {str(e)}"