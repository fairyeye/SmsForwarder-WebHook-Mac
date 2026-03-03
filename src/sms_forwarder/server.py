from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, unquote
import threading

APP_NAME_MAP = {
    'com.tencent.mm': '微信',
    'com.tencent.androidqqmail': 'QQ邮箱',
    'com.tencent.mobileqq': 'QQ',
    'com.alibaba.android.rimet': '钉钉',
    'com.ss.android.ugc.aweme': '抖音',
    'com.smartisanos.notes': '笔记',
    'com.android.mms': '短信',
    'com.miui.mms': '短信',
    'com.android.camera': '相机',
    'com.android.settings': '设置',
    'com.android.fileexplorer': '文件管理',
    'com.android.browser': '浏览器',
    'com.miui.weather': '天气',
    'com.android.calculator2': '计算器',
    'com.android.calendar': '日历',
    'com.android.deskclock': '时钟',
    'com.android.soundrecorder': '录音机',
    'com.android.fmradio': '收音机',
    'com.android.compass': '指南针',
    'com.UCMobile': 'UC浏览器',
    'com.tencent.mtt': 'QQ浏览器',
    'com.netease.cloudmusic': '网易云音乐',
    'com.tencent.qqmusic': 'QQ音乐',
    'com.qiyi.video': '爱奇艺',
    'com.tencent.qqlive': '腾讯视频',
    'com.moji.mjweather': '墨迹天气',
    'com.sohu.inputmethod.sogou': '搜狗输入法',
    'com.baidu.input': '百度输入法',
    'com.autonavi.amapauto': '高德地图',
    'com.baidu.BaiduMap': '百度地图',
    'com.taobao.taobao': '淘宝',
    'com.jingdong.app.mall': '京东',
    'com.eg.android.AlipayGphone': '支付宝',
    'com.sankuai.meituan': '美团',
    'com.alipay.android.app': '饿了么',
}

notification_callback = None

def get_app_name(package_name):
    # if package_name.isdigit() or package_name.startswith('+'):
    #     return f'短信 {package_name}'
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
