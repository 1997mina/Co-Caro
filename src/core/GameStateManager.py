import pygame

class GameStateManager:
    """
    Quản lý các trạng thái chính của game như: đang chạy, tạm dừng, kết thúc.
    """
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.paused = False
        self.game_over = False
        
        # Fonts và overlay cho màn hình tạm dừng
        self.overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128)) # Màu đen, bán trong suốt
        self.pause_font = pygame.font.SysFont("Times New Roman", 80, bold=True)
        self.pause_text = self.pause_font.render("Đã tạm dừng", True, (255, 255, 255))
        self.pause_text_rect = self.pause_text.get_rect(center=self.screen_rect.center)

    def is_playing(self):
        """Kiểm tra xem game có đang trong trạng thái chơi được không."""
        return not self.paused and not self.game_over

    def is_paused(self):
        """Kiểm tra xem game có đang tạm dừng không."""
        return self.paused

    def set_game_over(self, status):
        """Đặt trạng thái kết thúc game."""
        self.game_over = status

    def toggle_pause(self, timer):
        """Bật/tắt trạng thái tạm dừng."""
        self.paused = not self.paused
        if self.paused:
            timer.pause()
        else:
            timer.resume()

    def handle_event(self, event, timer, board):
        """Xử lý các sự kiện liên quan đến trạng thái game (ví dụ: click nút tạm dừng)."""
        if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
            if board.player_info_panel.pause_button_rect.collidepoint(event.pos):
                self.toggle_pause(timer)
                return True # Sự kiện đã được xử lý
        return False # Sự kiện chưa được xử lý

    def draw_overlay(self):
        """Vẽ lớp phủ và chữ khi game tạm dừng."""
        if self.paused:
            self.screen.blit(self.overlay, (0, 0))
            self.screen.blit(self.pause_text, self.pause_text_rect)

    def reset(self):
        """Thiết lập lại trạng thái để bắt đầu ván mới."""
        self.paused = False
        self.game_over = False