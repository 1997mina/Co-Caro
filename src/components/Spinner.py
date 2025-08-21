import pygame

# Hằng số màu sắc và kiểu dáng
BORDER_COLOR = (150, 150, 150)
BG_COLOR = (245, 245, 245)
ARROW_COLOR = (60, 60, 60)
TEXT_COLOR = (30, 30, 30)

class Spinner:
    """
    Một thành phần UI cho phép người dùng chọn một số bằng cách nhấp vào mũi tên lên/xuống.
    Bao gồm một nhãn, một hộp hiển thị giá trị và các nút lên/xuống.
    """
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, sound_manager, label_text=""):
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.sound_manager = sound_manager
        
        # Fonts
        self.font_value = pygame.font.SysFont("Times New Roman", 30)
        self.font_label = pygame.font.SysFont("Times New Roman", 35)

        # Nhãn
        self.label_text = label_text
        self.label_surf = self.font_label.render(self.label_text, True, TEXT_COLOR)
        
        # Các hình chữ nhật chính của component
        self.spinner_box_rect = pygame.Rect(x, y, width, height)
        button_width = height # Làm cho các nút mũi tên thành hình vuông
        self.value_display_rect = pygame.Rect(x, y, width - button_width, height)
        self.up_button_rect = pygame.Rect(x + width - button_width, y, button_width, height // 2)
        self.down_button_rect = pygame.Rect(x + width - button_width, y + height // 2, button_width, height // 2)

        # Trạng thái hover để phản hồi trực quan
        self.hover_up = False
        self.hover_down = False

    def get_value(self):
        return self.value

    def handle_event(self, event):
        changed = False
        mouse_pos = pygame.mouse.get_pos()
        
        self.hover_up = self.up_button_rect.collidepoint(mouse_pos)
        self.hover_down = self.down_button_rect.collidepoint(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hover_up:
                if self.value < self.max_val:
                    self.value += 1
                    self.sound_manager.play_sfx('button_click')
                    changed = True
            elif self.hover_down:
                if self.value > self.min_val:
                    self.value -= 1
                    self.sound_manager.play_sfx('button_click')
                    changed = True
        return changed

    def draw(self, screen):
        # Vẽ nhãn ở bên trái hộp spinner
        label_rect = self.label_surf.get_rect(midright=(self.spinner_box_rect.left - 20, self.spinner_box_rect.centery))
        screen.blit(self.label_surf, label_rect)

        # Vẽ nền hộp giá trị
        pygame.draw.rect(screen, BG_COLOR, self.value_display_rect, border_top_left_radius=8, border_bottom_left_radius=8)
        
        # Vẽ văn bản giá trị
        value_surf = self.font_value.render(str(self.value), True, TEXT_COLOR)
        value_text_rect = value_surf.get_rect(center=self.value_display_rect.center)
        screen.blit(value_surf, value_text_rect)

        # Vẽ nền và mũi tên cho nút lên
        up_bg_color = (220, 220, 220) if self.hover_up else BG_COLOR
        pygame.draw.rect(screen, up_bg_color, self.up_button_rect, border_top_right_radius=8)
        pygame.draw.polygon(screen, ARROW_COLOR, [(self.up_button_rect.centerx, self.up_button_rect.top + 10), (self.up_button_rect.left + 10, self.up_button_rect.bottom - 10), (self.up_button_rect.right - 10, self.up_button_rect.bottom - 10)])

        # Vẽ nền và mũi tên cho nút xuống
        down_bg_color = (220, 220, 220) if self.hover_down else BG_COLOR
        pygame.draw.rect(screen, down_bg_color, self.down_button_rect, border_bottom_right_radius=8)
        pygame.draw.polygon(screen, ARROW_COLOR, [(self.down_button_rect.centerx, self.down_button_rect.bottom - 10), (self.down_button_rect.left + 10, self.down_button_rect.top + 10), (self.down_button_rect.right - 10, self.down_button_rect.top + 10)])
        
        # Vẽ đường viền xung quanh toàn bộ hộp spinner
        pygame.draw.rect(screen, BORDER_COLOR, self.spinner_box_rect, 2, border_radius=8)
        # Vẽ đường phân cách
        pygame.draw.line(screen, BORDER_COLOR, self.up_button_rect.topleft, self.down_button_rect.bottomleft, 2)

    def add_to_cursor_manager(self, cursor_manager):
        cursor_manager.add_clickable_area(self.up_button_rect)
        cursor_manager.add_clickable_area(self.down_button_rect)

    def set_center_component(self, center_x, center_y):
        # Phương thức này căn giữa toàn bộ component (nhãn + hộp spinner)
        total_width = self.label_surf.get_width() + 20 + self.spinner_box_rect.width
        start_x = center_x - total_width / 2
        
        spinner_box_x = start_x + self.label_surf.get_width() + 20
        spinner_box_y = center_y - self.spinner_box_rect.height / 2
        
        # Cập nhật lại tất cả các rect dựa trên vị trí top-left mới của hộp spinner
        self.spinner_box_rect.topleft = (spinner_box_x, spinner_box_y)
        button_width = self.spinner_box_rect.height
        self.value_display_rect.topleft = self.spinner_box_rect.topleft
        self.up_button_rect.topleft = (self.spinner_box_rect.left + self.spinner_box_rect.width - button_width, self.spinner_box_rect.top)
        self.down_button_rect.topleft = (self.spinner_box_rect.left + self.spinner_box_rect.width - button_width, self.spinner_box_rect.top + self.spinner_box_rect.height // 2)