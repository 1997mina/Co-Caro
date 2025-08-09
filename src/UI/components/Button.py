import pygame
from manager.CursorManager import CursorManager

class Button:
    """
    Một lớp Button có thể tái sử dụng với các hiệu ứng hover, click và bóng đổ.
    """
    def __init__(self, x, y, width, height, icon_img, sound_manager,
                 color=(100, 200, 255),
                 hover_color=(130, 220, 255),
                 pressed_color=(130, 220, 255),
                 selected_color=(130, 220, 255),
                 disabled_color=(180, 180, 180), # Màu khi nút bị vô hiệu hóa
                 border_radius=-1, # Bán kính bo góc, -1 là hình elip (mặc định)
                 shadow_color=(0, 0, 0, 50),
                 shadow_offset=(3, 3)):

        self.rect = pygame.Rect(x, y, width, height)
        self.icon_img = icon_img
        self.sound_manager = sound_manager

        # Colors
        self.colors = {
            'normal': color,
            'hover': hover_color,
            'pressed': pressed_color,
            'disabled': disabled_color,
            'selected': selected_color
        }
        self.border_radius = border_radius
        self.shadow_color = shadow_color
        self.shadow_offset = shadow_offset
        self.shadow_rect = self.rect.copy().move(shadow_offset)

        # State
        self.is_hovered = False
        self.is_pressed = False
        self.is_selected = False
        self.is_enabled = True

        # Cursor
        self.cursor_manager = CursorManager()

    def handle_event(self, event):
        """
        Xử lý các sự kiện chuột cho nút.
        Trả về True nếu nút được nhấn và thả ra (click).
        """
        if not self.is_enabled:
            self.is_pressed = False
            return False

        clicked = False
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            self.is_pressed = True
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.is_hovered:
                self.sound_manager.play_button_click()
                clicked = True
            self.is_pressed = False
        
        return clicked

    def draw(self, screen, border_width=2):
        """
        Vẽ nút lên màn hình, bao gồm bóng đổ và các trạng thái khác nhau.
        """
        # Cập nhật con trỏ
        self.cursor_manager.reset()
        self.cursor_manager.add_clickable_area(self.rect, self.is_enabled)
        self.cursor_manager.update(pygame.mouse.get_pos())

        # Xác định màu sắc dựa trên trạng thái
        if not self.is_enabled:
            current_color = self.colors['disabled']
        elif self.is_pressed:
            current_color = self.colors['pressed']
        elif self.is_selected: # Nếu nút đã được chọn, giữ màu selected bất kể hover
            current_color = self.colors['selected']
        elif self.is_hovered:
            current_color = self.colors['hover']
        else:
            current_color = self.colors['normal']

        # Hiệu ứng "nhấn xuống"
        draw_rect = self.rect
        icon_rect = self.icon_img.get_rect(center=self.rect.center)
        if (self.is_pressed or self.is_selected) and self.is_enabled:
            draw_rect = self.rect.move(self.shadow_offset)
            icon_rect = self.icon_img.get_rect(center=draw_rect.center)
        else:
            # Vẽ bóng đổ chỉ khi không bị nhấn và không phải hình chữ nhật bo góc
            if self.border_radius == -1: # Chỉ vẽ elip cho bóng đổ nếu nút là hình elip
                pygame.draw.ellipse(screen, self.shadow_color, self.shadow_rect)
            else: # Nếu là hình chữ nhật bo góc, vẽ bóng đổ hình chữ nhật bo góc
                pygame.draw.rect(screen, self.shadow_color, self.shadow_rect, border_radius=self.border_radius)

        # Vẽ thân nút
        if self.border_radius == -1: # Hình elip
            pygame.draw.ellipse(screen, current_color, draw_rect)
            pygame.draw.ellipse(screen, (128, 128, 128), draw_rect, border_width) # Viền
        else: # Hình chữ nhật bo góc
            pygame.draw.rect(screen, current_color, draw_rect, border_radius=self.border_radius)
            pygame.draw.rect(screen, (128, 128, 128), draw_rect, border_width, border_radius=self.border_radius) # Viền

        # Vẽ icon
        screen.blit(self.icon_img, icon_rect)