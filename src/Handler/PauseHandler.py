import pygame

class PauseHandler:
    """
    Lớp này chịu trách nhiệm xử lý tất cả logic và giao diện
    liên quan đến việc tạm dừng game.
    """
    def __init__(self, screen, board_rect):
        """
        Khởi tạo trình xử lý tạm dừng.
        :param screen: Bề mặt màn hình chính để vẽ lên.
        :param board_rect: Hình chữ nhật xác định khu vực bàn cờ để vẽ lớp phủ.
        """
        self.screen = screen
        self.board_rect = board_rect
        self.paused = False
        # Các thành phần đồ họa đã được loại bỏ vì màn hình tạm dừng không còn hiển thị.

    def is_paused(self):
        """Trả về trạng thái tạm dừng hiện tại."""
        return self.paused

    def toggle(self, timer):
        """Bật/tắt trạng thái tạm dừng và điều khiển bộ đếm thời gian."""
        self.paused = not self.paused
        if self.paused:
            timer.pause()
        else:
            timer.resume()

    def draw(self):
        """Vẽ lớp phủ khi game tạm dừng. Chức năng này đã bị vô hiệu hóa."""
        pass

    def reset(self):
        """Thiết lập lại trạng thái tạm dừng cho ván mới."""
        self.paused = False
