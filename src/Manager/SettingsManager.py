import json
import os
import platform

class SettingsManager:
    """
    Quản lý việc tải và lưu cài đặt của game vào một file JSON.
    Sử dụng thiết kế Singleton để đảm bảo chỉ có một thể hiện duy nhất.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # Xác định đường dẫn file cấu hình trong thư mục dữ liệu người dùng
        # Điều này đảm bảo game có thể ghi file mà không cần quyền admin
        app_name = "CoCaro"

        if platform.system() == "Windows":
            # %APPDATA%
            pref_path = os.path.join(os.environ['APPDATA'], app_name)
        elif platform.system() == "Darwin":
            # ~/Library/Application Support
            pref_path = os.path.join(os.path.expanduser('~/Library/Application Support'), app_name)
        else:
            # ~/.local/share (Linux, XDG Base Directory Specification)
            pref_path = os.path.join(os.path.expanduser('~/.local/share'), app_name)

        self.config_file = os.path.join(pref_path, 'settings.json')

        # Các giá trị mặc định
        self.defaults = {
            'fullscreen': False,
            'board_size': 20,
            'music_volume': 0.5,  # Âm lượng mặc định 50%
            'sfx_volume': 0.7     # Âm lượng SFX mặc định 70%
        }
        self.settings = self.defaults.copy()
        self.load_settings()

    def load_settings(self):
        """Tải cài đặt từ file JSON. Nếu file không tồn tại hoặc lỗi, sử dụng giá trị mặc định."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Đảm bảo tất cả các key mặc định đều tồn tại
                    self.settings.update(loaded_settings)
        except (json.JSONDecodeError, IOError):
            print("Lỗi đọc file settings.json. Sử dụng cài đặt mặc định.")
            self.settings = self.defaults.copy()
        self.save_settings() # Lưu lại để tạo file nếu chưa có hoặc cập nhật key mới

    def save_settings(self):
        """Lưu cài đặt hiện tại vào file JSON."""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key):
        """Lấy một giá trị cài đặt."""
        return self.settings.get(key, self.defaults.get(key))

    def set(self, key, value):
        """Thiết lập một giá trị cài đặt và lưu ngay lập tức."""
        self.settings[key] = value
        self.save_settings()