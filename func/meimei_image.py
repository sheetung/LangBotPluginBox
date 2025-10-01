import httpx
import asyncio
import re  # 用于提取数字
from langbot_plugin.api.entities import context
from typing import Dict
import httpx

# 使用get_info()函数提供模块信息
def get_info() -> Dict[str, str]:
    """
    获取模块信息
    
    Returns:
        Dict[str, str]: 包含模块信息的字典，至少包含keyword和description
    """
    return {
        "keyword": "看妹妹",
        "description": "获取随机图片，支持指定获取数量",
        "usage": "看妹妹 [数量]  # 如 看妹妹 3 获取3张图片，最多10张"
    }

async def fetch_color_image(max_retries=3):
    """获取图片链接（带重试机制）"""
    api_url = "https://3650000.xyz/api/?type=json&mode=1,3,5,8"
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(api_url)
                if response.status_code == 200:
                    response_data = response.json()
                    if response_data.get("code") == 200:
                        return response_data.get("url")
                    else:
                        error_msg = f"API异常 code={response_data.get('code')} [尝试 {attempt+1}/{max_retries}]"
                else:
                    error_msg = f"状态码错误 {response.status_code} [尝试 {attempt+1}/{max_retries}]"
        except httpx.RequestError:
            error_msg = f"网络错误 [尝试 {attempt+1}/{max_retries}]"
        except Exception as e:
            error_msg = f"未知错误 {str(e)} [尝试 {attempt+1}/{max_retries}]"
        
        if attempt == max_retries - 1:
            return error_msg
        await asyncio.sleep(1)

async def execute(event_context: context.EventContext, request_dict) -> str:
    """
    执行获取随机图片功能
    
    Args:
        event_context: 事件上下文
        request_dict: 请求字典，包含args、args_text、sender_id、message等信息
        
    Returns:
        str: 包含图片链接的Markdown格式文本
    """
    # 从request_dict中获取参数列表
    args = request_dict.get('args', [])
    
    ssnum = 10  # 最大图片数量限制
    n = 1  # 默认获取1张图片
    # 解析请求次数参数（支持 x10、10次 等格式）
    if args:
        # 使用正则提取参数中的数字
        num_match = re.findall(r'\d+', args[0])
        if num_match:
            n = int(''.join(num_match))  # 合并连续数字
        else:
            n = 1  # 参数无效时使用默认值
    
    # 限制最大图片数量
    request_count = max(1, min(n, ssnum))
    
    # 并发请求
    tasks = [fetch_color_image() for _ in range(request_count)]
    results = await asyncio.gather(*tasks)
    
    # 构建结果
    response_lines = []
    
    if n > ssnum:
        response_lines.append(f'大人您看了{n}下，但是不行哦，只能看{ssnum}下')
        response_lines.append('')
    
    # 添加图片链接
    for i, result in enumerate(results, 1):
        if result and result.startswith('http'):
            response_lines.append(f"![随机图片{i}]({result})")
        else:
            response_lines.append(f"[失败] 第{i}次获取图片: {result}")
        
        # 多张图片时添加分隔符
        if request_count > 1 and i < request_count:
            response_lines.append('---')
    
    return '\n'.join(response_lines)