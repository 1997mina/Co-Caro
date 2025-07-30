import pygame

class TurnTimer:
    """
    Lớp quản lý bộ đếm thời gian cho mỗi lượt đi.
    """
    def __init__(self, time_limit_seconds):
        """
        Khởi tạo bộ đếm với giới hạn thời gian cho mỗi lượt.
        :param time_limit_seconds: Giới hạn thời gian (tính bằng giây).
        """
        self.time_limit = time_limit_seconds
        self.start_ticks = 0

    def start_turn(self):
        """Bắt đầu hoặc đặt lại bộ đếm cho một lượt mới."""
        self.start_ticks = pygame.time.get_ticks()

    def get_remaining_time(self):
        """
        Lấy thời gian còn lại của lượt hiện tại.
        :return: Thời gian còn lại (tính bằng giây).
        """
        elapsed_seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        remaining = self.time_limit - elapsed_seconds
        return max(0, remaining)

    def is_time_up(self):
        """
        Kiểm tra xem thời gian cho lượt hiện tại đã hết chưa.
        :return: True nếu hết giờ, False nếu còn thời gian.
        """
        return self.get_remaining_time() <= 0

