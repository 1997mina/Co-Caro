import pygame
from ui.general.InfoPanel import InfoPanel

class TwoPlayerInfoPanel(InfoPanel):
    """
    Lớp này chịu trách nhiệm vẽ bảng thông tin người chơi ở bên cạnh màn hình.
    """
    def __init__(self, rect, player_names, x_img, o_img):
        super().__init__(rect, player_names, x_img, o_img)

        # Xác định các nút sẽ được hiển thị trong chế độ này (không có nút Gợi ý)
        self.highlight_color = (112, 204, 225) # Màu xanh nước biển nhạt
        self.buttons_to_layout = [self.settings_button, self.quit_button]

        self.font_time_mode = pygame.font.SysFont("Times New Roman", 24, bold=True)

    def _get_vietnamese_time_mode(self, time_mode_en):
        """Chuyển đổi chế độ thời gian tiếng Anh sang tiếng Việt."""
        if time_mode_en == 'turn_based':
            return '20 giây Theo lượt'
        elif time_mode_en == 'total_time':
            return '2 phút Tổng cộng'
        elif time_mode_en == 'no_time':
            return 'Không giới hạn'
        return time_mode_en

    def draw(self, screen, current_player, remaining_times, time_mode, paused, winning_cells=None, last_move=None, match_history=None, difficulty=None):
        # Gọi phương thức draw của lớp cha, nó sẽ tự động vẽ các nút trong buttons_to_layout
        super().draw(screen, current_player, remaining_times, time_mode, paused, winning_cells, last_move, match_history, difficulty)

        # Hiển thị chế độ thời gian
        mode_text = f"Chế độ: {self._get_vietnamese_time_mode(time_mode)}"
        mode_surf = self.font_time_mode.render(mode_text, True, self.text_color)
        mode_rect = mode_surf.get_rect(centerx=self.rect.centerx, y=self.score_indicator.rect.y - mode_surf.get_height() - 10)
        screen.blit(mode_surf, mode_rect)