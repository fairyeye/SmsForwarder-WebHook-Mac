from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, unquote
import threading

APP_NAME_MAP = {
    'com.tencent.mm': '微信',
    'com.tencent.mobileqq': 'QQ',
    'com.alibaba.android.rimet': '钉钉',
    'com.ss.android.ugc.aweme': '抖音',
    'com.smartisanos.notes': '笔记',
    'com.android.mms': '短信',
    'com.miui.mms': '短信',
}

notification_callback = None

def get_app_name(package_name):
    if package_name.isdigit() or package_name.startswith('+'):
        return f'短信 {package_name}'
    return APP_NAME_MAP.get(package_name, package_name)

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

def start_server(port=19999, callback=None):
    global notification_callback
    notification_callback = callback
    
    server = HTTPServer(('0.0.0.0', port), NotificationServer)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    print(f"HTTP 服务运行在端口 {port}")
    return server
