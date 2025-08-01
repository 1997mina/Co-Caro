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

        # Tạo các thành phần đồ họa cho màn hình tạm dừng, chỉ tạo một lần
        self.overlay = pygame.Surface(self.board_rect.size, pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))  # Màu đen, bán trong suốt
        self.font = pygame.font.SysFont("Times New Roman", 80, bold=True)
        self.text = self.font.render("Đã tạm dừng", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=self.board_rect.center)

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
        """Vẽ lớp phủ và chữ nếu game đang ở trạng thái tạm dừng."""
        if self.paused:
            self.screen.blit(self.overlay, self.board_rect.topleft)
            self.screen.blit(self.text, self.text_rect)

    def reset(self):
        """Thiết lập lại trạng thái tạm dừng cho ván mới."""
        self.paused = False
