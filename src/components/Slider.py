import pygame

class Slider:
    """
    Lớp tạo ra một thanh trượt (slider) có thể tương tác trong Pygame.
    """
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, sound_manager, label_text="", value_suffix=""):
        """
        Khởi tạo Slider.
        :param x, y, w, h: Vị trí và kích thước của thanh trượt (track).
        :param min_val, max_val: Giá trị nhỏ nhất và lớn nhất của slider.
        :param initial_val: Giá trị khởi tạo.
        :param sound_manager: Thể hiện của SoundManager để phát âm thanh.
        :param label_text: Nhãn hiển thị bên cạnh giá trị.
        :param value_suffix: Hậu tố hiển thị sau giá trị (ví dụ: "%").
        """
        self.track_rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.sound_manager = sound_manager
        self.label_text = label_text
        self.value_suffix = value_suffix
        self.text_padding = 35 # Khoảng cách từ lề slider đến text min/max

        # Thuộc tính của núm trượt (knob)
        self.knob_radius = h + 4 # Bán kính của núm trượt
        self.knob_pos_x = self._calculate_knob_pos_from_value()
        self.knob_rect = pygame.Rect(0, 0, self.knob_radius * 2, self.knob_radius * 2)
        self.knob_rect.center = (self.knob_pos_x, self.track_rect.centery)

        # Trạng thái
        self.dragging = False

        # Màu sắc
        self.track_color = (150, 150, 150)
        self.knob_color = (255, 0, 0)
        self.knob_hover_color = (255, 50, 50)
        self.text_color = (30, 30, 30)

        # Font chữ
        self.font = pygame.font.SysFont("Times New Roman", 30)
        self.min_max_font = pygame.font.SysFont("Times New Roman", 25) # Font nhỏ hơn cho min/max

        # Tạo surface cho văn bản min/max để tối ưu hóa
        self.min_text_surf = self.min_max_font.render(str(self.min_val), True, self.text_color) # Render min text
        self.max_text_surf = self.min_max_font.render(str(self.max_val), True, self.text_color) # Render max text

        # Tính toán vị trí cho văn bản min/max
        self.min_text_rect = self.min_text_surf.get_rect(midright=(self.track_rect.left - self.text_padding, self.track_rect.centery))
        self.max_text_rect = self.max_text_surf.get_rect(midleft=(self.track_rect.right + self.text_padding, self.track_rect.centery))

    def _calculate_knob_pos_from_value(self):
        """Tính toán vị trí x của núm trượt dựa trên giá trị hiện tại."""
        # Tỷ lệ của giá trị hiện tại trong khoảng min-max
        value_ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        # Chuyển đổi tỷ lệ đó thành vị trí pixel trên thanh trượt
        return self.track_rect.x + value_ratio * self.track_rect.width

    def _calculate_value_from_knob_pos(self):
        """Tính toán giá trị dựa trên vị trí x của núm trượt."""
        # Tỷ lệ vị trí của núm trượt trên thanh
        pos_ratio = (self.knob_rect.centerx - self.track_rect.x) / self.track_rect.width
        # Chuyển đổi tỷ lệ đó thành giá trị, làm tròn đến số nguyên gần nhất
        value = self.min_val + pos_ratio * (self.max_val - self.min_val)
        return int(round(value))

    def handle_event(self, event):
        """Xử lý sự kiện chuột cho slider."""
        value_changed = False
        mouse_pos = pygame.mouse.get_pos()
        is_hovering_knob = self.knob_rect.collidepoint(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Cho phép click vào cả núm và thanh trượt
            if is_hovering_knob or self.track_rect.collidepoint(mouse_pos):
                self.dragging = True
                # Nếu click vào thanh trượt, di chuyển núm đến vị trí đó
                if self.track_rect.collidepoint(mouse_pos):
                    self.knob_rect.centerx = mouse_pos[0]
                    # Giới hạn vị trí núm trong phạm vi thanh trượt
                    self.knob_rect.centerx = max(self.track_rect.left, min(self.knob_rect.centerx, self.track_rect.right))
                    new_value = self._calculate_value_from_knob_pos()
                    if new_value != self.value:
                        self.value = new_value
                        self.sound_manager.play_button_click()
                        value_changed = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.knob_rect.centerx = mouse_pos[0]
                # Giới hạn vị trí núm trong phạm vi thanh trượt
                self.knob_rect.centerx = max(self.track_rect.left, min(self.knob_rect.centerx, self.track_rect.right))
                new_value = self._calculate_value_from_knob_pos()
                if new_value != self.value:
                    self.value = new_value
                    value_changed = True
                    # Có thể thêm âm thanh ở đây nếu muốn
        
        return value_changed

    def draw(self, screen):
        """Vẽ slider lên màn hình."""
        # Vẽ thanh trượt
        pygame.draw.rect(screen, self.track_color, self.track_rect, border_radius=5)

        # Vẽ núm trượt
        knob_color = self.knob_hover_color if self.knob_rect.collidepoint(pygame.mouse.get_pos()) or self.dragging else self.knob_color
        pygame.draw.circle(screen, knob_color, self.knob_rect.center, self.knob_radius)

        # Vẽ giá trị hiện tại
        value_text = f"{self.label_text}{self.value}{self.value_suffix}"
        text_surf = self.font.render(value_text, True, self.text_color)
        text_rect = text_surf.get_rect(center=(self.track_rect.centerx, self.track_rect.centery - 55))
        screen.blit(text_surf, text_rect)

        # Vẽ giá trị min và max ở hai bên
        screen.blit(self.min_text_surf, self.min_text_rect) # Draw min text
        screen.blit(self.max_text_surf, self.max_text_rect) # Draw max text


    def get_value(self):
        """Trả về giá trị hiện tại của slider."""
        return self.value

    def add_to_cursor_manager(self, cursor_manager):
        """Thêm vùng có thể click của slider vào CursorManager."""
        # Tạo một vùng chữ nhật lớn hơn một chút bao quanh cả thanh và núm
        clickable_area = self.track_rect.inflate(self.knob_radius, self.knob_radius * 2)
        cursor_manager.add_clickable_area(clickable_area, True)

    def set_center_component(self, center_x, center_y):
        """
        Căn giữa toàn bộ component (thanh trượt + nhãn) vào một điểm cho trước.
        :param center_x: Tọa độ x của điểm trung tâm.
        :param center_y: Tọa độ y của điểm trung tâm.
        """
        # Cập nhật vị trí của thanh trượt
        self.track_rect.center = (center_x, center_y)

        # Cập nhật lại vị trí của núm trượt dựa trên giá trị hiện tại
        self.knob_rect.center = (self._calculate_knob_pos_from_value(), self.track_rect.centery)

        # Cập nhật lại vị trí của nhãn min/max để chúng di chuyển cùng thanh trượt
        self.min_text_rect.midright = (self.track_rect.left - self.text_padding, self.track_rect.centery) # Update min text position
        self.max_text_rect.midleft = (self.track_rect.right + self.text_padding, self.track_rect.centery) # Update max text position