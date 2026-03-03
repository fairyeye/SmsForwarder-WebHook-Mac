# 通知接收器 - 完整开发文档

## 目录
1. [项目概述](#项目概述)
2. [功能特性](#功能特性)
3. [技术栈](#技术栈)
4. [项目结构](#项目结构)
5. [安装与部署](#安装与部署)
6. [使用指南](#使用指南)
7. [API 接口](#api-接口)
8. [自定义图标](#自定义图标)
9. [配置说明](#配置说明)
10. [开发指南](#开发指南)
11. [常见问题](#常见问题)

---

## 项目概述

通知接收器是一个 macOS 状态栏应用，用于接收和处理来自 Android 设备的短信和应用通知。应用通过 HTTP 服务器接收 POST 请求，并在 macOS 上显示系统通知，同时保存历史记录供查看。

### 主要特点
- 轻量级状态栏应用
- 实时接收通知
- 历史记录管理
- 数据持久化
- 自动识别应用类型

---

## 功能特性

### 核心功能
- ✅ **状态栏图标** - 在 macOS 状态栏显示铃铛图标
- ✅ **HTTP 服务器** - 监听端口 19999 接收 POST 请求
- ✅ **系统通知** - 收到通知时弹出 macOS 系统通知
- ✅ **历史记录** - 保存最近 50 条通知记录
- ✅ **数据持久化** - 应用关闭后记录不丢失
- ✅ **应用识别** - 自动识别短信、微信、QQ 等应用

### 用户交互
- ✅ **菜单显示** - 点击状态栏图标显示历史记录
- ✅ **刷新功能** - 手动刷新历史记录列表
- ✅ **清空历史** - 一键清空所有历史记录
- ✅ **静默退出** - 无提示退出应用
- ✅ **验证码复制** - 点击历史记录自动复制短信验证码
- ✅ **通知点击复制** - 点击通知自动复制验证码
- ✅ **显示按钮** - 通知带"显示"按钮，点击打开历史记录

---

## 技术栈

### 开发语言
- **Python 3.11+** - 主要开发语言

### 核心库
- **rumps** - macOS 状态栏应用框架
- **py2app** - Python 应用打包工具
- **http.server** - 内置 HTTP 服务器
- **threading** - 多线程支持
- **pyperclip** - 剪贴板操作
- **PyObjC** - Python 与 Objective-C 桥接（用于带按钮通知）

### 系统依赖
- **macOS 10.9+** - 操作系统要求
- **PyObjC** - Python 与 Objective-C 桥接

---

## 项目结构

```
notification-app/
├── main.py                  # 主应用入口
├── server.py                # HTTP 服务器
├── history.py               # 历史记录管理
├── setup.py                 # py2app 打包配置
├── notification-icon.icns   # 应用图标
├── README.md                # 项目说明
├── build/                   # 构建临时文件
└── dist/                    # 打包输出
    └── 通知接收器.app       # 可执行应用
```

### 文件说明

#### main.py
主应用文件，包含：
- `NotificationApp` 类：应用主逻辑
- `NotificationDelegate` 类：带按钮通知处理
- 状态栏菜单管理
- 通知处理回调
- 用户交互处理
- 验证码提取和复制功能

#### server.py
HTTP 服务器模块，包含：
- `NotificationServer` 类：HTTP 请求处理
- `start_server()` 函数：启动服务器
- 包名映射配置

#### history.py
历史记录管理模块，包含：
- `HistoryManager` 类：记录 CRUD 操作
- JSON 文件持久化
- 格式化输出

---

## 安装与部署

### 环境要求
- macOS 10.9 或更高版本
- Python 3.11 或更高版本

### 开发环境安装

1. **安装依赖**
```bash
pip3 install rumps py2app pyperclip
```

2. **获取源码**
```bash
git clone <repository-url>
cd notification-app
```

### 打包应用

1. **清理旧版本**
```bash
rm -rf build dist
```

2. **执行打包**
```bash
python3 setup.py py2app
```

3. **获取应用**
打包完成后，应用位于 `dist/通知接收器.app`

---

## 使用指南

### 启动应用

**方法一：双击应用**
```bash
open dist/通知接收器.app
```

**方法二：命令行运行**
```bash
cd notification-app
python3 main.py
```

### 状态栏菜单

点击状态栏铃铛图标，菜单结构：

```
━━━━━━━━━━ 历史记录 ━━━━━━━━━━
1. [2026-02-28 16:15:32] 短信 13800138000
   这是一条测试短信内容
   
━━━━━━━━━━ 历史记录 ━━━━━━━━━━
2. [2026-02-28 16:14:20] 微信
   测试消息内容
   
刷新
清空历史记录

退出
```

### 功能操作

**查看**历史记录
- 点击状态栏图标
- 自动显示最近 5 条记录
- 点击"刷新"更新列表

**清空**历史记录
- 点击"清空历史记录"
- 历史记录立即清空
- 无弹窗提示

**退出**应用
- 点击"退出"
- 应用静默退出

### 验证码功能

**自动识别验证码**
- 系统自动识别短信中的验证码（4-6位数字）
- 支持多种格式：
  - `验证码：123456`
  - `验证码是 123456`
  - 纯数字 6 位
  - 纯数字 4 位

**点击历史记录复制验证码**
- 点击历史记录项
- 如果是短信且包含"验证码"或"码"字样
- 自动提取并复制 4-6 位数字到剪贴板
- 弹出通知确认复制成功

**点击通知复制验证码**
- 点击 macOS 通知
- 自动复制最新短信的验证码到剪贴板
- 弹出通知确认复制成功

**点击"显示"按钮**
- 通知带有"显示"按钮
- 点击按钮打开状态栏菜单
- 显示历史记录列表

---

## API 接口

### 接口信息
- **协议**: HTTP
- **方法**: POST
- **端口**: 19999
- **URL**: `/sms` 或 `/notify`（任意路径）

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| from | string | 是 | 来源标识（手机号或包名） |
| content | string | 是 | 通知内容 |
| timestamp | string | 否 | 时间戳（可选） |

### 请求示例

**短信通知**
```bash
curl -X POST \
  -d "from=13800138000&content=验证码：123456" \
  http://localhost:19999/sms
```

**微信通知**
```bash
curl -X POST \
  -d "from=com.tencent.mm&content=新消息：测试" \
  http://localhost:19999/notify
```

**完整参数**
```bash
curl -X POST \
  -d "from=com.tencent.mm&content=测试内容&timestamp=1772262084530" \
  http://localhost:19999/notify
```

### 响应
- **成功**: `已接收` (HTTP 200)
- **失败**: HTTP 错误码

---

## 自定义图标

### 图标要求

**文件格式**
- **状态栏图标**: `.icns` 格式
- **通知图标**: 可使用系统默认

**图标尺寸**
macOS `.icns` 文件应包含以下尺寸：
- 16x16
- 32x32
- 64x64
- 128x128
- 256x256
- 512x512
- 1024x1024（可选）

### 创建自定义图标

**方法一：使用 sips（系统自带）**
```bash
# PNG 转 ICNS
sips -s format icns icon.png --out notification-icon.icns
```

**方法二：使用 iconutil（推荐）**
```bash
# 创建 iconset 文件夹
mkdir MyIcon.iconset

# 准备不同尺寸的图片
cp icon_16x16.png MyIcon.iconset/icon_16x16.png
cp icon_32x32.png MyIcon.iconset/icon_32x32.png
cp icon_64x64.png MyIcon.iconset/icon_64x64.png
cp icon_128x128.png MyIcon.iconset/icon_128x128.png
cp icon_256x256.png MyIcon.iconset/icon_256x256.png
cp icon_512x512.png MyIcon.iconset/icon_512x512.png

# 生成 .icns
iconutil -c icns MyIcon.iconset -o notification-icon.icns
```

**方法三：使用第三方工具**
- **Icon Slate**: https://www.icnsapp.com/
- **Image2icon**: https://www.img2icnsapp.com/

### 替换图标

1. 准备 `notification-icon.icns` 文件
2. 放置在 `notification-app/` 目录
3. 重新打包应用：
```bash
rm -rf build dist
python3 setup.py py2app
```

### 修改代码引用

编辑 `main.py` 第 10 行：
```python
icon_path = os.path.join(os.path.dirname(__file__), 'your-custom-icon.icns')
```

---

## 配置说明

### 修改端口

编辑 `server.py` 第 49 行：
```python
def start_server(port=19999, callback=None):
```

### 修改历史记录数量

编辑 `main.py` 第 17 行：
```python
self.history_manager = HistoryManager(max_records=50)
```

### 修改应用包名映射

编辑 `server.py` 第 6-14 行：
```python
APP_NAME_MAP = {
    'com.tencent.mm': '微信',
    'com.tencent.mobileqq': 'QQ',
    # 添加更多...
}
```

### 修改菜单显示数量

编辑 `main.py` 第 33 行：
```python
for idx, record in enumerate(history[:5], 1):
    # 改为 [:10] 显示 10 条
```

---

## 开发指南

### 调试模式

**启用日志输出**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**使用 py2app 调试**
```bash
python3 setup.py py2app -A
```

### 添加新功能

**添加新的应用包名识别**

1. 编辑 `server.py` 的 `APP_NAME_MAP`
2. 添加新映射

**添加菜单项**

编辑 `main.py` 的 `__init__` 方法：
```python
self.menu = [
    rumps.MenuItem("新功能", callback=self.new_function),
    # ...
]
```

**修改通知处理**

编辑 `main.py` 的 `on_notification` 方法：
```python
def on_notification(self, app_name, content):
    # 添加自定义处理逻辑
    pass
```

### 测试

**单元测试**
```python
import unittest

class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        self.manager = HistoryManager(max_records=10)
    
    def test_add_record(self):
        self.manager.add_record("测试", "内容")
        self.assertEqual(len(self.manager.get_history()), 1)
```

**集成测试**
```bash
curl -X POST -d "from=test&content=test" http://localhost:19999/test
```

---

## 常见问题

### Q1: 应用无法启动

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

### Q2: 图标不显示

**可能原因**：
- 图标文件不存在
- 图标格式不正确
- Info.plist 配置错误

**解决方案**：
```bash
# 检查图标文件
ls -l notification-icon.icns

# 验证图标格式
file notification-icon.icns
```

**手动修复图标**：
```bash
# 1. 复制图标到 Resources 目录
cp notification-icon.icns dist/通知接收器.app/Contents/Resources/

# 2. 修改 Info.plist 中的 CFBundleIconFile
# 确保为: <string>notification-icon.icns</string>
```

### Q3: 打包后应用无法打开

**可能原因**：
- 打包时使用了不同版本的 Python
- 字节码文件 (.pyc) 不兼容

**解决方案**：
```bash
# 清理旧构建并重新打包
rm -rf build dist
python3 setup.py py2app
```

### Q4: 打包后图标未正确复制

**可能原因**：
- DATA_FILES 配置不正确
- 需要手动复制图标

**解决方案**：
```bash
# 手动复制图标到 Resources 目录
cp notification-icon.icns dist/通知接收器.app/Contents/Resources/
```

### Q5: 历史记录丢失

**可能原因**：
- 权限问题
- 文件路径错误

**解决方案**：
```bash
# 检查历史文件
cat ~/.notification_history.json

# 检查权限
ls -l ~/.notification_history.json
```

### Q4: 通知不弹窗

**可能原因**：
- 系统通知权限未开启
- 勿扰模式开启

**解决方案**：
1. 系统设置 → 通知 → 通知接收器
2. 启用"允许通知"

### Q5: 打包失败

**可能原因**：
- 依赖未安装
- 签名问题

**解决方案**：
```bash
# 重新安装依赖
pip3 install --upgrade rumps py2app

# 清理并重新打包
rm -rf build dist
python3 setup.py py2app
```

---

## 版本历史

### v1.0.1 (2026-03-02)
- ✅ 修复通知显示问题：优化通知处理逻辑
- ✅ 改进通知显示：添加备用通知机制（AppleScript）
- ✅ 优化通知内容处理：限制消息长度
- ✅ 增强错误处理：添加详细的异常信息
- ✅ 修复通知中特殊字符显示问题
- ✅ 新增 GitHub Actions 自动打包功能
- ✅ 支持自动创建 DMG 安装程序
- ✅ 集成 GitHub Release 自动发布

### v1.0.0 (2026-02-28)
- ✅ 初始版本发布
- ✅ 基础通知接收功能
- ✅ 历史记录管理
- ✅ 状态栏应用
- ✅ 打包支持
- ✅ 验证码自动复制
- ✅ 带按钮通知

### v1.1.0 (2026-02-28)
- ✅ 历史记录点击复制验证码
- ✅ 通知点击复制验证码
- ✅ "显示"按钮打开历史记录

---

## 许可证

MIT License

---

## 联系方式

- 问题反馈：提交 Issue
- 功能建议：提交 Pull Request

---

## 致谢

感谢以下开源项目：
- [rumps](https://github.com/jaredks/rumps) - macOS 状态栏应用框架
- [py2app](https://github.com/ronaldoussoren/py2app) - Python 应用打包工具
