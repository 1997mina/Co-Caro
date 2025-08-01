import pygame
import os

class PlayerInfoPanel:
    """
    Lớp này chịu trách nhiệm vẽ bảng thông tin người chơi ở bên cạnh màn hình.
    """
    def __init__(self, rect, player_names, x_img, o_img):
        self.rect = rect
        self.player_names = player_names
        
        # Tạo phiên bản ảnh nhỏ hơn cho panel
        icon_size = 50 # Tăng kích thước cho cân đối
        self.x_img = pygame.transform.smoothscale(x_img, (icon_size, icon_size))
        self.o_img = pygame.transform.smoothscale(o_img, (icon_size, icon_size))
        
        # Tải và thay đổi kích thước ảnh đại diện người chơi
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

    def _draw_player_info(self, screen, player_char, player_name, player_time, is_current_player, time_mode, player_area):
        """Vẽ thông tin cho một người chơi cụ thể trong khu vực được chỉ định."""
        if is_current_player:
            pygame.draw.rect(screen, self.highlight_color, player_area, border_radius=10)
        
        # --- Bố cục từ trên xuống cho các thành phần cố định ---
        y_cursor = player_area.y + 10  # Bắt đầu với một chút padding trên (giảm để có thêm không gian)

        # 1. Icon người chơi
        player_icon_rect = self.player_icon_img.get_rect(centerx=player_area.centerx, top=y_cursor)
        screen.blit(self.player_icon_img, player_icon_rect)
        y_cursor = player_icon_rect.bottom  # Di chuyển con trỏ xuống dưới icon (giảm padding)

        # 2. Tên người chơi
        name_surf = self.font_name.render(player_name, True, self.text_color)
        name_rect = name_surf.get_rect(centerx=player_area.centerx, top=y_cursor)
        screen.blit(name_surf, name_rect)
        y_cursor = name_rect.bottom + 15 # Giảm padding

        # 3. Biểu tượng X/O
        icon_img = self.x_img if player_char == 'X' else self.o_img
        icon_rect = icon_img.get_rect(centerx=player_area.centerx, top=y_cursor)
        screen.blit(icon_img, icon_rect)

        # --- Bố cục từ dưới lên cho các thành phần có điều kiện ---
        y_cursor_bottom = player_area.bottom - 5  # Bắt đầu từ dưới (giảm padding)

        # 4. Vẽ bộ đếm thời gian
        if time_mode == "total_time" or (time_mode == "turn_based" and is_current_player):
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
            y_cursor_bottom = timer_rect.top - 1  # Dịch con trỏ lên trên (giảm padding)
        
        # 5. Thông báo lượt chơi
        if is_current_player:
            turn_surf = self.font_turn.render("Đến lượt!", True, self.text_color) # Dùng text ngắn gọn hơn
            turn_rect = turn_surf.get_rect(centerx=player_area.centerx, bottom=y_cursor_bottom)
            screen.blit(turn_surf, turn_rect)

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
        
        # --- Khu vực người chơi 1 ---
        p1_y = divider_y - margin_from_center - area_height
        p1_area = pygame.Rect(self.rect.x + 10, p1_y, area_width, area_height)
        self._draw_player_info(screen, 'X', self.player_names['X'], remaining_times['X'], current_player == 'X', time_mode, p1_area)

        # --- Vẽ đường phân cách ---
        pygame.draw.line(screen, self.divider_color, (self.rect.x + 20, divider_y), (self.rect.right - 20, divider_y), 2)

        # --- Khu vực người chơi 2 ---
        p2_y = divider_y + margin_from_center
        p2_area = pygame.Rect(self.rect.x + 10, p2_y, area_width, area_height)
        self._draw_player_info(screen, 'O', self.player_names['O'], remaining_times['O'], current_player == 'O', time_mode, p2_area)

        # --- Vẽ nút Tạm dừng/Tiếp tục (sử dụng hình ảnh) ---
        pygame.draw.circle(screen, self.pause_button_bg_color, self.pause_button_rect.center, self.pause_button_rect.width // 2) # Nền vàng
        pygame.draw.circle(screen, self.pause_button_border_color, self.pause_button_rect.center, self.pause_button_rect.width // 2, 3) # Viền xám
        if paused:
            screen.blit(self.play_img, self.play_img.get_rect(center=self.pause_button_rect.center))
        else:
            screen.blit(self.pause_img, self.pause_img.get_rect(center=self.pause_button_rect.center))