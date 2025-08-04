import pygame
import os

class InfoPanel:
    """
    Lớp cơ sở (cha) cho các bảng thông tin.
    Chứa các thuộc tính và phương thức chung để vẽ thông tin người chơi,
    bộ đếm thời gian, và các nút điều khiển.
    """
    def __init__(self, rect, player_names, x_img, o_img):
        self.rect = rect
        self.player_names = player_names
        
        # Tạo phiên bản ảnh nhỏ hơn cho panel
        icon_size = 50
        self.x_img = pygame.transform.smoothscale(x_img, (icon_size, icon_size))
        self.o_img = pygame.transform.smoothscale(o_img, (icon_size, icon_size))
        
        # Tải và thay đổi kích thước ảnh đại diện người chơi mặc định
        player_icon_size = 100
        self.player_icon_img = pygame.image.load(os.path.join('img', 'Player.png')).convert_alpha()
        self.player_icon_img = pygame.transform.smoothscale(self.player_icon_img, (player_icon_size, player_icon_size))
        
        # Fonts
        self.font_name = pygame.font.SysFont("Times New Roman", 32, bold=True)
        self.font_total_time_label = pygame.font.SysFont("Times New Roman", 24)
        self.font_turn = pygame.font.SysFont("Times New Roman", 24, italic=True)
        self.font_timer = pygame.font.SysFont("Arial", 42, bold=True)
        self.font_button = pygame.font.SysFont("Times New Roman", 24, bold=True)
        
        # Colors
        self.bg_color = (240, 240, 240)
        self.text_color = (30, 30, 30)
        self.highlight_color = (112, 204, 225) # Màu xanh nước biển nhạt
        self.divider_color = (200, 200, 200)
        self.timer_color = (60, 60, 60)
        self.timer_warning_color = (211, 47, 47) # Màu đỏ cảnh báo
        self.timer_inactive_color = (150, 150, 150) # Màu xám cho đồng hồ không hoạt động
        self.pause_button_bg_color = (255, 255, 0) # Màu vàng cho nền nút tạm dừng
        self.pause_button_border_color = (128, 128, 128) # Màu xám cho viền nút tạm dừng

        # Nút tạm dừng (sử dụng hình ảnh)
        self.pause_img = pygame.image.load(os.path.join('img', 'Pause.png')).convert_alpha()
        self.play_img = pygame.image.load(os.path.join('img', 'Play.png')).convert_alpha()
        self.button_img_size = 60
        self.pause_img = pygame.transform.scale(self.pause_img, (self.button_img_size, self.button_img_size))
        self.play_img = pygame.transform.scale(self.play_img, (self.button_img_size, self.button_img_size))
        
        # Tạo rect cho nút tạm dừng với kích thước và vị trí cố định
        self.pause_button_rect = pygame.Rect(0, 0, self.button_img_size + 20, self.button_img_size + 20) # Thêm padding cho viền, sẽ dùng cho hình tròn
        self.pause_button_rect.center = (self.rect.centerx, self.rect.height - 80)

    def _draw_player_avatar(self, screen, player_name, player_area, y_cursor):
        """Vẽ ảnh đại diện mặc định cho người chơi. Lớp con có thể ghi đè."""
        player_icon_rect = self.player_icon_img.get_rect(centerx=player_area.centerx, top=y_cursor)
        screen.blit(self.player_icon_img, player_icon_rect)
        return player_icon_rect.bottom

    def _draw_player_info(self, screen, player_char, player_name, player_time, is_current_player, time_mode, player_area):
        """Vẽ thông tin cho một người chơi cụ thể trong khu vực được chỉ định."""
        if is_current_player:
            pygame.draw.rect(screen, self.highlight_color, player_area, border_radius=10)
        
        y_cursor = player_area.y + 10

        # 1. Icon người chơi (gọi phương thức riêng để lớp con có thể tùy chỉnh)
        y_cursor = self._draw_player_avatar(screen, player_name, player_area, y_cursor)

        # 2. Tên người chơi
        name_surf = self.font_name.render(player_name, True, self.text_color)
        name_rect = name_surf.get_rect(centerx=player_area.centerx, top=y_cursor)
        screen.blit(name_surf, name_rect)
        y_cursor = name_rect.bottom + 15

        # 3. Biểu tượng X/O
        icon_img = self.x_img if player_char == 'X' else self.o_img
        icon_rect = icon_img.get_rect(centerx=player_area.centerx, top=y_cursor)
        screen.blit(icon_img, icon_rect)

        y_cursor_bottom = player_area.bottom - 5

        # 4. Vẽ bộ đếm thời gian
        # Chỉ vẽ đồng hồ cho chế độ 'total_time' hoặc cho người chơi hiện tại trong chế độ 'turn_based'
        if time_mode == "total_time" or (time_mode == "turn_based" and is_current_player):
            timer_color = self.timer_color # Màu mặc định

            if player_time == float('inf'):
                timer_text = ""
            else:
                warning_threshold = 30 if time_mode == "total_time" else 10
                
                seconds = max(0, int(player_time))
                minutes = seconds // 60
                seconds_display = seconds % 60
                timer_text = f"{minutes:01d}:{seconds_display:02d}"

                if time_mode == "total_time" and not is_current_player:
                    timer_color = self.timer_inactive_color
                else:
                    timer_color = self.timer_warning_color if player_time < warning_threshold else self.timer_color

            timer_surf = self.font_timer.render(timer_text, True, timer_color)
            timer_rect = timer_surf.get_rect(centerx=player_area.centerx, bottom=y_cursor_bottom)
            screen.blit(timer_surf, timer_rect)
            y_cursor_bottom = timer_rect.top - 1

        # 5. Thông báo lượt chơi
        if is_current_player: # Kiểm tra xem đây có phải là người chơi hiện tại không
            # Kiểm tra nếu tên người chơi là "Máy tính" thì hiển thị thông báo khác
            if player_name == "Máy tính":
                turn_surf = self.font_turn.render("Máy đang suy nghĩ...", True, self.text_color)
            else:
                turn_surf = self.font_turn.render("Đến lượt bạn!", True, self.text_color)

            turn_rect = turn_surf.get_rect(centerx=player_area.centerx, bottom=y_cursor_bottom)
            screen.blit(turn_surf, turn_rect)

    def draw(self, screen, current_player, remaining_times, time_mode, paused):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        
        area_width = self.rect.width - 20
        area_height = 300 
        margin_from_center = 10
        divider_y = self.rect.centery - 60
        
        # --- Khu vực người chơi 1 ---
        p1_y = divider_y - margin_from_center - area_height
        p1_area = pygame.Rect(self.rect.x + 10, divider_y - margin_from_center - area_height, area_width, area_height)
        self._draw_player_info(screen, 'X', self.player_names['X'], remaining_times['X'], current_player == 'X', time_mode, p1_area)

        # --- Vẽ đường phân cách ---
        pygame.draw.line(screen, self.divider_color, (self.rect.x + 20, divider_y), (self.rect.right - 20, divider_y), 2)

        # --- Khu vực người chơi 2 ---
        p2_y = divider_y + margin_from_center
        p2_area = pygame.Rect(self.rect.x + 10, p2_y, area_width, area_height)
        self._draw_player_info(screen, 'O', self.player_names['O'], remaining_times['O'], current_player == 'O', time_mode, p2_area)

        # --- Vẽ nút Tạm dừng/Tiếp tục (sử dụng hình ảnh) ---
        pygame.draw.circle(screen, self.pause_button_bg_color, self.pause_button_rect.center, self.pause_button_rect.width // 2)
        pygame.draw.circle(screen, self.pause_button_border_color, self.pause_button_rect.center, self.pause_button_rect.width // 2, 3)
        if paused:
            screen.blit(self.play_img, self.play_img.get_rect(center=self.pause_button_rect.center))
        else:
            screen.blit(self.pause_img, self.pause_img.get_rect(center=self.pause_button_rect.center))
