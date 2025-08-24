import pygame

from components.Button import Button

class InputBox:
    """
    Một lớp đóng gói toàn bộ logic cho một ô nhập liệu văn bản.
    Bao gồm xử lý sự kiện, vẽ, và hiệu ứng con trỏ nhấp nháy.
    """
    def __init__(self, x, y, w, h, font, text_color, active_color, inactive_color, initial_text='', max_chars=None):
        """
        Khởi tạo một ô nhập liệu.
        :param x, y, w, h: Vị trí và kích thước của ô.
        :param font: Font chữ để hiển thị văn bản.
        :param text_color: Màu của văn bản và con trỏ.
        :param active_color: Màu viền khi ô được chọn.
        :param inactive_color: Màu viền khi ô không được chọn.
        :param initial_text: Văn bản ban đầu.
        :param max_chars: Số lượng ký tự tối đa. None có nghĩa là không giới hạn.
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.text_color = text_color
        self.active_color = active_color
        self.inactive_color = inactive_color
        
        self.text = initial_text
        self.active = False
        self.max_chars = max_chars

        self.cursor_visible = True # Khởi tạo thuộc tính cursor_visible
        # Thuộc tính cho con trỏ nhấp nháy
        self.last_cursor_toggle = pygame.time.get_ticks()
        self.cursor_blink_interval = 500  # milliseconds

        if not pygame.scrap.get_init():
            pygame.scrap.init()

    def handle_event(self, event):
        """
        Xử lý các sự kiện đầu vào (chuột và bàn phím) cho ô nhập liệu.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Nếu người dùng click vào ô
            if self.rect.collidepoint(event.pos):
                if not self.active:
                    self.last_cursor_toggle = pygame.time.get_ticks()
                self.update() # Cập nhật ngay lập tức để con trỏ hiển thị
                self.active = True # Kích hoạt ô nhập liệu
                # Tùy chọn: Kích hoạt nút Dán khi ô được kích hoạt
                self.cursor_visible = True
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                # Reset con trỏ khi gõ phím để nó hiện lên ngay lập tức
                self.last_cursor_toggle = pygame.time.get_ticks()

                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                # Xử lý dán (Ctrl+V hoặc Cmd+V)
                elif event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL or event.mod & pygame.KMOD_GUI):
                    self._paste_from_clipboard()
                else:
                    # Chỉ thêm ký tự nếu chưa đạt giới hạn
                    if self.max_chars is None or len(self.text) < self.max_chars:
                        self.text += event.unicode

    def _paste_from_clipboard(self):
        try:
            clipboard_content = pygame.scrap.get(pygame.SCRAP_TEXT)
            if clipboard_content:
                pasted_text = clipboard_content.decode('utf-8').strip('\x00') # Loại bỏ ký tự null
                if self.max_chars is not None:
                    # Tính toán không gian còn lại và cắt bớt văn bản dán nếu cần
                    remaining_space = self.max_chars - len(self.text)
                    if remaining_space > 0:
                        self.text += pasted_text[:remaining_space]
                else:
                    self.text += pasted_text
        except (pygame.error, UnicodeDecodeError) as e:
            print(f"Không thể dán văn bản từ clipboard: {e}")
            
    def update(self):
        """
        Cập nhật trạng thái của ô, ví dụ như con trỏ nhấp nháy.
        Hàm này nên được gọi mỗi frame trong vòng lặp game.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_cursor_toggle > self.cursor_blink_interval:
            self.cursor_visible = not self.cursor_visible
            self.last_cursor_toggle = current_time

    def handle_mouse_cursor(self, mouse_pos):
        """
        Đặt con trỏ chuột thành IBEAM khi di chuột qua ô nhập liệu.
        Trả về True nếu con trỏ được đặt, False nếu không.
        """
        if self.rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            return True
        return False

    def draw(self, screen):
        """
        Vẽ ô nhập liệu lên màn hình.
        """
        # Vẽ viền
        border_color = self.active_color if self.active else self.inactive_color
        pygame.draw.rect(screen, border_color, self.rect, 2)

        # Vẽ văn bản
        text_surface = self.font.render(self.text, True, self.text_color)
        # Đảm bảo văn bản không tràn ra ngoài (tùy chọn, có thể thêm sau)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

        # Vẽ con trỏ nhấp nháy nếu ô đang được chọn
        if self.active and self.cursor_visible:
            text_width = text_surface.get_width()
            cursor_x = self.rect.x + 10 + text_width
            cursor_y_start = self.rect.y + 8
            cursor_y_end = self.rect.y + self.rect.height - 8
            pygame.draw.line(screen, self.text_color, (cursor_x, cursor_y_start), (cursor_x, cursor_y_end), 2)

    def get_text(self):
        """Trả về văn bản hiện tại trong ô."""
        return self.text.strip()

    def is_active(self):
        """Kiểm tra xem ô có đang được chọn không."""
        return self.active