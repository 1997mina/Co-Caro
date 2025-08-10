import pygame

class ScoreIndicator:
    """
    Lớp quản lý việc vẽ khu vực hiển thị tỉ số trong InfoPanel.
    Bao gồm các ô vuông, tỉ số dạng số, và quân cờ của người thắng ván gần nhất.
    """
    def __init__(self, rect, font_title, font_score, colors, x_img, o_img):
        self.rect = rect
        self.font_title = font_title
        self.font_score = font_score
        
        # Giải nén màu sắc
        self.text_color = colors['text']
        self.fill_color = colors['fill']
        self.border_color = colors['border']
        
        # Lưu trữ hình ảnh quân cờ đã được thu nhỏ
        self.x_img = x_img
        self.o_img = o_img

        self.box_size = 40
        self.box_spacing = 10

    def draw(self, screen, match_history, total_rounds=5):
        """
        Vẽ toàn bộ khu vực hiển thị tỉ số.
        :param match_history: Một danh sách chứa những người thắng của các ván trước, ví dụ: ['X', 'O', 'X'].
        """
        # Vẽ tiêu đề "Lịch sử đấu"
        title_surf = self.font_title.render("Lịch sử đấu", True, self.text_color)
        title_rect = title_surf.get_rect(centerx=self.rect.centerx, y=self.rect.y)
        screen.blit(title_surf, title_rect)

        # Tính toán vị trí để căn giữa 5 ô
        total_boxes_width = (total_rounds * self.box_size) + ((total_rounds - 1) * self.box_spacing)
        start_x = self.rect.centerx - total_boxes_width / 2

        for i in range(total_rounds):
            box_rect = pygame.Rect(start_x + i * (self.box_size + self.box_spacing), self.rect.y + 35, self.box_size, self.box_size)
            # Luôn vẽ viền cho ô
            pygame.draw.rect(screen, self.border_color, box_rect, 2, border_radius=4)

            # Nếu có lịch sử cho ô này, vẽ quân cờ của người thắng
            if i < len(match_history):
                winner_char = match_history[i]
                icon_img = self.x_img if winner_char == 'X' else self.o_img
                icon_scaled = pygame.transform.smoothscale(icon_img, (self.box_size - 12, self.box_size - 12))
                icon_rect = icon_scaled.get_rect(center=box_rect.center)
                screen.blit(icon_scaled, icon_rect)