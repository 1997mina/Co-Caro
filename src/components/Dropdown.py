import pygame

# Hằng số màu sắc và kiểu dáng
BORDER_COLOR = (150, 150, 150)
MAIN_BOX_COLOR = (245, 245, 245)
ARROW_COLOR = (60, 60, 60)
TEXT_COLOR = (30, 30, 30)
SCROLLBAR_COLOR = (220, 220, 220)
SCROLLBAR_THUMB_COLOR = (160, 160, 160)

class Dropdown:
    """
    Một thành phần UI menu thả xuống (Dropdown/ComboBox) có khả năng cuộn.
    """
    def __init__(self, x, y, width, height, options, initial_option, 
                 sound_manager, label_text="", 
                 option_hover_color=(200, 220, 255),
                 max_visible_options=7):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected_option = initial_option
        self.sound_manager = sound_manager
        self.option_hover_color = option_hover_color
        self.is_open = False
        self.max_visible_options = max_visible_options
        self.scroll_offset = 0

        # Thuộc tính cho việc kéo thanh cuộn bằng chuột
        self.is_dragging_scrollbar = False
        self.drag_start_y = 0
        self.drag_start_offset = 0

        # Fonts
        self.font_option = pygame.font.SysFont("Times New Roman", 30)
        self.font_label = pygame.font.SysFont("Times New Roman", 35)

        # Nhãn
        self.label_text = label_text
        self.label_surf = self.font_label.render(self.label_text, True, TEXT_COLOR)

        # --- Cấu hình cho việc cuộn ---
        self.show_scrollbar = len(self.options) > self.max_visible_options
        self.scrollbar_width = 20
        # Vùng chứa các tùy chọn và thanh cuộn
        self.dropdown_panel_height = self.rect.height * min(len(self.options), self.max_visible_options)
        self.dropdown_panel_rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.width, self.dropdown_panel_height)
        
        # Thanh cuộn
        if self.show_scrollbar:
            self.scrollbar_track_rect = pygame.Rect(
                self.dropdown_panel_rect.right - self.scrollbar_width,
                self.dropdown_panel_rect.top,
                self.scrollbar_width,
                self.dropdown_panel_rect.height
            )
            self.thumb_height = max(20, self.scrollbar_track_rect.height * (self.max_visible_options / len(self.options)))
            self.scrollbar_thumb_rect = pygame.Rect(
                self.scrollbar_track_rect.x,
                self.scrollbar_track_rect.y,
                self.scrollbar_width,
                self.thumb_height
            )

    def get_selected_option(self):
        return self.selected_option

    def _update_scroll_thumb(self):
        """Cập nhật vị trí của thanh cuộn thumb."""
        if not self.show_scrollbar:
            return
        scrollable_range = len(self.options) - self.max_visible_options
        scroll_ratio = self.scroll_offset / scrollable_range if scrollable_range > 0 else 0
        thumb_travel_range = self.scrollbar_track_rect.height - self.thumb_height
        self.scrollbar_thumb_rect.y = self.scrollbar_track_rect.y + scroll_ratio * thumb_travel_range

    def handle_event(self, event):
        changed = False
        handled = False
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(mouse_pos):
                self.is_open = not self.is_open
                self.sound_manager.play_sfx('button_click')
                handled = True
            elif self.is_open:
                # Nếu dropdown đang mở, kiểm tra xem click có nằm trong panel không
                if self.dropdown_panel_rect.collidepoint(mouse_pos):
                    handled = True # Sự kiện được xử lý bởi dropdown

                    # 1. Kiểm tra kéo thanh cuộn
                    if self.show_scrollbar and self.scrollbar_thumb_rect.collidepoint(mouse_pos):
                        self.is_dragging_scrollbar = True
                        self.drag_start_y = mouse_pos[1]
                        self.drag_start_offset = self.scroll_offset
                    else:
                        # 2. Kiểm tra click trên các tùy chọn
                        option_clicked = False
                        visible_options = self.options[self.scroll_offset : self.scroll_offset + self.max_visible_options]
                        for i, option in enumerate(visible_options):
                            option_rect = pygame.Rect(self.rect.x, self.rect.bottom + i * self.rect.height, self.rect.width, self.rect.height)
                            if option_rect.collidepoint(mouse_pos):
                                if self.selected_option != option:
                                    self.selected_option = option
                                    changed = True
                                self.is_open = False
                                self.sound_manager.play_sfx('dropdown_click')
                                option_clicked = True
                                break
                        
                        # 3. Nếu không click vào tùy chọn, kiểm tra click vào rãnh cuộn (để cuộn trang)
                        if not option_clicked and self.show_scrollbar and self.scrollbar_track_rect.collidepoint(mouse_pos):
                            if mouse_pos[1] < self.scrollbar_thumb_rect.y: # Click phía trên
                                self.scroll_offset -= self.max_visible_options
                            else: # Click phía dưới
                                self.scroll_offset += self.max_visible_options
                            self.scroll_offset = max(0, min(self.scroll_offset, len(self.options) - self.max_visible_options))
                            self._update_scroll_thumb()
                else:
                    # Click ra ngoài panel, đóng nó lại
                    self.is_open = False
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging_scrollbar = False
        
        elif event.type == pygame.MOUSEMOTION and self.is_dragging_scrollbar:
            mouse_dy = mouse_pos[1] - self.drag_start_y
            scrollable_range_pixels = self.scrollbar_track_rect.height - self.thumb_height
            scrollable_range_options = len(self.options) - self.max_visible_options
            if scrollable_range_pixels > 0:
                options_per_pixel = scrollable_range_options / scrollable_range_pixels
                new_offset = self.drag_start_offset + (mouse_dy * options_per_pixel)
                self.scroll_offset = max(0, min(round(new_offset), scrollable_range_options))
                self._update_scroll_thumb()
        
        # Xử lý cuộn chuột
        if event.type == pygame.MOUSEWHEEL and self.is_open and self.show_scrollbar:
            # event.y = 1 (cuộn lên), -1 (cuộn xuống)
            self.scroll_offset -= event.y
            # Giới hạn giá trị của scroll_offset
            self.scroll_offset = max(0, min(self.scroll_offset, len(self.options) - self.max_visible_options))
            self._update_scroll_thumb()
            handled = True
        return changed, handled

    def draw(self, screen):
        # Vẽ nhãn
        label_rect = self.label_surf.get_rect(midright=(self.rect.left - 20, self.rect.centery))
        screen.blit(self.label_surf, label_rect)

        # Vẽ hộp chính
        pygame.draw.rect(screen, MAIN_BOX_COLOR, self.rect, border_radius=8)
        pygame.draw.rect(screen, BORDER_COLOR, self.rect, 2, border_radius=8)

        # Vẽ văn bản đã chọn
        selected_surf = self.font_option.render(self.selected_option, True, TEXT_COLOR)
        selected_rect = selected_surf.get_rect(center=(self.rect.centerx - 10, self.rect.centery))
        screen.blit(selected_surf, selected_rect)

        # Vẽ mũi tên
        arrow_points = []
        if self.is_open: # Mũi tên hướng lên
            arrow_points = [(self.rect.right - 25, self.rect.centery + 5),
                            (self.rect.right - 15, self.rect.centery + 5),
                            (self.rect.right - 20, self.rect.centery - 5)]
        else: # Mũi tên hướng xuống
            arrow_points = [(self.rect.right - 25, self.rect.centery - 5),
                            (self.rect.right - 15, self.rect.centery - 5),
                            (self.rect.right - 20, self.rect.centery + 5)]
        pygame.draw.polygon(screen, ARROW_COLOR, arrow_points)

        # Vẽ danh sách thả xuống nếu đang mở
        if self.is_open:
            mouse_pos = pygame.mouse.get_pos()
            # Vẽ nền cho toàn bộ danh sách
            pygame.draw.rect(screen, MAIN_BOX_COLOR, self.dropdown_panel_rect, border_bottom_left_radius=8, border_bottom_right_radius=8)
            pygame.draw.rect(screen, BORDER_COLOR, self.dropdown_panel_rect, 2, border_bottom_left_radius=8, border_bottom_right_radius=8)

            # Lấy các tùy chọn sẽ được hiển thị
            visible_options = self.options[self.scroll_offset : self.scroll_offset + self.max_visible_options]
            
            # Vẽ các tùy chọn
            options_area_width = self.rect.width - (self.scrollbar_width if self.show_scrollbar else 0)
            for i, option in enumerate(visible_options):
                option_rect = pygame.Rect(self.rect.x, self.rect.bottom + i * self.rect.height, options_area_width, self.rect.height)
                
                # Highlight tùy chọn đang được hover
                if option_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, self.option_hover_color, option_rect)

                option_surf = self.font_option.render(option, True, TEXT_COLOR)
                option_text_rect = option_surf.get_rect(center=option_rect.center)
                screen.blit(option_surf, option_text_rect)
            
            # Vẽ thanh cuộn nếu cần
            if self.show_scrollbar:
                # Vẽ rãnh cuộn
                pygame.draw.rect(screen, SCROLLBAR_COLOR, self.scrollbar_track_rect, border_top_right_radius=8, border_bottom_right_radius=8)
                # Vẽ thumb
                pygame.draw.rect(screen, SCROLLBAR_THUMB_COLOR, self.scrollbar_thumb_rect, border_radius=5)

    def add_to_cursor_manager(self, cursor_manager):
        cursor_manager.add_clickable_area(self.rect)
        if self.is_open:
            # Chỉ thêm các vùng có thể click của các tùy chọn đang hiển thị
            visible_options_count = min(len(self.options) - self.scroll_offset, self.max_visible_options)
            for i in range(visible_options_count):
                option_rect = pygame.Rect(self.rect.x, self.rect.bottom + i * self.rect.height, self.rect.width, self.rect.height)
                cursor_manager.add_clickable_area(option_rect)

    def set_center_component(self, center_x, center_y):
        # Căn giữa toàn bộ component (nhãn + hộp dropdown)
        total_width = self.label_surf.get_width() + 20 + self.rect.width
        start_x = center_x - total_width / 2
        
        dropdown_box_x = start_x + self.label_surf.get_width() + 20
        dropdown_box_y = center_y - self.rect.height / 2
        
        # Cập nhật lại tất cả các rect
        original_dx = dropdown_box_x - self.rect.x
        original_dy = dropdown_box_y - self.rect.y

        self.rect.move_ip(original_dx, original_dy)
        
        # Cập nhật panel và thanh cuộn
        self.dropdown_panel_rect.move_ip(original_dx, original_dy)
        if self.show_scrollbar:
            self.scrollbar_track_rect.move_ip(original_dx, original_dy)
            self.scrollbar_thumb_rect.move_ip(original_dx, original_dy)