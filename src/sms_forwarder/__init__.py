"""
SMS 转发器 WebHook Mac 应用 - 自动接收和处理 Android 设备通知的 macOS 状态栏应用

提供以下功能：
- 实时接收 Android 设备通过 HTTP WebHook 发送的通知
- 自动识别短信验证码并复制到剪贴板
- 历史记录管理功能
- 系统通知显示
- 支持多种应用识别和过滤

主要模块：
- main: 应用主入口，负责 UI 和通知显示
- server: HTTP 服务器，接收 WebHook 请求
- history: 历史记录管理

使用方法：
    from sms_forwarder.main import NotificationApp
    app = NotificationApp()
    app.run()

或者直接运行：
    python -m sms_forwarder.main
"""

__version__ = "1.0.1"
__author__ = "通知接收器"
__email__ = ""
__license__ = "MIT"

from .main import NotificationApp
from .server import start_server
from .history import HistoryManager

__all__ = ["NotificationApp", "start_server", "HistoryManager"]