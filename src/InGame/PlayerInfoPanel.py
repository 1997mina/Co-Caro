import pygame

class PlayerInfoPanel:
    """
    Lớp này chịu trách nhiệm vẽ bảng thông tin người chơi ở bên cạnh màn hình.
    """
    def __init__(self, rect, player_names, x_img, o_img):
        self.rect = rect
        self.player_names = player_names
        
        # Tạo phiên bản ảnh nhỏ hơn cho panel
        icon_size = 50
        self.x_img = pygame.transform.smoothscale(x_img, (icon_size, icon_size))
        self.o_img = pygame.transform.smoothscale(o_img, (icon_size, icon_size))
        
        # Fonts
        self.font_name = pygame.font.SysFont("Times New Roman", 28, bold=True)
        self.font_total_time_label = pygame.font.SysFont("Times New Roman", 22)
        self.font_turn = pygame.font.SysFont("Times New Roman", 22, italic=True)
        self.font_timer = pygame.font.SysFont("Arial", 42, bold=True)
        self.font_button = pygame.font.SysFont("Times New Roman", 24, bold=True)
        
        # Colors
        self.bg_color = (240, 240, 240)
        self.text_color = (30, 30, 30)
        self.highlight_color = (200, 255, 200) # Màu xanh lá cây nhạt
        self.divider_color = (200, 200, 200)
        self.timer_color = (60, 60, 60)
        self.timer_warning_color = (211, 47, 47) # Màu đỏ cảnh báo
        self.pause_button_color = (255, 193, 7) # Màu vàng

        # Nút tạm dừng
        self.pause_button_rect = pygame.Rect(self.rect.x + 30, self.rect.height - 80, self.rect.width - 60, 50)

    def draw(self, screen, current_player, remaining_times, time_mode, paused):
        # Lấy chế độ chơi từ Main.py (cần truyền vào hoặc lấy từ một biến toàn cục)
        # Vẽ nền panel
        pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # Tính toán vị trí các thành phần để cân đối
        area_height = 200
        area_width = self.rect.width - 20
        margin_from_center = 40 # Khoảng cách từ đường kẻ giữa đến khu vực thông tin
        divider_y = self.rect.centery
        
        # --- Vẽ thông tin người chơi 1 ---
        p1_y = divider_y - margin_from_center - area_height
        p1_area = pygame.Rect(self.rect.x + 10, p1_y, area_width, area_height)
        if current_player == 'X':
            pygame.draw.rect(screen, self.highlight_color, p1_area, border_radius=10)
            turn_surf_p1 = self.font_turn.render("Lượt của bạn!", True, self.text_color)
            screen.blit(turn_surf_p1, turn_surf_p1.get_rect(centerx=self.rect.centerx, y=p1_area.y + 110))
        
        p1_name_surf = self.font_name.render(self.player_names['X'], True, self.text_color)
        screen.blit(p1_name_surf, p1_name_surf.get_rect(centerx=self.rect.centerx, y=p1_area.y + 20))
        screen.blit(self.x_img, self.x_img.get_rect(centerx=self.rect.centerx, y=p1_area.y + 60))

        # Vẽ bộ đếm thời gian cho P1
        p1_time = remaining_times['X']
        seconds_p1 = max(0, int(p1_time))
        minutes_p1 = seconds_p1 // 60
        seconds_display_p1 = seconds_p1 % 60
        timer_text_p1 = f"{minutes_p1:01d}:{seconds_display_p1:02d}"
        
        warning_threshold = 30 if time_mode == "total_time" else 10
        timer_color_p1 = self.timer_warning_color if p1_time < warning_threshold else self.timer_color

        timer_surf_p1 = self.font_timer.render(timer_text_p1, True, timer_color_p1)
        screen.blit(timer_surf_p1, timer_surf_p1.get_rect(centerx=self.rect.centerx, y=p1_area.y + 140))

        # --- Vẽ đường phân cách ---
        pygame.draw.line(screen, self.divider_color, (self.rect.x + 20, divider_y), (self.rect.right - 20, divider_y), 2)

        # --- Vẽ thông tin người chơi 2 ---
        p2_y = divider_y + margin_from_center
        p2_area = pygame.Rect(self.rect.x + 10, p2_y, area_width, area_height)
        if current_player == 'O':
            pygame.draw.rect(screen, self.highlight_color, p2_area, border_radius=10)
            turn_surf_p2 = self.font_turn.render("Lượt của bạn!", True, self.text_color)
            screen.blit(turn_surf_p2, turn_surf_p2.get_rect(centerx=self.rect.centerx, y=p2_area.y + 110))
        
        p2_name_surf = self.font_name.render(self.player_names['O'], True, self.text_color)
        screen.blit(p2_name_surf, p2_name_surf.get_rect(centerx=self.rect.centerx, y=p2_area.y + 20))
        screen.blit(self.o_img, self.o_img.get_rect(centerx=self.rect.centerx, y=p2_area.y + 60))

        # Vẽ bộ đếm thời gian cho P2
        p2_time = remaining_times['O']
        seconds_p2 = max(0, int(p2_time))
        minutes_p2 = seconds_p2 // 60
        seconds_display_p2 = seconds_p2 % 60
        timer_text_p2 = f"{minutes_p2:01d}:{seconds_display_p2:02d}"

        timer_color_p2 = self.timer_warning_color if p2_time < warning_threshold else self.timer_color
        timer_surf_p2 = self.font_timer.render(timer_text_p2, True, timer_color_p2)
        screen.blit(timer_surf_p2, timer_surf_p2.get_rect(centerx=self.rect.centerx, y=p2_area.y + 140))

        # --- Vẽ nút Tạm dừng/Tiếp tục ---
        pygame.draw.rect(screen, self.pause_button_color, self.pause_button_rect, border_radius=10)
        if paused:
            button_text = "Tiếp tục"
        else:
            button_text = "Tạm dừng"
        
        button_surf = self.font_button.render(button_text, True, self.text_color)
        screen.blit(button_surf, button_surf.get_rect(center=self.pause_button_rect.center))