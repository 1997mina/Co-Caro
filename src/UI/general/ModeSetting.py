import pygame

from manager.SoundManager import SoundManager
from components.Button import Button
from utils.ResourcePath import resource_path

# Hằng số màu sắc cho các nút trong màn hình cài đặt
WHITE = (255, 255, 255)
# Màu nút Bắt đầu
START_COLOR = (0, 120, 215) # Xanh dương
START_HOVER_COLOR = (0, 150, 255)
START_PRESSED_COLOR = (0, 100, 195)
# Màu nút Quay lại
BACK_COLOR = (100, 100, 100) # Xám đậm
BACK_HOVER_COLOR = (130, 130, 130)
BACK_PRESSED_COLOR = (80, 80, 80)
# Màu nút bị vô hiệu hóa
DISABLED_COLOR = (180, 180, 180)

class SettingUI:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        # Sử dụng font hệ thống Times New Roman cho các thành phần giao diện chung
        self.font_label = pygame.font.SysFont("Times New Roman", 36)
        self.font_button = pygame.font.SysFont("Times New Roman", 40, bold=True)
        self.font_placeholder = pygame.font.SysFont("Times New Roman", 24, italic=True)
        self.font_mode = pygame.font.SysFont("Times New Roman", 28) # Font for radio buttons

        # Tải hình nền
        self.background_img = pygame.image.load(resource_path('img/general/Background.jpg')).convert()
        self.background_img = pygame.transform.scale(self.background_img, (self.screen_width, self.screen_height))
        self.background_img.set_alpha(50)

        # Nút Quay lại
        button_width = 200
        button_height = 60
        back_button_x = self.screen_width / 2 - 50 - button_width
        back_button_y = 700

        self.sound_manager = SoundManager()

        self.back_button = Button(
            back_button_x, back_button_y, button_width, button_height,
            self.font_button.render("Quay lại", True, WHITE), self.sound_manager,
            color=BACK_COLOR, hover_color=BACK_HOVER_COLOR, pressed_color=BACK_PRESSED_COLOR,
            border_radius=10
        )

        # Thuộc tính cho con trỏ nhấp nháy
        self.cursor_visible = True
        self.last_cursor_toggle = pygame.time.get_ticks()
        self.cursor_blink_interval = 500 # milliseconds


    def draw_piece_button(self, screen, rect, piece_img, player_piece, current_piece, mouse_pos, 
                          enabled_color, disabled_color, disabled_hover_color):
        """
        Vẽ nút chọn quân cờ (X hoặc O).
        """
        color = enabled_color if player_piece == current_piece else \
            (disabled_hover_color if rect.collidepoint(mouse_pos) else disabled_color)
    
        pygame.draw.rect(screen, color, rect, border_radius=15)
        screen.blit(piece_img, piece_img.get_rect(center=rect.center))

    def draw_button(self, screen, rect, color, text, font, text_color, border_radius=0):
        """
        Vẽ một nút trên màn hình.
        """
        pygame.draw.rect(screen, color, rect, border_radius=border_radius)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    def draw_radio_button(self, screen, center_x, center_y, radius, is_selected, text, font, text_color, selected_color):
        """
        Vẽ một nút radio.
        """
        # Vẽ vòng tròn ngoài
        pygame.draw.circle(screen, text_color, (center_x, center_y), radius, 2)
    
        # Nếu được chọn, vẽ vòng tròn bên trong
        if is_selected:
            pygame.draw.circle(screen, selected_color, (center_x, center_y), radius - 4)
    
        # Vẽ văn bản
        text_x_offset = radius + 10
        text_surface = font.render(text, True, text_color)
        screen.blit(text_surface, (center_x + text_x_offset, center_y - text_surface.get_height() / 2))

    def _draw_dashed_rect(self, surface, color, rect, dash_length=5, gap_length=5):
        """Vẽ một hình chữ nhật với đường viền đứt nét."""
        x, y, w, h = rect
        # Trên và dưới
        for i in range(x, x + w, dash_length + gap_length):
            pygame.draw.line(surface, color, (i, y), (min(i + dash_length, x + w), y), 2)
            pygame.draw.line(surface, color, (i, y + h), (min(i + dash_length, x + w), y + h), 2)
        # Trái và phải
        for i in range(y, y + h, dash_length + gap_length):
            pygame.draw.line(surface, color, (x, i), (x, min(i + dash_length, y + h)), 2)
            pygame.draw.line(surface, color, (x + w, i), (x + w, min(i + dash_length, y + h)), 2)

    def _draw_section_title(self, screen, text, text_color, font, y_position, screen_width, align_left_of_box=None, align_right_of_box=None, align_right_offset=15, y_override=None):
        """
        Vẽ tiêu đề cho một phần cài đặt.
        Nếu align_left_of_box được cung cấp, tiêu đề sẽ được căn lề so với hộp đó.
        Nếu không, nó sẽ được căn giữa màn hình.
        """
        title_surface = font.render(text, True, text_color)
        y_pos = y_override if y_override is not None else align_left_of_box.centery if align_left_of_box else (align_right_of_box.centery if align_right_of_box else y_position)

        if align_left_of_box: # Align title to the left of a given box
            title_rect = title_surface.get_rect(midright=(align_left_of_box.left - 15, y_pos))
        elif align_right_of_box: # Align title to the right of a given box
            title_rect = title_surface.get_rect(midleft=(align_right_of_box.right + align_right_offset, y_pos))
        else:
            title_rect = title_surface.get_rect(center=(screen_width / 2, y_position))
        screen.blit(title_surface, title_rect)