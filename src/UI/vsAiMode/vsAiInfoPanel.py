import pygame

from utils.ResourcePath import resource_path
from ui.general.InfoPanel import InfoPanel

class vsAiInfoPanel(InfoPanel):
    """
    Lớp này chịu trách nhiệm vẽ bảng thông tin người chơi ở bên cạnh màn hình.
    """
    def __init__(self, rect, player_names, x_img, o_img):
        # Gọi constructor của lớp cha để khởi tạo các thuộc tính chung
        super().__init__(rect, player_names, x_img, o_img)
        self.highlight_color = (255, 213, 79) # Màu vàng nhạt
        self.buttons_to_layout = [self.hint_button, self.pause_button, self.quit_button]

        # Tải và thay đổi kích thước ảnh đại diện người chơi
        player_icon_size = 90
        self.ai_icon_img = pygame.image.load(resource_path('img/ingame/Computer.png')).convert_alpha() # Ảnh đại diện cho máy
        self.ai_icon_img = pygame.transform.smoothscale(self.ai_icon_img, (player_icon_size, player_icon_size))

    def _get_player_icon(self, player_name):
        """Trả về ảnh đại diện phù hợp cho người chơi, bao gồm cả AI."""
        if player_name == "Máy tính":
            return self.ai_icon_img
        return self.player_icon_img

    def draw(self, screen, current_player, remaining_times, time_mode, paused, winning_cells=None, last_move=None, match_history=None):
        # Gọi phương thức draw của lớp cha
        super().draw(screen, current_player, remaining_times, time_mode, paused, winning_cells, last_move, match_history)

        # Xác định người chơi là AI
        ai_player_char = 'X' if self.player_names['X'] == "Máy tính" else 'O'
        
        # Bật nút gợi ý nếu không tạm dừng và đang là lượt của người chơi
        self.hint_button.is_enabled = not paused and current_player != ai_player_char # Vô hiệu hóa nút gợi ý khi AI đang suy nghĩ