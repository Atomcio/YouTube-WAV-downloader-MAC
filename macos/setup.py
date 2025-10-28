from setuptools import setup

APP = ['ytwav_gui.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'includes': ['yt_dlp'],
    'plist': {
        'CFBundleName': 'YTWAV',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'CFBundleIdentifier': 'com.atomcio.ytwav',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
)