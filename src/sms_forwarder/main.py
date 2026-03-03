#!/usr/bin/env python3

import rumps
import os
import re
import pyperclip
import sys

# 设置正确的工作路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 直接使用绝对导入
import server
import history

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

def is_sms(app_name):
    return '短信' in app_name

class NotificationApp(rumps.App):
    def __init__(self):
        icon_path = os.path.join(os.path.dirname(__file__), 'notification-icon.icns')
        if os.path.exists(icon_path):
            super().__init__("", icon=icon_path)
        else:
            super().__init__("🔔")

        self.history_manager = history.HistoryManager(max_records=50)
        
        self.menu = [
            rumps.MenuItem("刷新", callback=self.refresh_menu),
            rumps.MenuItem("清空历史记录", callback=self.clear_history),
            None,
            rumps.MenuItem("退出", callback=self.quit_app)
        ]
        
        server.start_server(port=19999, callback=self.on_notification)
        print("应用已启动")
    
    def show_menu(self):
        self.refresh_menu(None)
    
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
    
    def create_history_callback(self, index):
        def callback(_):
            history = self.history_manager.get_history()
            if 0 <= index < len(history):
                record = history[index]
                app_name = record['app']
                content = record['content']
                
                if is_sms(app_name):
                    code = extract_verification_code(content)
                    if code:
                        pyperclip.copy(code)
                        rumps.notification(
                            title="验证码已复制",
                            subtitle="",
                            message=f"验证码 {code} 已复制到剪贴板",
                            sound=False
                        )
                        return
                
                pyperclip.copy(content)
                rumps.notification(
                    title="内容已复制",
                    subtitle="",
                    message="内容已复制到剪贴板",
                    sound=False
                )
        return callback
    
    def on_notification(self, app_name, content):
        print(f"收到通知: [{app_name}] {content}")

        self.history_manager.add_record(app_name, content)

        self.refresh_menu(None)

        # 优化通知显示，确保在主线程中执行并处理各种边界情况
        try:
            # 确保消息长度适中，避免通知显示问题
            display_content = content[:100] + "..." if len(content) > 100 else content

            # 首先尝试显示应用名称和内容的通知
            rumps.notification(
                title=app_name,
                subtitle="",
                message=display_content,
                sound=True
            )

            # 如果是短信类应用，尝试提取验证码并显示单独的通知
            if is_sms(app_name):
                code = extract_verification_code(content)
                if code:
                    pyperclip.copy(code)
                    rumps.notification(
                        title="验证码已复制",
                        subtitle="",
                        message=f"验证码 {code} 已复制到剪贴板",
                        sound=False
                    )

        except Exception as e:
            print(f"显示通知失败: {e}")
            # 如果 rumps.notification 失败，尝试使用 AppleScript 通知
            try:
                import subprocess
                # 处理内容中的引号
                safe_content = content.replace('"', '\\"')
                safe_app_name = app_name.replace('"', '\\"')
                subprocess.run([
                    'osascript', '-e',
                    f'display notification "{safe_content}" with title "{safe_app_name}"'
                ], capture_output=True, text=True)
                print("✅ AppleScript 通知已发送")
            except Exception as e2:
                print(f"AppleScript 通知也失败: {e2}")
    
    def clear_history(self, _):
        self.history_manager.clear_history()
        self.refresh_menu(None)
    
    def quit_app(self, _):
        rumps.quit_application()
    
    @rumps.notifications
    def notification_center(self, info):
        history = self.history_manager.get_history()
        if history:
            latest = history[0]
            app_name = latest['app']
            content = latest['content']
            
            if is_sms(app_name):
                code = extract_verification_code(content)
                if code:
                    pyperclip.copy(code)
                    rumps.notification(
                        title="验证码已复制",
                        subtitle="",
                        message=f"验证码 {code} 已复制到剪贴板",
                        sound=False
                    )
                    return
            
            pyperclip.copy(content)
            rumps.notification(
                title="内容已复制",
                subtitle="",
                message="点击查看历史记录",
                sound=False
            )

if __name__ == '__main__':
    app = NotificationApp()
    app.run()
