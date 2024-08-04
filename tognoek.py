import sys
import os

if getattr(sys, 'frozen', False):
    # Chạy từ PyInstaller
    base_path = sys._MEIPASS
else:
    # Chạy từ mã nguồn
    base_path = os.path.dirname(__file__)

icon_path = os.path.join(base_path, 'data', 'icon.png')
print(icon_path)