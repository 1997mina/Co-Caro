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
        self.font_turn = pygame.font.SysFont("Times New Roman", 22, italic=True)
        
        # Colors
        self.bg_color = (240, 240, 240)
        self.text_color = (30, 30, 30)
        self.highlight_color = (200, 255, 200) # Màu xanh lá cây nhạt
        self.divider_color = (200, 200, 200)

    def draw(self, screen, current_player):
        # Vẽ nền panel
        pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # Tính toán vị trí các thành phần để cân đối
        area_height = 180
        area_width = self.rect.width - 20
        margin_from_center = 40 # Khoảng cách từ đường kẻ giữa đến khu vực thông tin
        divider_y = self.rect.centery

        # --- Vẽ thông tin người chơi 1 (X) ---
        p1_y = divider_y - margin_from_center - area_height
        p1_area = pygame.Rect(self.rect.x + 10, p1_y, area_width, area_height)
        if current_player == 'X':
            pygame.draw.rect(screen, self.highlight_color, p1_area, border_radius=10)
        
        p1_name_surf = self.font_name.render(self.player_names['X'], True, self.text_color)
        screen.blit(p1_name_surf, p1_name_surf.get_rect(centerx=self.rect.centerx, y=p1_area.y + 20))
        screen.blit(self.x_img, self.x_img.get_rect(centerx=self.rect.centerx, y=p1_area.y + 60))
        if current_player == 'X':
            turn_surf_p1 = self.font_turn.render("Lượt của bạn!", True, self.text_color)
            screen.blit(turn_surf_p1, turn_surf_p1.get_rect(centerx=self.rect.centerx, y=p1_area.y + 125))

        # --- Vẽ đường phân cách ---
        pygame.draw.line(screen, self.divider_color, (self.rect.x + 20, divider_y), (self.rect.right - 20, divider_y), 2)

        # --- Vẽ thông tin người chơi 2 (O) ---
        p2_y = divider_y + margin_from_center
        p2_area = pygame.Rect(self.rect.x + 10, p2_y, area_width, area_height)
        if current_player == 'O':
            pygame.draw.rect(screen, self.highlight_color, p2_area, border_radius=10)
        
        p2_name_surf = self.font_name.render(self.player_names['O'], True, self.text_color)
        screen.blit(p2_name_surf, p2_name_surf.get_rect(centerx=self.rect.centerx, y=p2_area.y + 20))
        screen.blit(self.o_img, self.o_img.get_rect(centerx=self.rect.centerx, y=p2_area.y + 60))
        if current_player == 'O':
            turn_surf_p2 = self.font_turn.render("Lượt của bạn!", True, self.text_color)
            screen.blit(turn_surf_p2, turn_surf_p2.get_rect(centerx=self.rect.centerx, y=p2_area.y + 125))