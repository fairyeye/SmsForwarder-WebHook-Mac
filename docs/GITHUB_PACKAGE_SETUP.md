# GitHub Actions 自动打包配置指南

## 概述

本文档详细介绍如何配置和使用 GitHub Actions 自动打包 macOS 应用通知接收器。配置完成后，每当推送标签或创建发布时，系统会自动打包应用、创建 DMG 安装程序并发布到 GitHub Releases。

## 文件结构

```
.
├── .github/
│   └── workflows/
│       └── release.yml          # GitHub Actions 工作流配置
├── GITHUB_RELEASE.md            # 使用说明文档
├── GITHUB_PACKAGE_SETUP.md      # 本配置指南
├── test_github_action.py        # 测试脚本
├── setup.py                     # 打包配置
└── main.py                       # 应用主入口
```

## 配置文件详解

### 1. GitHub Actions 工作流配置 (.github/workflows/release.yml)

```yaml
name: 自动打包和发布

on:
  push:
    tags:
      - 'v*'                      # 标签推送触发
  release:
    types: [published]            # 发布创建触发

jobs:
  build:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - name: 安装 Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 安装项目依赖
        run: |
          python -m pip install --upgrade pip
          pip install rumps py2app pyperclip

      - name: 打包应用
        run: |
          rm -rf build dist
          python3 setup.py py2app

      - name: 验证构建结果
        run: |
          ls -la dist/
          echo "---"
          ls -la dist/*.app/Contents/

      - name: 创建 DMG 安装程序
        run: |
          npm install -g appdmg
          cat > appdmg.json << 'EOF'
          {
            "title": "通知接收器",
            "icon": "notification-icon.icns",
            "background": "none",
            "contents": [
              { "x": 192, "y": 344, "type": "file", "path": "dist/通知接收器.app" },
              { "x": 448, "y": 344, "type": "link", "path": "/Applications" }
            ]
          }
          EOF
          appdmg appdmg.json dist/通知接收器.dmg

      - name: 获取版本信息
        id: get_version
        run: echo "VERSION=${GITHUB_REF#refs/tags/}" >> $GITHUB_ENV

      - name: 压缩应用程序
        run: |
          cd dist
          zip -r '通知接收器.app.zip' '通知接收器.app'

      - name: 上传到 GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: |
            dist/通知接收器.app.zip
            dist/通知接收器.dmg
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: 清理临时文件
        if: always()
        run: rm -f appdmg.json
```

### 2. py2app 打包配置 (setup.py)

```python
from setuptools import setup
import os

APP = ['main.py']
ICON_FILE = 'notification-icon.icns'
ICON_PNG = 'notification-icon.png'
DATA_FILES = [('Resources', [ICON_FILE, ICON_PNG, 'server.py', 'history.py'])]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
        'CFBundleIdentifier': 'com.notification.receiver',
        'CFBundleName': '通知接收器',
        'CFBundleDisplayName': '通知接收器',
        'CFBundleIconFile': ICON_FILE,
        'CFBundleShortVersionString': '1.0.1',
        'CFBundleVersion': '1.0.1',
        'NSHumanReadableCopyright': '© 2026. All rights reserved.',
    },
    'packages': ['rumps', 'pyperclip'],
    'resources': [ICON_FILE, ICON_PNG, 'server.py', 'history.py'],
    'includes': ['rumps', 'pyperclip'],
    'excludes': ['unittest', 'test', 'setuptools'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```

### 3. 本地测试脚本 (test_github_action.py)

用于在本地测试打包过程，验证与 GitHub Actions 环境的兼容性。

## 配置步骤

### 1. 确保项目已推送到 GitHub

```bash
# 初始化 git 仓库
git init

# 配置远程仓库
git remote add origin <your-repository-url>

# 添加并提交文件
git add .
git commit -m "初始化项目"

# 推送到远程仓库
git push -u origin main
```

### 2. 测试本地打包过程

```bash
# 运行测试脚本
python3 test_github_action.py

# 或者手动执行
rm -rf build dist
pip3 install -r requirements.txt
python3 setup.py py2app
```

### 3. 启用 GitHub Actions

1. 进入项目仓库
2. 点击 "Settings" -> "Actions" -> "General"
3. 在 "Actions permissions" 中选择 "Allow all actions and reusable workflows"
4. 点击 "Save"

### 4. 配置环境变量（可选）

如果需要自定义配置，可以在 Settings -> Secrets and variables -> Actions 中添加以下变量：

- `APP_NAME`: 应用名称（默认：通知接收器）
- `APP_VERSION`: 应用版本（默认：从标签自动获取）
- `MACOS_VERSION`: macOS 版本（默认：10.15）

## 使用方法

### 方法一：通过标签推送触发打包

```bash
# 创建标签（格式：v1.0.0）
git tag v1.0.1

# 推送到远程仓库
git push origin v1.0.1
```

### 方法二：通过 GitHub 网页界面创建发布

1. 进入仓库页面
2. 点击 "Releases" -> "Draft a new release"
3. 填写：
   - Tag version: v1.0.1
   - Release title: v1.0.1 版本发布
   - Description: 简要说明版本变更
4. 点击 "Publish release"

### 方法三：通过 GitHub CLI 触发发布

```bash
gh release create v1.0.1 --notes "修复通知显示问题" --title "v1.0.1 版本"
```

## 检查打包状态

### 查看 GitHub Actions 运行情况

1. 进入项目仓库
2. 点击 "Actions" 标签
3. 选择 "自动打包和发布" 工作流
4. 点击最近的运行记录查看详细日志

### 下载发布的文件

1. 进入 "Releases" 页面
2. 在 Assets 部分下载以下文件：
   - `通知接收器.app.zip`：压缩后的应用程序
   - `通知接收器.dmg`：DMG 安装程序

## 常见问题排查

### 1. 打包失败

**错误信息**：pip 安装依赖失败

**解决方法**：
```yaml
# 在工作流中添加重试机制
- name: 安装项目依赖
  run: |
    python -m pip install --upgrade pip
    pip install --retries 3 rumps py2app pyperclip
```

### 2. DMG 创建失败

**错误信息**：appdmg 安装失败或权限问题

**解决方法**：
```yaml
- name: 创建 DMG 安装程序
  run: |
    npm install -g --unsafe-perm appdmg
    # ...
```

### 3. 应用程序无法运行

**错误信息**：打包过程中依赖库缺失

**解决方法**：
```python
# setup.py 中检查 resources 和 packages 配置
OPTIONS = {
    'packages': ['rumps', 'pyperclip'],
    'resources': [ICON_FILE, ICON_PNG, 'server.py', 'history.py'],
    'includes': ['rumps', 'pyperclip'],
}
```

### 4. 通知接收器权限问题

**错误信息**：运行时出现权限警告

**解决方法**：
```python
# setup.py 中添加权限配置
OPTIONS = {
    'plist': {
        'NSAppleEventsUsageDescription': '此应用需要发送通知权限',
        'NSHumanReadableCopyright': '© 2026. All rights reserved.',
    },
}
```

### 5. 打包超时

**错误信息**：构建过程超时

**解决方法**：
```yaml
# 在工作流中增加超时设置
jobs:
  build:
    runs-on: macos-latest
    timeout-minutes: 60
```

## 调试和测试

### 1. 本地模拟 GitHub Actions 环境

```bash
# 使用 act 工具本地运行 GitHub Actions
brew install nektos/tap/act
act -j build
```

### 2. 测试应用程序

```bash
# 安装并运行打包后的应用
open dist/通知接收器.app

# 测试通知功能
curl -X POST -d "from=13800138000&content=验证码：123456" http://localhost:19999
```

### 3. 验证 DMG 安装程序

```bash
# 挂载 DMG 并验证
hdiutil attach dist/通知接收器.dmg
ls -la /Volumes/通知接收器/
hdiutil detach /Volumes/通知接收器
```

## 性能优化建议

### 1. 缓存依赖

```yaml
- name: 缓存 Python 依赖
  uses: actions/cache@v4
  with:
    path: ~/Library/Caches/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### 2. 使用更快的镜像源

```bash
pip install -i https://mirrors.aliyun.com/pypi/simple/ rumps py2app pyperclip
```

### 3. 并行执行任务

```yaml
jobs:
  build:
    runs-on: macos-latest
    steps:
      - name: 安装依赖
        run: |
          pip install rumps py2app
          npm install -g appdmg
```

## 安全考虑

### 1. 依赖验证

确保使用官方仓库的依赖：
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org rumps
```

### 2. 构建环境隔离

使用 GitHub 托管的 runner，避免使用自托管的不安全环境。

### 3. 发布前验证

```yaml
- name: 验证应用程序
  run: |
    osascript -e 'tell application "通知接收器" to activate'
    sleep 5
    osascript -e 'tell application "通知接收器" to quit'
```

## 版本控制建议

### 1. 语义化版本控制

```
vMAJOR.MINOR.PATCH
  ├─ 主要版本（不兼容变更）
  ├─ 次要版本（新功能）
  └─ 补丁版本（错误修复）
```

### 2. 发布流程

1. 修复 bug 或添加新功能
2. 更新 setup.py 中的版本号
3. 创建和推送标签
4. 检查 GitHub Actions 结果
5. 验证下载的文件

## 总结

通过配置 GitHub Actions 自动打包功能，您可以：

1. 实现代码提交到发布的自动化流程
2. 确保每个版本的打包环境一致性
3. 提供可信赖的安装程序给用户
4. 简化发布过程，减少人为错误

如果您在使用过程中遇到问题，请参考本文档的常见问题排查部分或提交 Issue 反馈。