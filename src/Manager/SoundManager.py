import pygame
import os

from manager.SettingsManager import SettingsManager
from utils.ResourcePath import resource_path

class SoundManager:
    """
    Quản lý việc tải và phát âm thanh, nhạc nền.
    Sử dụng thiết kế Singleton để đảm bảo chỉ có một thể hiện duy nhất.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
            # Thêm biến để theo dõi bản nhạc đang phát
            cls._instance._current_music = None
        return cls._instance

    def __init__(self):
        """
        Khởi tạo SoundManager, tải tất cả các file âm thanh cần thiết.
        Việc này chỉ chạy một lần.
        """
        if self._initialized:
            return
        self._initialized = True

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        except pygame.error as e:
            print(f"Lỗi: Không thể khởi tạo pygame.mixer: {e}")
            return

        self.sounds = {
            'move_X': self._load_sound('MoveX.mp3', volume=0.7),
            'move_O': self._load_sound('MoveO.mp3', volume=0.7),
            'checkbox_click': self._load_sound('CheckBox.mp3', volume=0.6),
            'game_over': self._load_sound('GameOver.mp3', volume=0.8),
            'button_click': self._load_sound('ButtonClick.mp3', volume=0.6),
        }

        # Định nghĩa các bản nhạc khác nhau
        self.music_tracks = {
            'menu': 'BackgroundMusic.mp3', # Nhạc cho menu
            'game': 'BackgroundMusic.mp3'  # Sử dụng lại nhạc nền cho ván chơi
        }

        self.settings_manager = SettingsManager()
        # Phát nhạc cho menu ngay khi khởi tạo lần đầu
        self.play_music('menu')


    def _load_sound(self, filename, volume=1.0):
        """
        Hàm trợ giúp để tải một file âm thanh từ thư mục 'sfx'.
        Trả về một đối tượng Sound giả nếu không tìm thấy file.
        """
        path = resource_path(os.path.join('sound', filename))
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        except pygame.error as e:
            print(f"Lỗi: Không thể tải file âm thanh '{path}'. {e}")
            return pygame.mixer.Sound(buffer=b'')

    def play_music(self, track_key, loop=-1, force_replay=False):
        """
        Phát một bản nhạc nền cụ thể. Sẽ không làm gì nếu bản nhạc đó đang phát.
        :param track_key: Key của bản nhạc trong self.music_tracks (ví dụ: 'menu', 'game').
        :param loop: Số lần lặp (-1 là vô hạn).
        :param force_replay: Nếu True, sẽ phát lại bản nhạc từ đầu ngay cả khi nó đang phát.
        """
        if track_key not in self.music_tracks:
            print(f"Cảnh báo: Không tìm thấy track nhạc với key '{track_key}'")
            return

        # Nếu không bắt buộc phát lại, và nhạc đang phát đúng bản nhạc được yêu cầu, thì không làm gì cả
        if not force_replay and self._current_music == track_key and pygame.mixer.music.get_busy():
            return

        try:
            music_filename = self.music_tracks[track_key]
            music_path = resource_path(os.path.join('sound', music_filename))
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                volume = self.settings_manager.get('music_volume')
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loop)
                self._current_music = track_key  # Cập nhật track đang phát
            else:
                print(f"Cảnh báo: Không tìm thấy file nhạc nền tại: {music_path}")
                self._current_music = None
        except pygame.error as e:
            print(f"Lỗi khi tải hoặc phát nhạc '{track_key}': {e}")
            self._current_music = None

    def play_move(self, player):
        """Phát âm thanh khi đi cờ của người chơi cụ thể (X hoặc O)."""
        self.sounds[f'move_{player}'].play()

    def play_game_over(self):
        """Phát âm thanh khi game kết thúc."""
        self.sounds['game_over'].play()

    def play_button_click(self):
        """Phát âm thanh khi nhấn nút."""
        self.sounds['button_click'].play()

    def play_sfx(self, sfx_name):
        """Phát một hiệu ứng âm thanh chung."""
        if sfx_name in self.sounds:
            self.sounds[sfx_name].play()
        else:
            print(f"Cảnh báo: Không tìm thấy âm thanh '{sfx_name}'")

    def set_music_volume(self, volume, save_setting=True):
        """
        Đặt âm lượng nhạc nền và tùy chọn lưu cài đặt.
        Volume là một số float từ 0.0 đến 1.0.
        """
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(volume)
            if save_setting:
                self.settings_manager.set('music_volume', volume)