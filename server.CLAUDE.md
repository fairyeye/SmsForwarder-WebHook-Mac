[根目录](./CLAUDE.md) > **server.py**

# HTTP 服务器模块

## 模块职责

server.py 负责实现 HTTP 服务器功能，主要职责包括：

1. 监听指定端口的 HTTP 请求
2. 解析 POST 请求中的通知数据
3. 识别通知来源应用
4. 调用回调函数处理通知
5. 返回响应给客户端

## 入口与启动

### 服务器启动函数

```python
def start_server(port=19999, callback=None):
    global notification_callback
    notification_callback = callback

    server = HTTPServer(('0.0.0.0', port), NotificationServer)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    print(f"HTTP 服务运行在端口 {port}")
    return server
```

## 对外接口

### 请求处理类

```python
class NotificationServer(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_POST(self):
        global notification_callback

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = parse_qs(post_data)

        source = unquote(parsed_data.get('from', [''])[0])
        content = unquote(parsed_data.get('content', [''])[0])

        app_name = get_app_name(source)

        if notification_callback:
            notification_callback(app_name, content)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('已接收'.encode('utf-8'))
```

### 应用识别函数

```python
def get_app_name(package_name):
    if package_name.isdigit() or package_name.startswith('+'):
        return f'短信 {package_name}'
    return APP_NAME_MAP.get(package_name, package_name)
```

### 应用包名映射

```python
APP_NAME_MAP = {
    'com.tencent.mm': '微信',
    'com.tencent.mobileqq': 'QQ',
    'com.alibaba.android.rimet': '钉钉',
    'com.ss.android.ugc.aweme': '抖音',
    'com.smartisanos.notes': '笔记',
    'com.android.mms': '短信',
    'com.miui.mms': '短信',
}
```

## 关键依赖与配置

### 依赖库

- **http.server**: 内置 HTTP 服务器
- **urllib.parse**: URL 解析和编码
- **threading**: 多线程支持
- **os**: 系统操作

### 配置参数

```python
# 应用包名映射
APP_NAME_MAP = {
    'com.tencent.mm': '微信',
    'com.tencent.mobileqq': 'QQ',
    # 可以添加更多应用映射
}

# 默认监听端口
def start_server(port=19999, callback=None):
```

## 数据模型

### 请求参数格式

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| from | string | 是 | 来源标识（手机号或包名） |
| content | string | 是 | 通知内容 |
| timestamp | string | 否 | 时间戳（可选） |

### 响应格式

```
HTTP/1.1 200 OK
Content-Type: text/plain

已接收
```

## 测试与质量

### 测试重点

1. 服务器启动和停止
2. 请求解析
3. 应用识别
4. 回调函数调用
5. 响应格式

### 测试方法

```python
import unittest
import http.client
import urllib.parse

class TestNotificationServer(unittest.TestCase):
    def test_send_sms_notification(self):
        conn = http.client.HTTPConnection('localhost', 19999)
        params = urllib.parse.urlencode({'from': '13800138000', 'content': '验证码：123456'})
        conn.request('POST', '/', params)
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.read().decode(), '已接收')
        conn.close()

    def test_send_wechat_notification(self):
        conn = http.client.HTTPConnection('localhost', 19999)
        params = urllib.parse.urlencode({'from': 'com.tencent.mm', 'content': '新消息'})
        conn.request('POST', '/', params)
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.read().decode(), '已接收')
        conn.close()

if __name__ == '__main__':
    unittest.main()
```

## 常见问题 (FAQ)

### Q: 服务器无法启动

**可能原因**：
- 端口被占用
- 权限不足

**解决方案**：
```bash
# 检查端口占用
lsof -ti:19999

# 杀掉占用进程
lsof -ti:19999 | xargs kill -9

# 检查权限
python3 --version
```

### Q: 请求无法解析

**可能原因**：
- 请求格式不正确
- 参数编码问题

**解决方案**：
- 确保使用正确的 POST 请求格式
- 检查参数编码是否为 UTF-8

## 相关文件清单

| 文件 | 描述 |
|------|------|
| server.py | HTTP 服务器模块 |
| main.py | 主应用入口文件 |
| history.py | 历史记录管理模块 |
| setup.py | 打包配置文件 |

## 变更记录 (Changelog)

### 2026-03-02 v1.0.0

- ✅ 实现 HTTP 服务器功能
- ✅ 完成请求解析和响应
- ✅ 实现应用识别
- ✅ 添加应用包名映射
- ✅ 支持多线程处理
