import pygame
import os

from ui.InfoPanel import InfoPanel

class vsAiInfoPanel(InfoPanel):
    """
    Lớp này chịu trách nhiệm vẽ bảng thông tin người chơi ở bên cạnh màn hình.
    """
    def __init__(self, rect, player_names, x_img, o_img):
        self.rect = rect
        self.player_names = player_names
        
        # Tạo phiên bản ảnh nhỏ hơn cho panel
        super().__init__(rect, player_names, x_img, o_img)
        
        # Tải và thay đổi kích thước ảnh đại diện người chơi
        player_icon_size = 100
        self.ai_icon_img = pygame.image.load(os.path.join('img', 'Computer.png')).convert_alpha() # Ảnh đại diện cho máy
        self.ai_icon_img = pygame.transform.smoothscale(self.ai_icon_img, (player_icon_size, player_icon_size))
        
    def _get_player_icon(self, player_name):
        return self.ai_icon_img if player_name == "Máy tính" else self.player_icon_img

    def draw(self, screen, current_player, remaining_times, time_mode, paused):
        # Vẽ nền panel
        pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # Tính toán vị trí và kích thước cho khu vực của mỗi người chơi
        area_width = self.rect.width - 20
        # Tăng chiều cao để có đủ không gian cho icon 120x120 và các thông tin khác
        area_height = 300 
        margin_from_center = 10
        # Dịch chuyển đường kẻ lên một chút để cân bằng với nút Pause ở dưới
        divider_y = self.rect.centery - 60
        
        # --- Khu vực người chơi (Player) ---
        p1_y = divider_y - margin_from_center - area_height
        p1_area = pygame.Rect(self.rect.x + 10, p1_y, area_width, area_height)
        self._draw_player_info(screen, 'X', self.player_names['X'], remaining_times['X'], current_player == 'X', time_mode, p1_area, self._get_player_icon(self.player_names['X']))

        # --- Vẽ đường phân cách ---
        pygame.draw.line(screen, self.divider_color, (self.rect.x + 20, divider_y), (self.rect.right - 20, divider_y), 2)

        # --- Khu vực AI (Máy tính) ---
        p2_y = divider_y + margin_from_center
        p2_area = pygame.Rect(self.rect.x + 10, p2_y, area_width, area_height)
        self._draw_player_info(screen, 'O', self.player_names['O'], remaining_times['O'], current_player == 'O', time_mode, p2_area, self._get_player_icon(self.player_names['O']))

        # --- Vẽ nút Tạm dừng/Tiếp tục (sử dụng hình ảnh) ---
        pygame.draw.circle(screen, self.pause_button_bg_color, self.pause_button_rect.center, self.pause_button_rect.width // 2) # Nền vàng
        pygame.draw.circle(screen, self.pause_button_border_color, self.pause_button_rect.center, self.pause_button_rect.width // 2, 3) # Viền xám
        if paused:
            screen.blit(self.play_img, self.play_img.get_rect(center=self.pause_button_rect.center))
        else:
            screen.blit(self.pause_img, self.pause_img.get_rect(center=self.pause_button_rect.center))