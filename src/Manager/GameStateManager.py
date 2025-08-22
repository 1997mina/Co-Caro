class GameStateManager:
    """
    Quản lý các trạng thái chính của game như: đang chạy, tạm dừng, kết thúc.
    """
    def __init__(self):
        self.game_over = False
        self.paused = False

    def is_playing(self):
        """Kiểm tra xem game có đang trong trạng thái chơi được không."""
        # Game đang chơi khi không tạm dừng và chưa kết thúc
        return not self.paused and not self.game_over

    def is_paused(self):
        """Kiểm tra xem game có đang tạm dừng không."""
        return self.paused

    def set_game_over(self, status):
        """Đặt trạng thái kết thúc game."""
        self.game_over = status

    def toggle_pause(self, timer):
        """Bật/tắt trạng thái tạm dừng và điều khiển bộ đếm thời gian."""
        self.paused = not self.paused
        if self.paused:
            timer.pause()
        else:
            timer.resume()

    def handle_event(self, event, timer, board):
        """
        Xử lý các sự kiện liên quan đến trạng thái game.
        Phương thức này không còn xử lý sự kiện click nút, vì logic đó đã được
        chuyển đến GameSession để đảm bảo hoạt động nhất quán.
        """
        return False # Luôn trả về False để GameSession có thể xử lý sự kiện.

    def draw_overlay(self):
        """Vẽ lớp phủ khi game tạm dừng. Hiện tại chức năng này không hoạt động."""
        pass

    def reset(self):
        """Thiết lập lại trạng thái để bắt đầu ván mới."""
        self.game_over = False
        self.paused = False