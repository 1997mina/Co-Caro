import pygame
import os

class SoundManager:
    """
    Lớp quản lý việc tải và phát các hiệu ứng âm thanh trong game.
    """
    def __init__(self):
        """
        Khởi tạo SoundManager, tải tất cả các file âm thanh cần thiết.
        """
        # Khởi tạo mixer nếu nó chưa được khởi tạo
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        self.sounds = {
            'move_X': self._load_sound('MoveX.mp3', volume=0.7),
            'move_O': self._load_sound('MoveO.mp3', volume=0.7),
            'game_over': self._load_sound('GameOver.mp3', volume=0.8),
            'button_click': self._load_sound('ButtonClick.mp3', volume=0.6)
        }

    def _load_sound(self, filename, volume=1.0):
        """
        Hàm trợ giúp để tải một file âm thanh từ thư mục 'sfx'.
        Trả về một đối tượng Sound giả nếu không tìm thấy file.
        """
        path = os.path.join('sound', filename)
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        except pygame.error as e:
            print(f"Lỗi: Không thể tải file âm thanh '{path}'. {e}")
            # Trả về một đối tượng Sound "câm" để game không bị crash
            return pygame.mixer.Sound(buffer=b'')

    def play_move(self, player):
        """Phát âm thanh khi đi cờ của người chơi cụ thể (X hoặc O)."""
        self.sounds[f'move_{player}'].play()

    def play_game_over(self):
        """Phát âm thanh khi hết giờ."""
        self.sounds['game_over'].play()

    def play_button_click(self):
        """Phát âm thanh khi nhấn nút."""
        self.sounds['button_click'].play()