[根目录](./CLAUDE.md) > **main.py**

# 主应用模块

## 模块职责

main.py 是 SMS 转发器 WebHook Mac 应用的主入口文件，负责：

1. 实现 macOS 状态栏应用界面
2. 处理用户交互（菜单操作、通知点击）
3. 管理通知的接收和展示
4. 实现验证码自动识别和复制功能
5. 协调各个模块的工作

## 入口与启动

### 启动流程

```python
if __name__ == '__main__':
    app = NotificationApp()
    app.run()
```

### 应用初始化

```python
class NotificationApp(rumps.App):
    def __init__(self):
        icon_path = os.path.join(os.path.dirname(__file__), 'notification-icon.icns')
        if os.path.exists(icon_path):
            super().__init__("", icon=icon_path)
        else:
            super().__init__("🔔")

        self.history_manager = HistoryManager(max_records=50)

        self.menu = [
            rumps.MenuItem("刷新", callback=self.refresh_menu),
            rumps.MenuItem("清空历史记录", callback=self.clear_history),
            None,
            rumps.MenuItem("退出", callback=self.quit_app)
        ]

        start_server(port=19999, callback=self.on_notification)
        print("应用已启动")
```

## 对外接口

### 通知接收回调

```python
def on_notification(self, app_name, content):
    print(f"收到通知: [{app_name}] {content}")

    self.history_manager.add_record(app_name, content)

    self.refresh_menu(None)

    rumps.notification(
        title=app_name,
        subtitle="",
        message=content,
        sound=True
    )
```

### 验证码提取

```python
def extract_verification_code(content):
    if '验证码' not in content and '码' not in content:
        return None
    patterns = [
        r'(\d{6})',
        r'(\d{4})',
        r'验证码[：:]\s*(\d{4,6})',
        r'验证码是\s*(\d{4,6})',
        r'码\s*(\d{4,6})',
    ]
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    return None
```

### 菜单刷新

```python
def refresh_menu(self, _):
    history = self.history_manager.get_history()

    new_menu = []

    if history:
        new_menu.append(rumps.MenuItem("━━━━━━━━━━ 历史记录 ━━━━━━━━━━"))

        for idx, record in enumerate(history[:5], 1):
            content_preview = record['content'][:25] + "..." if len(record['content']) > 25 else record['content']
            menu_text = f"{idx}. [{record['timestamp']}] {record['app']}"

            menu_item = rumps.MenuItem(menu_text, callback=self.create_history_callback(idx - 1))
            new_menu.append(menu_item)
            new_menu.append(rumps.MenuItem(f"   {content_preview}"))

        new_menu.append(None)

    new_menu.append(rumps.MenuItem("刷新", callback=self.refresh_menu))
    new_menu.append(rumps.MenuItem("清空历史记录", callback=self.clear_history))
    new_menu.append(None)
    new_menu.append(rumps.MenuItem("退出", callback=self.quit_app))

    self.menu.clear()
    for item in new_menu:
        self.menu.add(item)
```

## 关键依赖与配置

### 依赖库

- **rumps**: macOS 状态栏应用框架
- **pyperclip**: 剪贴板操作
- **re**: 正则表达式匹配
- **os**: 系统操作
- **server**: HTTP 服务器模块
- **history**: 历史记录管理模块

### 配置参数

```python
# 历史记录最大数量
self.history_manager = HistoryManager(max_records=50)

# HTTP 服务器端口
start_server(port=19999, callback=self.on_notification)

# 菜单显示历史记录数量
for idx, record in enumerate(history[:5], 1):
```

## 数据模型

### 通知记录格式

```python
{
    'timestamp': '2026-03-02 09:42:14',
    'app': '短信 13800138000',
    'content': '验证码：123456'
}
```

## 测试与质量

### 测试重点

1. 应用启动和退出
2. 通知接收和显示
3. 菜单操作（刷新、清空历史、退出）
4. 验证码提取和复制
5. 历史记录管理

### 测试方法

```python
import unittest
from main import extract_verification_code

class TestVerificationCodeExtraction(unittest.TestCase):
    def test_extract_6_digit_code(self):
        self.assertEqual(extract_verification_code("验证码：123456"), "123456")

    def test_extract_4_digit_code(self):
        self.assertEqual(extract_verification_code("验证码：1234"), "1234")

    def test_extract_with_chinese_format(self):
        self.assertEqual(extract_verification_code("验证码是 123456"), "123456")

    def test_no_code(self):
        self.assertIsNone(extract_verification_code("这是一条普通短信"))

if __name__ == '__main__':
    unittest.main()
```

## 常见问题 (FAQ)

### Q: 应用无法启动

**可能原因**：
- 端口 19999 被占用
- Python 版本不兼容

**解决方案**：
```bash
# 检查端口占用
lsof -ti:19999

# 杀掉占用进程
lsof -ti:19999 | xargs kill -9

# 检查 Python 版本
python3 --version
```

### Q: 通知不弹窗

**可能原因**：
- 系统通知权限未开启
- 勿扰模式开启

**解决方案**：
1. 系统设置 → 通知 → 通知接收器
2. 启用"允许通知"

## 相关文件清单

| 文件 | 描述 |
|------|------|
| main.py | 主应用入口文件 |
| server.py | HTTP 服务器模块 |
| history.py | 历史记录管理模块 |
| setup.py | 打包配置文件 |
| notification-icon.icns | 应用图标 |
| README.md | 项目说明文档 |

## 变更记录 (Changelog)

### 2026-03-02 v1.0.0

- ✅ 实现状态栏应用界面
- ✅ 完成通知接收和展示功能
- ✅ 实现验证码自动识别和复制功能
- ✅ 完成历史记录管理
- ✅ 实现用户交互（菜单操作、通知点击）
