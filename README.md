# LangBotPluginBox

A LangBot plugin collection that implements small features that don't require independent plugins.

You can add your own small features in the `func` directory.

## Usage

- Use `菜单` (menu) to view all features
    - 菜单 --help to view menu details
- Use <function name> to trigger the corresponding function
- <function name> --help to view function details

## Feature Development

Core files are located in the `core` directory.

Refer to the example code usage in the `func` directory.

!!! Unless necessary, DO NOT modify files under `core`

```python
# Use get_info() function to provide module information
def get_info() -> Dict[str, str]:
    """
    Get module information
        keyword : Required - trigger command
        description : Required - feature description
        usage : Required - command usage
        need_at : Optional - whether @user is required
    Returns:
        Dict[str, str]: Dictionary containing module info, must include at least keyword and description
    """
    return {
        "keyword": "测试",
        "description": "Test feature, echoes user input",
        "usage": "测试 content",
        "need_at": True
    }

# Main functionality is implemented in the execute function
async def execute(event_context: context.EventContext, request_dict) -> str:
    """
    Execute main functionality

    Args:
        event_context: Event context
        request_dict: Request dictionary containing args, args_text, sender_id, message etc.

    Returns:
        str: Execution result
    """
```


## AI Generation Suggestions

- Don't implement complex features; complex features are better suited for independent plugin systems
- ~~Haven't figured it out yet~~
- You can use config to edit menu images in HTML, upload them to an image hosting service, and change menu commands to more elegant image displays

## Plugin List

| Feature | Trigger Command | Description |
| :--: | :------: | :--------------: |
| Menu | 菜单 | Display all features |
| Bing Daily | bing | Bing daily wallpaper |
| Look Beauty | 看妹妹(archive) | Random beauty images |
| Pat Head | 摸头 | Pat QQ avatar |
| KFC | kfc | Random KFC Thursday jokes |
| Weather | 天气 | QWeather function, requires API key and API Host configuration (independent for each developer), [Console](https://console.qweather.com/home?lang=zh) |
| Morning News | 早报 | Daily 60s morning news image |
| req_demo | req_demo | Test parameter passing |
| Test | 测试 | Test text and image features |

## Supported Platforms

| Platform | Status | Notes |
| :--------: | :--: | :----: |
| OneBot V11 | ✅ | Napcat |

## Development Progress

- [ ] Improve other plugin features
- [x] Use dictionary method for parameter passing
- [x] Add admin features
- [x] Add enable/disable functionality
- [x] Add help support for features
- [x] Add image support
- [x] Enhance plugin trigger methods
- [x] Complete basic feature development

### Update History

- V1.0.2  Official release and QWeather request update
- V0.8.11 Fix image parsing issues

## Feedback & Feature Development

[![QQ Group](https://img.shields.io/badge/QQ群-965312424-green)](https://qm.qq.com/cgi-bin/qm/qr?k=en97YqjfYaLpebd9Nn8gbSvxVrGdIXy2&jump_from=webapi&authKey=41BmkEjbGeJ81jJNdv7Bf5EDlmW8EHZeH7/nktkXYdLGpZ3ISOS7Ur4MKWXC7xIx)
