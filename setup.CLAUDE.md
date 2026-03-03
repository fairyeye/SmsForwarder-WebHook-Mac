[根目录](./CLAUDE.md) > **setup.py**

# 打包配置模块

## 模块职责

setup.py 负责应用的打包配置，主要职责包括：

1. 配置 py2app 打包参数
2. 指定应用入口和资源文件
3. 配置应用属性和标识符
4. 管理打包过程

## 入口与启动

### 打包命令

```bash
# 清理旧构建
rm -rf build dist

# 执行打包
python3 setup.py py2app
```

## 配置说明

### 应用入口和资源

```python
APP = ['main.py']
ICON_FILE = 'notification-icon.icns'
ICON_PNG = 'notification-icon.png'
DATA_FILES = [('Resources', [ICON_FILE, ICON_PNG, 'server.py', 'history.py'])]
```

### 打包选项

```python
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
        'CFBundleIdentifier': 'com.notification.receiver',
        'CFBundleName': '通知接收器',
        'CFBundleDisplayName': '通知接收器',
        'CFBundleIconFile': ICON_FILE,
    },
    'packages': ['rumps', 'pyperclip'],
    'resources': [ICON_FILE, ICON_PNG, 'server.py', 'history.py'],
}
```

### 打包配置

```python
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```

## 关键依赖与配置

### 依赖库

- **setuptools**: Python 打包工具
- **py2app**: macOS 应用打包工具

### 配置参数

| 参数 | 类型 | 说明 |
|------|------|------|
| APP | list | 应用入口文件 |
| DATA_FILES | list | 资源文件列表 |
| OPTIONS | dict | 打包选项 |
| CFBundleIdentifier | string | 应用标识符 |
| CFBundleName | string | 应用名称 |
| CFBundleDisplayName | string | 应用显示名称 |
| CFBundleIconFile | string | 应用图标文件 |

## 测试与质量

### 测试重点

1. 打包过程
2. 应用资源完整性
3. 应用属性正确性

### 测试方法

```bash
# 打包应用
python3 setup.py py2app

# 检查输出目录
ls -la dist/

# 检查应用内容
cd dist/通知接收器.app/Contents && ls -la
```

## 常见问题 (FAQ)

### Q: 打包失败

**可能原因**：
- 依赖未安装
- 权限问题
- 文件路径错误

**解决方案**：
```bash
# 检查依赖
pip3 list | grep -E "(rumps|py2app|pyperclip)"

# 重新安装依赖
pip3 install --upgrade rumps py2app pyperclip

# 清理并重新打包
rm -rf build dist && python3 setup.py py2app
```

### Q: 打包后应用无法打开

**可能原因**：
- 打包时使用了不同版本的 Python
- 字节码文件不兼容

**解决方案**：
```bash
# 清理旧构建并重新打包
rm -rf build dist
python3 setup.py py2app
```

### Q: 图标不显示

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

# 重新打包
rm -rf build dist && python3 setup.py py2app
```

## 相关文件清单

| 文件 | 描述 |
|------|------|
| setup.py | 打包配置文件 |
| main.py | 主应用入口文件 |
| server.py | HTTP 服务器模块 |
| history.py | 历史记录管理模块 |
| notification-icon.icns | 应用图标 |
| notification-icon.png | 备用图标 |

## 变更记录 (Changelog)

### 2026-03-02 v1.0.0

- ✅ 实现 py2app 打包配置
- ✅ 添加应用入口和资源配置
- ✅ 配置应用属性和标识符
- ✅ 完成打包过程管理
- ✅ 支持图标和资源文件配置
