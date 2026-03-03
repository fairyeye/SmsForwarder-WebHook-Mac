from setuptools import setup
import os

APP = ['src/sms_forwarder/main.py']
ICON_FILE = 'src/sms_forwarder/notification-icon.icns'
ICON_PNG = 'src/sms_forwarder/notification-icon.png'
DATA_FILES = [('Resources', [ICON_FILE, ICON_PNG])]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
        'CFBundleIdentifier': 'com.notification.receiver',
        'CFBundleName': '通知接收器',
        'CFBundleDisplayName': '通知接收器',
        'CFBundleIconFile': 'notification-icon.icns',
        'CFBundleShortVersionString': '1.0.1',
        'CFBundleVersion': '1.0.1',
        'NSHumanReadableCopyright': '© 2026. All rights reserved.',
    },
    'packages': ['rumps', 'pyperclip', 'sms_forwarder'],
    'resources': [
        'src/sms_forwarder/notification-icon.icns',
        'src/sms_forwarder/notification-icon.png',
        'src/sms_forwarder/server.py',
        'src/sms_forwarder/history.py'
    ],
    'includes': ['rumps', 'pyperclip'],
    'excludes': ['unittest', 'test', 'setuptools'],
    'bdist_base': 'build',
    'dist_dir': 'dist',
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    packages=['sms_forwarder'],
    package_dir={'sms_forwarder': 'src/sms_forwarder'},
)
