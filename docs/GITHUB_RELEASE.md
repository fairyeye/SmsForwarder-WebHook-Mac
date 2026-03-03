# GitHub 自动打包和发布指南

## 概述

该项目已配置 GitHub Actions 自动打包和发布功能。当创建新的标签或发布版本时，会自动执行以下操作：

1. 安装项目依赖
2. 使用 py2app 打包 macOS 应用
3. 验证构建结果
4. 创建 DMG 安装程序
5. 自动上传到 GitHub Release

## 配置说明

### 1. GitHub Actions 配置

配置文件位置：`.github/workflows/release.yml`

**触发条件**：
- 当推送标签（如 `v1.0.1`）时
- 当创建新的 Release 时

**主要任务**：
- 安装依赖：rumps、py2app、pyperclip
- 执行打包：python3 setup.py py2app
- 验证构建结果
- 创建 DMG 安装程序
- 上传到 GitHub Release

### 2. 打包配置

配置文件位置：`setup.py`

**版本信息**：
- CFBundleShortVersionString：1.0.1
- CFBundleVersion：1.0.1
- NSHumanReadableCopyright：© 2026. All rights reserved.

**包含资源**：
- notification-icon.icns：应用图标
- notification-icon.png：通知图标
- server.py：HTTP 服务器模块
- history.py：历史记录管理模块

## 使用方法

### 方式一：通过标签触发（推荐）

1. 确保代码已提交到 main 分支
2. 创建新的标签：
   ```bash
   git tag v1.0.1
   git push --tags
   ```

3. GitHub Actions 会自动触发打包过程

### 方式二：通过创建 Release 触发

1. 前往项目的 Releases 页面
2. 点击 "Draft a new release"
3. 填写版本信息（如 v1.0.1）
4. 点击 "Publish release"
5. GitHub Actions 会自动触发打包过程

### 方式三：本地测试打包（用于调试）

运行测试脚本来验证打包过程：

```bash
python3 test_github_action.py
```

## 检查打包过程

1. 进入项目的 Actions 页面
2. 查看最新的打包工作流
3. 点击工作流查看详细执行过程

## 发布后的文件

打包完成后，GitHub Release 会包含以下文件：

- **通知接收器.app.zip**：压缩后的应用程序
- **通知接收器.dmg**：DMG 安装程序

## 手动打包（可选）

如果需要手动打包，可以运行以下命令：

```bash
# 清理旧的构建文件
rm -rf build dist

# 执行打包
python3 setup.py py2app

# 压缩应用程序
cd dist && zip -r '通知接收器.app.zip' '通知接收器.app'
```

## 常见问题

### 1. 打包失败

**原因**：依赖库安装失败或环境问题

**解决方法**：
- 检查 GitHub Actions 日志
- 确保所有依赖库正常安装
- 检查 Python 版本是否兼容（需要 Python 3.11+）

### 2. 应用程序无法运行

**原因**：打包时缺少资源文件或依赖库

**解决方法**：
- 检查 setup.py 中 resources 配置
- 确保所有必需的文件都包含在打包中
- 检查应用程序控制台输出（Console.app）

### 3. DMG 文件创建失败

**原因**：appdmg 工具安装失败

**解决方法**：
- 检查 GitHub Actions 中 appdmg 安装过程
- 确保 Node.js 和 npm 版本兼容

## 版本管理建议

### 版本号规范

遵循语义化版本控制（Semantic Versioning）：
- 主版本号：不兼容的 API 变更
- 次版本号：向后兼容的功能新增
- 修订号：向后兼容的 bug 修复

**示例**：
- v1.0.0：初始版本
- v1.0.1：修复通知显示问题
- v1.1.0：新增通知过滤功能

### 发布流程

1. 更新代码和测试
2. 更新 setup.py 中的版本号
3. 更新 CHANGELOG.md（如果有）
4. 创建新的标签
5. 推送到 GitHub
6. 检查 GitHub Actions 执行结果
7. 验证发布的文件

## 安全注意事项

- GitHub Actions 配置会自动使用 `GITHUB_TOKEN`，无需手动设置
- 确保代码中的敏感信息不被提交到仓库
- 定期检查依赖库的安全更新

---

**注意**：首次使用时，可能需要允许 GitHub Actions 访问仓库的工作流权限。