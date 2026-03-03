import json
import os
from datetime import datetime

class HistoryManager:
    def __init__(self, max_records=50):
        self.max_records = max_records
        self.history_file = os.path.join(os.path.expanduser('~'), '.notification_history.json')
        self.history = []
        self.load_history()
    
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except Exception as e:
                print(f"加载历史记录失败: {e}")
                self.history = []
    
    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {e}")
    
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
    
    def get_history(self):
        return self.history
    
    def clear_history(self):
        self.history = []
        self.save_history()
    
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
