# LangBotPluginBox

LangBot插件，实现一些不需要独立制作插件的小功能集合

可以在`func`目录下添加自己的小功能

## 使用方法

核心文件在`core`目录下


参照目录`func`中示例代码的使用

！！！除非必要，`core`下文件不要修改

```python


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

| 功能 | 触发命令 |       描述       |
| :--: | :------: | :--------------: |
| 菜单 |   菜单   |   显示所有功能   |
| 测试 |   测试   | 测试中文命令触发 |
| 回显 |   echo   |   回显用户输入   |

## 开发进度

- [ ] 完善其他插件小功能
- [x] 增强功能插件的触发方式
- [x] 完成基础功能开发

## 问题反馈及功能开发

[![QQ群](https://img.shields.io/badge/QQ群-965312424-green)](https://qm.qq.com/cgi-bin/qm/qr?k=en97YqjfYaLpebd9Nn8gbSvxVrGdIXy2&jump_from=webapi&authKey=41BmkEjbGeJ81jJNdv7Bf5EDlmW8EHZeH7/nktkXYdLGpZ3ISOS7Ur4MKWXC7xIx)