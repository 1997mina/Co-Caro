import pygame

from handler.PieceDragHandler import PieceDragHandler
from manager.CursorManager import CursorManager
from ui.components.Button import Button
from ui.components.InputBox import InputBox
from ui.general.SettingUI import SettingUI
from utils.ResourcePath import resource_path

# Hằng số cho màu sắc và font chữ
WHITE = (255, 255, 255)
BLUE = (0, 120, 215)
BLUE_HOVER = (0, 150, 255)

TEXT_COLOR = (40, 40, 40)
MODE_BUTTON_COLOR_INACTIVE = (220, 220, 220)
MODE_BUTTON_HOVER = (180, 180, 180)

class TwoPlayerSetting(SettingUI):
    """
    Hiển thị màn hình cài đặt cho chế độ 2 người chơi.
    """
    def __init__(self, screen):
        super().__init__(screen)

        # Tải và thay đổi kích thước hình ảnh X và O
        self.img_size = 50 
        x_img_raw = pygame.image.load(resource_path('img/general/X.png')).convert_alpha()
        o_img_raw = pygame.image.load(resource_path('img/general/O.png')).convert_alpha()
        self.x_img = pygame.transform.scale(x_img_raw, (self.img_size, self.img_size))
        self.o_img = pygame.transform.scale(o_img_raw, (self.img_size, self.img_size))

        # Tải icon hoán đổi
        swap_icon_size = 40
        swap_icon_raw = pygame.image.load(resource_path('img/general/Swap.png')).convert_alpha()
        self.swap_icon_img = pygame.transform.scale(swap_icon_raw, (swap_icon_size, swap_icon_size))

        # Các ô nhập liệu và nhãn
        input_box_width = 500
        self.input_box1 = pygame.Rect((self.screen_width - input_box_width) / 2, 80, input_box_width, 50)
        self.input_box2 = pygame.Rect((self.screen_width - input_box_width) / 2, 150, input_box_width, 50)

        self.input_box1_ui = InputBox(self.input_box1.x, self.input_box1.y
                                      , self.input_box1.width, self.input_box1.height, 
                                      self.font_label, TEXT_COLOR, (100, 100, 100), (200, 200, 200))
        self.input_box1_ui._create_paste_button(self.sound_manager)
        self.input_box2_ui = InputBox(self.input_box2.x, self.input_box2.y, 
                                      self.input_box2.width, self.input_box2.height, 
                                      self.font_label, TEXT_COLOR, (100, 100, 100), (200, 200, 200))
        self.input_box2_ui._create_paste_button(self.sound_manager)
        
        # Vị trí ban đầu của X và O để kéo (đã điều chỉnh để có chỗ cho nút Dán)
        x_drag_rect_initial_center = (self.screen_width / 2 - 100, 400)
        o_drag_rect_initial_center = (self.screen_width / 2 + 100, 400)
        
        # Vị trí thả cho người chơi 1 và 2
        self.drop_target1 = pygame.Rect(self.input_box1_ui.paste_button.rect.right + 15, self.input_box1.y, self.img_size, self.img_size)
        self.drop_target2 = pygame.Rect(self.input_box2_ui.paste_button.rect.right + 15, self.input_box2.y, self.img_size, self.img_size)

        # Khởi tạo trình xử lý kéo thả quân cờ
        self.drag_handler = PieceDragHandler(self.x_img, self.o_img, x_drag_rect_initial_center, o_drag_rect_initial_center, self.drop_target1, self.drop_target2)

        # Nút hoán đổi quân cờ
        swap_button_x = self.drop_target1.right + 15
        swap_button_y = (self.drop_target1.centery + self.drop_target2.centery) / 2 - self.swap_icon_img.get_height() / 2
        self.swap_button_rect = self.swap_icon_img.get_rect(topleft=(swap_button_x, swap_button_y))

        # Các chế độ chơi
        self.modes = {
            "turn_based": {"name": "20 giây mỗi lượt", "time_limit": 20},
            "total_time": {"name": "2 phút tổng cộng", "time_limit": 120}
        }
        self.selected_mode = None # Chế độ mặc định

        # --- Các nút chọn chế độ (Radio button) ---
        self.radio_button_y_start = 550
        self.radio_button_spacing = 40
        
        mode_button_width, mode_button_height = 350, 50
        mode_button_x = self.screen_width / 2 - mode_button_width / 2

        self.turn_based_button = Button(mode_button_x, self.radio_button_y_start, mode_button_width, mode_button_height,
                                        self.font_mode.render(self.modes["turn_based"]["name"], True, TEXT_COLOR), self.sound_manager,
                                        color=MODE_BUTTON_COLOR_INACTIVE, hover_color=MODE_BUTTON_HOVER, 
                                        selected_color=BLUE_HOVER, border_radius=10)
        
        self.total_time_button = Button(mode_button_x, self.radio_button_y_start + mode_button_height + 10, mode_button_width, mode_button_height,
                                        self.font_mode.render(self.modes["total_time"]["name"], True, TEXT_COLOR), self.sound_manager,
                                        color=MODE_BUTTON_COLOR_INACTIVE, hover_color=MODE_BUTTON_HOVER, 
                                        selected_color=BLUE_HOVER, border_radius=10)
        
        # Nút Bắt đầu
        button_width = 200
        button_height = 60
        start_button_x = self.screen_width / 2 + 50
        start_button_y = 700
        
        self.start_button = Button(
            start_button_x, start_button_y, button_width, button_height,
            self.font_button.render("Bắt đầu", True, WHITE), self.sound_manager,
            color=BLUE, hover_color=BLUE_HOVER, pressed_color=BLUE_HOVER,
            disabled_color=MODE_BUTTON_HOVER, border_radius=10
        )

    def _update_selection_buttons(self, selected_button, button_group):
        """Cập nhật trạng thái is_selected cho một nhóm các nút."""
        for button in button_group:
            button.is_selected = (button == selected_button)

    def run(self):
        mouse_pos = pygame.mouse.get_pos()
        self.cursor_manager = CursorManager()
    
        self.player1_name = self.input_box1_ui.get_text()
        self.player2_name = self.input_box2_ui.get_text()

        # Điều kiện để kích hoạt nút "Bắt đầu"
        is_start_enabled = (self.player1_name.strip() and
                            self.player2_name.strip() and
                            self.drag_handler.player1_piece and
                            self.drag_handler.player2_piece and
                            self.selected_mode is not None)
        self.start_button.is_enabled = is_start_enabled

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Xử lý sự kiện cho các thành phần UI
            self.input_box1_ui.handle_event(event)
            self.input_box2_ui.handle_event(event)
            self._handle_piece_drag_and_drop(event)

            # Xử lý sự kiện cho nút hoán đổi
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Chỉ cho phép hoán đổi khi cả hai người chơi đã chọn quân cờ
                if self.drag_handler.player1_piece and self.drag_handler.player2_piece:
                    if self.swap_button_rect.collidepoint(event.pos):
                        self.drag_handler.player1_piece, self.drag_handler.player2_piece = self.drag_handler.player2_piece, self.drag_handler.player1_piece
                        self.sound_manager.play_button_click()

            if self.turn_based_button.handle_event(event):
                self.selected_mode = "turn_based"
                self._update_selection_buttons(self.turn_based_button, [self.turn_based_button, self.total_time_button])
            
            if self.total_time_button.handle_event(event):
                self.selected_mode = "total_time"
                self._update_selection_buttons(self.total_time_button, [self.turn_based_button, self.total_time_button])

            if self.start_button.handle_event(event):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                if self.drag_handler.player1_piece == 'X':
                    return self.player1_name.strip(), self.player2_name.strip(), self.selected_mode, self.modes[self.selected_mode]["time_limit"]
                elif self.drag_handler.player1_piece == 'O':
                    return self.player2_name.strip(), self.player1_name.strip(), self.selected_mode, self.modes[self.selected_mode]["time_limit"]
            
            if self.back_button.handle_event(event):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                return 'back'


        # --- Vẽ lên màn hình ---
        self.screen.fill(WHITE)
        self.screen.blit(self.background_img, (0, 0))

        # Vẽ các ô nhập tên người chơi
        super()._draw_section_title(self.screen, "Người chơi 1:", TEXT_COLOR, self.font_label, self.input_box1.y - 30, self.screen_width, align_left_of_box=self.input_box1)
        self.input_box1_ui.draw(self.screen)
        super()._draw_section_title(self.screen, "Người chơi 2:", TEXT_COLOR, self.font_label, self.input_box2.y - 30, self.screen_width, align_left_of_box=self.input_box2)
        self.input_box2_ui.draw(self.screen)

        # --- Vẽ khu vực kéo thả quân cờ đã được cải tiến ---
        # 1. Vẽ tiêu đề cho khu vực chọn
        super()._draw_section_title(self.screen, "Kéo quân cờ vào ô bên phải để chọn:", TEXT_COLOR, self.font_label, 320, self.screen_width)

        # 2. Vẽ các ô nhận quân cờ (drop zones)
        is_hovering_target1 = self.drop_target1.collidepoint(mouse_pos) and self.drag_handler.dragging
        is_hovering_target2 = self.drop_target2.collidepoint(mouse_pos) and self.drag_handler.dragging
        
        piece1_img = self.x_img if self.drag_handler.player1_piece == 'X' else (self.o_img if self.drag_handler.player1_piece == 'O' else None)
        piece2_img = self.x_img if self.drag_handler.player2_piece == 'X' else (self.o_img if self.drag_handler.player2_piece == 'O' else None)

        super().draw_drop_zone(self.screen, self.drop_target1, piece1_img, is_hovering_target1)
        super().draw_drop_zone(self.screen, self.drop_target2, piece2_img, is_hovering_target2)

        # 2.1 Vẽ nút hoán đổi nếu cả hai đã chọn quân cờ
        if self.drag_handler.player1_piece and self.drag_handler.player2_piece:
            self.screen.blit(self.swap_icon_img, self.swap_button_rect)
            # Thêm nút vào cursor manager để đổi con trỏ
            self.cursor_manager.add_clickable_area(self.swap_button_rect, True)

        # 3. Vẽ các quân cờ có thể kéo và quản lý con trỏ
        if not self.drag_handler.is_piece_dropped('X'):
            self.screen.blit(self.x_img, self.drag_handler.x_drag_rect)
            self.cursor_manager.add_clickable_area(self.drag_handler.x_drag_rect, True)
        if not self.drag_handler.is_piece_dropped('O'):
            self.screen.blit(self.o_img, self.drag_handler.o_drag_rect)
            self.cursor_manager.add_clickable_area(self.drag_handler.o_drag_rect, True)

        # Vẽ lựa chọn chế độ chơi
        super()._draw_section_title(self.screen, "Chọn chế độ thời gian:", TEXT_COLOR, self.font_label, 500, self.screen_width)
        self.turn_based_button.draw(self.screen)
        self.total_time_button.draw(self.screen)

        self.start_button.draw(self.screen)
        self.back_button.draw(self.screen)

         # Cập nhật con trỏ chuột
        self.cursor_manager.add_clickable_area(self.start_button.rect, self.start_button.is_enabled)
        self.cursor_manager.add_clickable_area(self.back_button.rect, self.back_button.is_enabled)
        self.cursor_manager.add_clickable_area(self.turn_based_button.rect, True)
        self.cursor_manager.add_clickable_area(self.total_time_button.rect, True)
        self.cursor_manager.add_clickable_area(self.input_box1_ui.paste_button.rect, self.input_box1_ui.paste_button.is_enabled)
        self.cursor_manager.add_clickable_area(self.input_box2_ui.paste_button.rect, self.input_box2_ui.paste_button.is_enabled)
        self.cursor_manager.update(mouse_pos)

        pygame.display.flip()

def get_two_player_setting(screen):
    """
    Hàm tiện ích để khởi tạo và gọi màn hình cài đặt 2 người chơi.
    """
    settings_ui = TwoPlayerSetting(screen)
    running = True

    while running:
        result = settings_ui.run() # run() trả về tuple, 'back', hoặc None
        if result == 'back':
            return None # Quay lại menu chính
        elif result is not None:
            return result # Trả về cài đặt

        pygame.time.wait(10) # Đợi một chút để tránh ngốn CPU