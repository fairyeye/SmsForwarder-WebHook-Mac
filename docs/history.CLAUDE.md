[根目录](./CLAUDE.md) > **history.py**

# 历史记录管理模块

## 模块职责

history.py 负责通知历史记录的管理，主要职责包括：

1. 保存通知历史记录
2. 提供历史记录的 CRUD 操作
3. 格式化历史记录显示
4. 数据持久化（JSON 文件存储）

## 入口与启动

### 初始化历史记录管理器

```python
class HistoryManager:
    def __init__(self, max_records=50):
        self.max_records = max_records
        self.history_file = os.path.join(os.path.expanduser('~'), '.notification_history.json')
        self.history = []
        self.load_history()
```

## 对外接口

### 添加记录

```python
def add_record(self, app_name, content):
    record = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'app': app_name,
        'content': content
    }
    self.history.insert(0, record)
    if len(self.history) > self.max_records:
        self.history = self.history[:self.max_records]
    self.save_history()
```

### 获取历史记录

```python
def get_history(self):
    return self.history
```

### 清空历史记录

```python
def clear_history(self):
    self.history = []
    self.save_history()
```

### 获取格式化历史记录

```python
def get_formatted_history(self):
    if not self.history:
        return "暂无历史记录"

    lines = []
    for idx, record in enumerate(self.history[:10], 1):
        lines.append(f"{idx}. [{record['timestamp']}] {record['app']}")
        lines.append(f"   {record['content']}")
        lines.append("")

    if len(self.history) > 10:
        lines.append(f"... 还有 {len(self.history) - 10} 条记录")

    return "\n".join(lines)
```

## 关键依赖与配置

### 依赖库

- **json**: JSON 数据处理
- **os**: 系统操作
- **datetime**: 日期时间处理

### 配置参数

```python
# 最大记录数量
def __init__(self, max_records=50):

# 历史记录文件路径
self.history_file = os.path.join(os.path.expanduser('~'), '.notification_history.json')
```

## 数据模型

### 记录格式

```python
{
    'timestamp': '2026-03-02 09:42:14',
    'app': '短信 13800138000',
    'content': '验证码：123456'
}
```

### 存储结构

```json
[
    {
        "timestamp": "2026-03-02 09:42:14",
        "app": "短信 13800138000",
        "content": "验证码：123456"
    },
    {
        "timestamp": "2026-03-02 09:40:00",
        "app": "微信",
        "content": "新消息"
    }
]
```

## 测试与质量

### 测试重点

1. 记录添加和获取
2. 记录格式化显示
3. 记录数量限制
4. 数据持久化
5. 清空历史记录

### 测试方法

```python
import unittest
from history import HistoryManager
import os

class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        self.test_file = os.path.join(os.path.expanduser('~'), '.test_notification_history.json')
        self.manager = HistoryManager(max_records=5)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_record(self):
        self.manager.add_record("测试应用", "测试内容")
        history = self.manager.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['app'], "测试应用")
        self.assertEqual(history[0]['content'], "测试内容")

    def test_max_records(self):
        for i in range(6):
            self.manager.add_record(f"应用{i}", f"内容{i}")
        history = self.manager.get_history()
        self.assertEqual(len(history), 5)
        self.assertEqual(history[0]['app'], "应用5")

    def test_clear_history(self):
        self.manager.add_record("测试应用", "测试内容")
        self.manager.clear_history()
        self.assertEqual(len(self.manager.get_history()), 0)

    def test_formatted_history(self):
        self.manager.add_record("测试应用", "测试内容")
        formatted = self.manager.get_formatted_history()
        self.assertIn("测试应用", formatted)
        self.assertIn("测试内容", formatted)

if __name__ == '__main__':
    unittest.main()
```

## 常见问题 (FAQ)

### Q: 历史记录丢失

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

### Q: 记录数量超过限制

**可能原因**：
- 代码中的 max_records 参数设置过大

**解决方案**：
```python
# 修改最大记录数量
manager = HistoryManager(max_records=30)
```

## 相关文件清单

| 文件 | 描述 |
|------|------|
| history.py | 历史记录管理模块 |
| main.py | 主应用入口文件 |
| server.py | HTTP 服务器模块 |
| ~/.notification_history.json | 历史记录存储文件（隐藏文件） |

## 变更记录 (Changelog)

### 2026-03-02 v1.0.0

- ✅ 实现历史记录管理
- ✅ 完成 CRUD 操作
- ✅ 实现数据持久化
- ✅ 添加记录格式化显示
- ✅ 支持记录数量限制
