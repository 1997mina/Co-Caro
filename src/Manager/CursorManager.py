import pygame
from ui.components.InputBox import InputBox

class CursorManager:
    """
    Lớp quản lý việc thay đổi con trỏ chuột dựa trên các thành phần UI.
    Giúp tách biệt logic xử lý con trỏ ra khỏi các màn hình cụ thể.
    """
    def __init__(self):
        self.clickable_areas = []  # Dành cho con trỏ HAND
        self.text_inputs = []      # Dành cho con trỏ IBEAM

    def add_clickable_area(self, rect, condition=True):
        """
        Đăng ký một khu vực (pygame.Rect) có thể click.
        Con trỏ sẽ chuyển thành hình bàn tay (HAND) khi di chuột qua.
        :param rect: Khu vực hình chữ nhật.
        :param condition: Điều kiện để khu vực này có hiệu lực (ví dụ: nút có được bật hay không).
        """
        if rect and condition:
            self.clickable_areas.append(rect)

    def add_text_input(self, input_box):
        """
        Đăng ký một ô nhập liệu (InputBox).
        Con trỏ sẽ chuyển thành dạng soạn thảo (IBEAM) khi di chuột qua.
        """
        if input_box:
            self.text_inputs.append(input_box)

    def update(self, mouse_pos):
        """
        Cập nhật con trỏ chuột. Hàm này nên được gọi mỗi frame.
        Ưu tiên con trỏ IBEAM hơn HAND.
        """
        # 1. Kiểm tra các ô nhập liệu trước
        for input_box in self.text_inputs:
            if input_box.rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                return # Đã xử lý, thoát sớm

        # 2. Nếu không phải ô nhập liệu, kiểm tra các khu vực có thể click
        for area in self.clickable_areas:
            if area.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                return # Đã xử lý, thoát sớm

        # 3. Nếu không có gì, đặt lại con trỏ mặc định
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)