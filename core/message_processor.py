import re
import base64
from pathlib import Path
from langbot_plugin.api.entities.builtin.platform import message as platform_message


class MessageProcessor:
    @staticmethod
    def convert_message(message, sender_id, need_at=False):
        """
        将消息文本转换为消息链对象，支持解析文本、网络图片和本地路径图片
        """
        parts = []
        last_end = 0
        has_image = False
        
        # 组合所有图片模式
        image_pattern = re.compile(
            r'!\[.*?\]\(\s*((?:https?://\S+)|(?:/home/.*?\.png))\s*\)'  # 网络图片或本地图片
        )
        
        # 处理@功能
        if need_at:
            parts.append(platform_message.At(target=sender_id))
        
        # 统一处理所有图片
        for match in image_pattern.finditer(message):
            has_image = True
            start, end = match.span()
            
            # 添加图片前的文本
            if start > last_end:
                parts.append(platform_message.Plain(text=message[last_end:start]))
            
            # 处理图片
            image_url_or_path = match.group(1)
            
            if image_url_or_path.startswith(('http://', 'https://')):
                # 网络图片
                parts.append(platform_message.Image(url=image_url_or_path))
            else:
                # 本地图片
                image_path = Path(image_url_or_path)
                if image_path.exists():
                    try:
                        with open(image_path, 'rb') as img_file:
                            img_bytes = img_file.read()
                            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                        parts.append(platform_message.Image(base64=img_base64))
                    except Exception as e:
                        parts.append(platform_message.Plain(text=f"[Error loading image: {e}]"))
                else:
                    parts.append(platform_message.Plain(text=f"[Image not found: {image_url_or_path}]"))
            
            last_end = end
        
        # 添加剩余文本
        if last_end < len(message):
            parts.append(platform_message.Plain(text=message[last_end:]))
        elif not has_image:
            # 如果没有找到任何图片，添加原始消息
            parts.append(platform_message.Plain(text=message))
        
        return parts if parts else [platform_message.Plain(text=message)]