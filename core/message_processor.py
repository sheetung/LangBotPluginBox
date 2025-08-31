import re
import base64
from pathlib import Path
from langbot_plugin.api.entities.builtin.platform import message as platform_message


class MessageProcessor:
    @staticmethod
    def convert_message(message, sender_id, need_at=False):
        """
        将消息文本转换为消息链对象，支持解析文本、网络图片和本地路径图片

        Args:
            message (str): 消息文本内容
            sender_id (str): 发送者ID，用于处理@功能
            need_at (bool): 是否需要@用户，默认为False

        Returns:
            list: 包含消息链元素的列表
        """
        parts = []
        last_end = 0
        Inimage = False
        # 匹配 Markdown 格式的网络图片 ![alt](http://...)
        image_pattern = re.compile(r'!\[.*?\]\((https?://\S+)\)')
        # 匹配本地绝对路径
        local_image_pattern = re.compile(r'(\/home\/\S+)')
        # 处理@功能
        if need_at:
            parts.append(platform_message.At(target=sender_id))

        # 处理网络图片 (Markdown 形式)
        for match in image_pattern.finditer(message):
            Inimage = True
            start, end = match.span()
            if start > last_end:
                parts.append(platform_message.Plain(text=message[last_end:start]))
            image_url = match.group(1)
            parts.append(platform_message.Image(url=image_url))  # ✅ 直接 url=URL
            last_end = end

        # 处理剩余文本
        if last_end + 1 < len(message) and Inimage:
            parts.append(platform_message.Plain(text=message[last_end:]))
        elif not Inimage:
            parts.append(platform_message.Plain(text=message))

        # 处理本地图片路径
        for match in local_image_pattern.finditer(message):
            print(f'match={local_image_pattern.finditer(message)}')
            image_path = Path(match.group(1))
            print(image_path)
            if image_path.exists():
                print(f'parts={parts}')
                try:
                    with open(image_path, 'rb') as img_file:
                        img_bytes = img_file.read()
                        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                    return [platform_message.Image(base64=img_base64)]
                except Exception as e:
                    return [platform_message.Plain(text=f"[Error loading image: {e}]")]
        return parts if parts else [platform_message.Plain(text=message)]
