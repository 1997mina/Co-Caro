import sys
import os

def resource_path(relative_path):
    """
    Lấy đường dẫn tuyệt đối đến tài nguyên, hoạt động cho cả môi trường dev và PyInstaller.
    """
    try:
        # PyInstaller tạo một thư mục tạm thời và lưu đường dẫn trong sys._MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Nếu không phải PyInstaller, đường dẫn gốc là thư mục chứa file Main.py
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    return os.path.join(base_path, relative_path)