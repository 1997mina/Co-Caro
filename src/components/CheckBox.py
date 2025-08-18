import pygame

class CheckBox:
    """
    Lớp tạo ra một ô checkbox có thể tương tác trong Pygame.
    Bao gồm văn bản nhãn và xử lý sự kiện click.
    """
    def __init__(self, x, y, w, h, text, text_color, font_size, sound_manager, initial_state=False, check_image_path=None, text_spacing=15):
        """
        Khởi tạo CheckBox.
        :param x, y, w, h: Vị trí và kích thước của ô vuông.
        :param text: Văn bản nhãn hiển thị bên cạnh ô.
        :param text_color: Màu của văn bản nhãn.
        :param font_size: Kích thước font cho nhãn.
        :param sound_manager: Thể hiện của SoundManager để phát âm thanh.
        :param initial_state: Trạng thái ban đầu (True là đã chọn).
        :param check_image_path: (Tùy chọn) Đường dẫn đến ảnh cho trạng thái đã chọn.
        :param text_spacing: (Tùy chọn) Khoảng cách giữa ô và văn bản.
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.SysFont("Times New Roman", font_size) # Sử dụng font mặc định của Pygame
        self.text = text
        self.checked = initial_state
        self.text_spacing = text_spacing

        # Màu sắc
        self.text_color = text_color
        self.box_color_inactive = (200, 200, 200)
        self.box_color_active = (0, 120, 215)
        self.checkmark_color = (255, 255, 255)
        self.border_color = (100, 100, 100)

        # Tải và chuẩn bị hình ảnh cho dấu tick nếu có
        self.check_image = None
        if check_image_path:
            try:
                # Tải và co dãn ảnh để vừa với hộp, có một chút lề
                margin = 6
                img_size = (self.rect.width - margin * 2, self.rect.height - margin * 2)
                original_image = pygame.image.load(check_image_path).convert_alpha()
                self.check_image = pygame.transform.scale(original_image, img_size)
            except pygame.error as e:
                print(f"Lỗi khi tải ảnh cho checkbox: {e}")

        # Tạo surface cho văn bản để tối ưu hóa việc vẽ
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(left=self.rect.right + self.text_spacing, centery=self.rect.centery)

        self.sound_manager = sound_manager
        # Vùng có thể click bao gồm cả hộp và chữ, được tính một lần để tối ưu
        self.clickable_area = self.rect # Chỉ ô vuông là vùng click

    def handle_event(self, event):
        """
        Xử lý sự kiện click chuột.
        :param event: Sự kiện Pygame.
        :return: True nếu trạng thái thay đổi, False nếu không.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.clickable_area.collidepoint(event.pos):
                self.checked = not self.checked
                # Sử dụng tên âm thanh chính xác đã định nghĩa trong SoundManager
                self.sound_manager.play_sfx('checkbox_click')
                return True
        return False

    def draw(self, screen):
        """
        Vẽ checkbox và nhãn lên màn hình.
        :param screen: Bề mặt Pygame để vẽ lên.
        """
        # Vẽ hộp
        if self.checked:
            pygame.draw.rect(screen, self.box_color_active, self.rect, border_radius=3)
            # Vẽ dấu tick: ưu tiên dùng ảnh, nếu không có thì vẽ đường thẳng
            if self.check_image:
                img_rect = self.check_image.get_rect(center=self.rect.center)
                screen.blit(self.check_image, img_rect)
            else: # Fallback nếu không có ảnh
                start_pos = (self.rect.left + 4, self.rect.centery)
                mid_pos = (self.rect.centerx - 2, self.rect.bottom - 5)
                end_pos = (self.rect.right - 4, self.rect.top + 6)
                pygame.draw.lines(screen, self.checkmark_color, False, [start_pos, mid_pos, end_pos], 3)
        else:
            pygame.draw.rect(screen, self.box_color_inactive, self.rect, border_radius=3)
            pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=3)

        # Vẽ nhãn
        screen.blit(self.text_surface, self.text_rect)

    def is_checked(self):
        """
        Trả về trạng thái hiện tại của checkbox.
        :return: True nếu đã được chọn, False nếu không.
        """
        return self.checked

    def get_clickable_area(self):
        """
        Trả về hình chữ nhật bao quanh toàn bộ vùng có thể click của component.
        """
        return self.clickable_area

    def set_center_component(self, center_x, center_y):
        """
        Căn giữa toàn bộ component (hộp + chữ) vào một điểm cho trước.
        :param center_x: Tọa độ x của điểm trung tâm.
        :param center_y: Tọa độ y của điểm trung tâm.
        """
        # Tính toán tổng chiều rộng của component
        total_width = self.rect.width + self.text_spacing + self.text_rect.width
        start_x = center_x - (total_width / 2)

        # Cập nhật lại vị trí của hộp và chữ
        self.rect.x = start_x
        self.rect.centery = center_y
        self.text_rect.left = self.rect.right + self.text_spacing
        self.text_rect.centery = self.rect.centery

        # Cập nhật lại vùng có thể click sau khi di chuyển
        self.clickable_area = self.rect.union(self.text_rect)