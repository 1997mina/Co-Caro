import pygame
from handler.PauseHandler import PauseHandler

class GameStateManager:
    """
    Quản lý các trạng thái chính của game như: đang chạy, tạm dừng, kết thúc.
    Sử dụng một PauseHandler để quản lý logic tạm dừng.
    """
    def __init__(self, screen, board_rect, sound_manager):
        self.game_over = False
        # Khởi tạo trình xử lý tạm dừng, ủy quyền các tác vụ liên quan cho nó
        self.pause_handler = PauseHandler(screen, board_rect)
        self.sound_manager = sound_manager

    def is_playing(self):
        """Kiểm tra xem game có đang trong trạng thái chơi được không."""
        # Game đang chơi khi không tạm dừng và chưa kết thúc
        return not self.pause_handler.is_paused() and not self.game_over

    def is_paused(self):
        """Kiểm tra xem game có đang tạm dừng không (ủy quyền cho PauseHandler)."""
        return self.pause_handler.is_paused()

    def set_game_over(self, status):
        """Đặt trạng thái kết thúc game."""
        self.game_over = status

    def toggle_pause(self, timer):
        """Bật/tắt trạng thái tạm dừng (ủy quyền cho PauseHandler)."""
        self.pause_handler.toggle(timer)

    def handle_event(self, event, timer, board):
        """Xử lý các sự kiện liên quan đến trạng thái game (ví dụ: click nút tạm dừng)."""
        # Chỉ xử lý sự kiện tạm dừng khi game chưa kết thúc
        if not self.game_over and board.player_info_panel.pause_button.handle_event(event):
            self.toggle_pause(timer)
            return True # Sự kiện đã được xử lý
        return False # Sự kiện chưa được xử lý

    def draw_overlay(self):
        """Vẽ lớp phủ và chữ khi game tạm dừng (ủy quyền cho PauseHandler)."""
        self.pause_handler.draw()

    def reset(self):
        """Thiết lập lại trạng thái để bắt đầu ván mới."""
        self.game_over = False
        self.pause_handler.reset()