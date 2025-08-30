# LangBotPluginBox

Lang一些小功能插件集合

可以更加模板在`func`中添加自己的小功能，触发使用模板中定义的触发命令使用

## 使用方法

核心文件在`core`目录下

目前包括`help.py`,用来遍历`func`目录下的插件,可修改`help.py`下的关键词更改触发

参照目录`func`中示例代码的使用

！！！除非必要，`core`下文件不要修改

```python
# 触发关键词，支持英文和中文触发
KEYWORD = "calc"

# 功能描述，会在插件列表中显示
DESCRIPTION = "简单计算器，支持加减乘除"

# 主要功能在execute函数中实现
async def execute(event_context: context.EventContext, args: List[str]) -> str:
    """
    执行主要功能

    Args:
        event_context: 事件上下文
        args: 参数列表

    Returns:
        str: 执行结果
    """
```


## AI 生成建议

- 不要实现复杂功能，复杂功能更建议独立插件系统
- ~~还没想好~~

## 插件列表

- **菜单**：显示所有可用的功能命令
- **计算器**：简单的加减乘除计算器
- **测试**：测试中文回显功能
- **回显**：回显用户输入
## 开发进度

- [ ] 完善其他插件小功能
- [x] 完成基础功能开发
