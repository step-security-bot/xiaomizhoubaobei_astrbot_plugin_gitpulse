"""Pytest 公共配置：在缺少 AstrBot 运行时环境时注入最小桩.

本插件的源码依赖 ``astrbot.api``（由 AstrBot 宿主提供）。单元测试不应强依赖
完整宿主，故此处仅在 ``astrbot`` 不可导入时，注册一组轻量桩模块，
让被测模块（formatter / config）可以在纯净环境下被导入。
真实环境中 astrbot 已存在，本文件不做任何覆盖。
"""

import sys
from types import ModuleType


class _StubLogger:
    """最小可用的日志桩."""

    def debug(self, *args, **kwargs) -> None:
        pass

    def info(self, *args, **kwargs) -> None:
        pass

    def warning(self, *args, **kwargs) -> None:
        pass

    def error(self, *args, **kwargs) -> None:
        pass


def _install_astrbot_stubs() -> None:
    """在 astrbot 缺失时安装最小桩，避免测试收集阶段导入失败."""
    if "astrbot" in sys.modules:
        return

    try:
        __import__("astrbot")

        return
    except ImportError:
        pass

    astrbot = ModuleType("astrbot")
    api = ModuleType("astrbot.api")
    api.logger = _StubLogger()
    api.AstrBotConfig = dict
    api.all = ModuleType("astrbot.api.all")
    api.message_components = ModuleType("astrbot.api.message_components")

    star = ModuleType("astrbot.api.star")

    class _Star:
        def __init__(self, context=None):
            self.context = context

    class _Context:
        pass

    def _register(*args, **kwargs):
        def _decorator(cls):
            return cls

        return _decorator

    star.Star = _Star
    star.Context = _Context
    star.register = _register
    api.star = star

    class _Plain:
        def __init__(self, *args, **kwargs):
            pass

    api.message_components.Plain = _Plain

    astrbot.api = api
    sys.modules["astrbot"] = astrbot
    sys.modules["astrbot.api"] = api
    sys.modules["astrbot.api.all"] = api.all
    sys.modules["astrbot.api.star"] = star
    sys.modules["astrbot.api.message_components"] = api.message_components


_install_astrbot_stubs()
