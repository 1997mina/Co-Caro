import pygame

class Slider:
    """
    Lớp tạo ra một thanh trượt (slider) có thể tương tác trong Pygame.
    """
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, sound_manager, label_text="", icon_surface=None, value_suffix="",
                 knob_color=(255, 0, 0), knob_hover_color = (255, 50, 50), track_color=(200, 200, 200), track_fill_color=(60, 180, 80)):
        """
        Khởi tạo Slider.
        :param x, y, w, h: Vị trí và kích thước của thanh trượt (track).
        :param min_val, max_val: Giá trị nhỏ nhất và lớn nhất của slider.
        :param initial_val: Giá trị khởi tạo.
        :param sound_manager: Thể hiện của SoundManager để phát âm thanh.
        :param label_text: (Tùy chọn) Nhãn hiển thị phía trên slider.
        :param icon_surface: (Tùy chọn) pygame.Surface của icon để hiển thị bên trái slider.
        :param value_suffix: (Tùy chọn) Hậu tố hiển thị sau giá trị (ví dụ: "%").
        :param knob_color: (Tùy chọn) Màu của núm trượt.
        :param track_color: (Tùy chọn) Màu của thanh trượt.
        """
        self.track_rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.sound_manager = sound_manager
        self.label_text = label_text
        self.icon_surface = icon_surface
        self.value_suffix = value_suffix
        self.component_padding = 30 # Khoảng cách giữa icon/value và slider

        # Thuộc tính của núm trượt (knob)
        self.knob_radius = h + 4 # Bán kính của núm trượt
        self.knob_pos_x = self._calculate_knob_pos_from_value()
        self.knob_rect = pygame.Rect(0, 0, self.knob_radius * 2, self.knob_radius * 2)
        self.knob_rect.center = (self.knob_pos_x, self.track_rect.centery)

        # Trạng thái
        self.dragging = False

        # Màu sắc
        self.track_color = track_color
        self.knob_color = knob_color
        self.track_fill_color = track_fill_color
        self.knob_hover_color = knob_hover_color
        self.text_color = (30, 30, 30)

        # Font chữ
        self.font = pygame.font.SysFont("Times New Roman", 35)
        self.label_font = pygame.font.SysFont("Times New Roman", 32)

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
        # 1. Vẽ nhãn ở trên (nếu có)
        if self.label_text:
            label_surf = self.label_font.render(self.label_text, True, self.text_color)
            label_rect = label_surf.get_rect(center=(self.track_rect.centerx, self.track_rect.top - 40))
            screen.blit(label_surf, label_rect)

        # 2. Vẽ icon bên trái (nếu có)
        if self.icon_surface:
            icon_rect = self.icon_surface.get_rect(midright=(self.track_rect.left - self.component_padding, self.track_rect.centery))
            screen.blit(self.icon_surface, icon_rect)

        # 3. Vẽ toàn bộ thanh trượt với màu nền (phần bên phải/chưa điền)
        pygame.draw.rect(screen, self.track_color, self.track_rect, border_radius=5)

        # 4. Vẽ phần đã điền (bên trái) đè lên trên
        fill_width = self.knob_rect.centerx - self.track_rect.left
        if fill_width > 0:
            fill_rect = pygame.Rect(self.track_rect.left, self.track_rect.top, fill_width, self.track_rect.height)
            # Xử lý bo góc để trông đẹp mắt
            # Nếu thanh trượt gần đầy, bo góc cả hai bên
            if fill_width >= self.track_rect.width - 2: # -2 để xử lý sai số làm tròn
                pygame.draw.rect(screen, self.track_fill_color, fill_rect, border_radius=5)
            else: # Nếu không, chỉ bo góc bên trái
                pygame.draw.rect(screen, self.track_fill_color, fill_rect, border_top_left_radius=5, border_bottom_left_radius=5)

        # 5. Vẽ núm trượt
        knob_color = self.knob_hover_color if self.knob_rect.collidepoint(pygame.mouse.get_pos()) or self.dragging else self.knob_color
        pygame.draw.circle(screen, knob_color, self.knob_rect.center, self.knob_radius)

        # 6. Vẽ giá trị hiện tại ở bên phải
        value_text = f"{self.value}{self.value_suffix}"
        text_surf = self.font.render(value_text, True, self.text_color)
        text_rect = text_surf.get_rect(midleft=(self.track_rect.right + self.component_padding, self.track_rect.centery))
        screen.blit(text_surf, text_rect)


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
        Căn giữa thanh trượt vào một điểm cho trước. Icon, nhãn và giá trị sẽ được định vị tương đối.
        :param center_x: Tọa độ x của điểm trung tâm.
        :param center_y: Tọa độ y của điểm trung tâm.
        """
        # Cập nhật vị trí của thanh trượt
        self.track_rect.center = (center_x, center_y)

        # Cập nhật lại vị trí của núm trượt dựa trên giá trị hiện tại
        self.knob_rect.center = (self._calculate_knob_pos_from_value(), self.track_rect.centery)