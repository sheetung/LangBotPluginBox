# LangBotPluginBox

LangBot插件，实现一些不需要独立制作插件的小功能集合

可以在`func`目录下添加自己的小功能

## 使用方法

- 使用`菜单`查看所有功能
    - 菜单 --help 查看菜单详细信息
- 使用<功能名>  触发对应功能
- <功能名> --help 查看功能详细信息

## 功能开发

核心文件在`core`目录下


参照目录`func`中示例代码的使用

！！！除非必要，`core`下文件不要修改

```python
# 使用get_info()函数提供模块信息
def get_info() -> Dict[str, str]:
    """
    获取模块信息
        keyword : 必需 触发指令
        description : 必需 功能描述
        usage : 必需 指令使用方法
        need_at : 可选 是否需要@用户
    Returns:
        Dict[str, str]: 包含模块信息的字典，至少包含keyword和description
    """
    return {
        "keyword": "测试", 
        "description": "测试功能，回显用户输入的内容",
        "usage": "测试 内容",
        "need_at": True
    }

# 主要功能在execute函数中实现
async def execute(event_context: context.EventContext, request_dict) -> str:
    """
    执行主要功能

    Args:
        event_context: 事件上下文
        request_dict: 请求字典，包含args、args_text、sender_id、message等信息

    Returns:
        str: 执行结果
    """
```


## AI 生成建议

- 不要实现复杂功能，复杂功能更建议独立插件系统
- ~~还没想好~~
- 可使用config在html编辑菜单图片并上传图床，将菜单命令改为更优雅的图片展示

## 插件列表

| 功能 | 触发命令 |       描述       |
| :--: | :------: | :--------------: |
| 菜单 |   菜单   |   显示所有功能   |
| 必应每日 |   bing   |   必应每日壁纸   |
| 看妹妹   |   看妹妹   |   随机美女图片   |
| 摸头   |   摸头   |   摸头qq头像   |
| kfc   |   kfc   |   随机疯狂星期四   |
| 天气   |   天气   |   和风天气API密钥，[链接](https://console.qweather.com/home?lang=zh)  |
| req_demo   |   req_demo   |   测试传参功能   |
| 测试 |   测试   | 测试文本以及图片功能 |

## 适配平台

|    平台    | 状态 |  备注  |
| :--------: | :--: | :----: |
| OneBot V11 |  ✅   | Napcat |

## 开发进度

- [ ] 完善其他插件小功能
- [x] 传参使用字典方法
- [x] 增加管理员功能
- [x] 增加启用/禁用功能
- [x] 增加功能help支持
- [x] 增加对图片的支持 
- [x] 增强功能插件的触发方式
- [x] 完成基础功能开发

### 已知BUG

- [x] 无法解析本地图片

## 问题反馈及功能开发

[![QQ群](https://img.shields.io/badge/QQ群-965312424-green)](https://qm.qq.com/cgi-bin/qm/qr?k=en97YqjfYaLpebd9Nn8gbSvxVrGdIXy2&jump_from=webapi&authKey=41BmkEjbGeJ81jJNdv7Bf5EDlmW8EHZeH7/nktkXYdLGpZ3ISOS7Ur4MKWXC7xIx)