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
        "keyword": "天气",
        "description": "获取指定城市的实时天气和未来三天天气预报",
        "usage": "天气 <城市名称>",
        "need_at": False
    }

async def execute(event_context: context.EventContext, request_dict: Dict) -> str:
    """
    执行获取天气功能
    
    Args:
        event_context: 事件上下文
        request_dict: 包含请求信息的字典
        
    Returns:
        str: 天气信息
    """
    # 从request_dict中获取参数列表
    args = request_dict.get('args', [])
    
    # 获取天气API密钥（从request_dict中获取）
    weather_key = request_dict.get('weather_key', None)
    # 获取天气API Host（从request_dict中获取）
    weather_api_host = request_dict.get('weather_host', None)

    # 如果没有配置API密钥，提示用户在后台填写
    if not weather_key:
        return "未配置天气API密钥，请在后台插件配置中填写weather_key"

    # 如果没有配置API Host，提示用户在后台填写
    if not weather_api_host:
        return "未配置天气API Host，请在后台插件配置中填写weather_api_host（每个开发者有独立的请求地址）"
    
    # 获取城市名称，默认为"贵阳"
    city_name = args[0] if args else "贵阳"
    
    try:
        # 获取Location ID
        location_id = get_location_id(weather_key, weather_api_host, city_name)
        if not location_id:
            return f"无法获取城市'{city_name}'的位置信息，请检查城市名称是否正确"

        # 获取实时天气和未来三天天气预报
        realtime_weather = get_realtime_weather(weather_key, weather_api_host, location_id)
        forecast_weather = get_forecast_weather(weather_key, weather_api_host, location_id)
        
        # 处理天气数据并返回结果
        if realtime_weather and forecast_weather:
            result = process_weather_data(city_name, realtime_weather, forecast_weather)
            return result
        else:
            return "获取天气数据失败，请检查网络或API配置"
            
    except Exception as e:
        return f"获取天气信息时发生错误: {str(e)}"

def get_location_id(api_key, api_host, location_name):
    """
    通过GeoAPI获取城市的Location ID

    Args:
        api_key: 和风天气API密钥
        api_host: 和风天气API Host
        location_name: 城市名称

    Returns:
        str: Location ID或None（如果获取失败）
    """
    geoapi_url = f"https://{api_host}/geo/v2/city/lookup"
    params = {
        "key": api_key,
        "location": location_name
    }
    try:
        response = requests.get(geoapi_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "200" and data.get("location"):
                # 获取Location ID
                location_id = data["location"][0]["id"]
                return location_id
            else:
                print(f"GeoAPI错误：{data.get('code')}, {data.get('message')}")
        else:
            print(f"GeoAPI请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"获取Location ID时出错: {str(e)}")
    return None

def get_realtime_weather(api_key, api_host, location_id):
    """
    获取实时天气

    Args:
        api_key: 和风天气API密钥
        api_host: 和风天气API Host
        location_id: 城市的Location ID

    Returns:
        dict: 实时天气数据或None（如果获取失败）
    """
    url = f"https://{api_host}/v7/weather/now"
    params = {
        "key": api_key,
        "location": location_id
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "200":
                return data
            else:
                print(f"实时天气API错误：{data.get('code')}, {data.get('message')}")
        else:
            print(f"实时天气请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"获取实时天气时出错: {str(e)}")
    return None

def get_forecast_weather(api_key, api_host, location_id):
    """
    获取未来三天天气预报

    Args:
        api_key: 和风天气API密钥
        api_host: 和风天气API Host
        location_id: 城市的Location ID

    Returns:
        dict: 天气预报数据或None（如果获取失败）
    """
    url = f"https://{api_host}/v7/weather/3d"
    params = {
        "key": api_key,
        "location": location_id
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "200":
                return data
            else:
                print(f"天气预报API错误：{data.get('code')}, {data.get('message')}")
        else:
            print(f"天气预报请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"获取天气预报时出错: {str(e)}")
    return None

def process_weather_data(city_name, realtime_weather, forecast_weather):
    """
    处理天气数据并返回格式化的结果
    
    Args:
        city_name: 城市名称
        realtime_weather: 实时天气数据
        forecast_weather: 天气预报数据
        
    Returns:
        str: 格式化的天气信息
    """
    now = realtime_weather['now']
    
    result = []
    result.append(f"📍位置：{city_name}")
    result.append("-" * 15)
    result.append(f"实时天气：{now['text']}")
    result.append(f"当前温度：{now['temp']}℃")
    
    # 提取风向和风力信息
    wind_info = []
    if 'windDir' in now and now['windDir']:
        wind_info.append(now['windDir'])
    if 'windScale' in now and now['windScale']:
        wind_info.append(f"{now['windScale']}级")
    if wind_info:
        result.append(f"风力：{' '.join(wind_info)}")
    
    # 提取湿度信息
    if 'humidity' in now and now['humidity']:
        result.append(f"湿度：{now['humidity']}%")
    
    # 添加未来三天天气预报
    result.append("\n📅未来三天天气预报：")
    if 'daily' in forecast_weather:
        for day in forecast_weather['daily'][:3]:  # 只显示未来三天
            result.append(f"日期：{day['fxDate']}")
            result.append(f"白天：{day['textDay']}，夜间：{day['textNight']}")
            result.append(f"最高温度：{day['tempMax']}℃，最低温度：{day['tempMin']}℃")
            result.append("-")
    
    return "\n".join(result)