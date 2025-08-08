import pygame

from manager.CursorManager import CursorManager
from handler.PieceDragHandler import PieceDragHandler
from ui.components.InputBox import InputBox
from ui.general.SettingUI import SettingUI
from utils.ResourcePath import resource_path

# Hằng số cho màu sắc và font chữ
WHITE = (255, 255, 255)
BLUE = (0, 120, 215)
BLUE_HOVER = (0, 150, 255)
TEXT_COLOR = (40, 40, 40)
DARK_GRAY = (100, 100, 100)
GRAY_HOVER = (130, 130, 130)
INPUT_BOX_COLOR_INACTIVE = (200, 200, 200)
START_BUTTON_DISABLED_COLOR = (180, 180, 180)
DRAG_COLOR = (150, 150, 150)
MODE_BUTTON_COLOR_INACTIVE = (220, 220, 220)

class TwoPlayerSetting(SettingUI):
    """
    Hiển thị màn hình cài đặt cho chế độ 2 người chơi.
    """
    def __init__(self, screen):
        super().__init__(screen)

        # Tải và thay đổi kích thước hình ảnh X và O
        self.img_size = 50 
        x_img_raw = pygame.image.load(resource_path('img/X.png')).convert_alpha()
        o_img_raw = pygame.image.load(resource_path('img/O.png')).convert_alpha()
        self.x_img = pygame.transform.scale(x_img_raw, (self.img_size, self.img_size))
        self.o_img = pygame.transform.scale(o_img_raw, (self.img_size, self.img_size))

        # Các ô nhập liệu và nhãn
        input_box_width = 500
        self.input_box1 = pygame.Rect((self.screen_width - input_box_width) / 2, 80, input_box_width, 50)
        self.input_box2 = pygame.Rect((self.screen_width - input_box_width) / 2, 150, input_box_width, 50)
        self.player1_name = ""
        self.player2_name = ""
        self.active_box = None  # Có thể là 1 hoặc 2, hoặc None

        self.input_box1_ui = InputBox(self.input_box1.x, self.input_box1.y
                                      , self.input_box1.width, self.input_box1.height, 
                                      self.font_label, TEXT_COLOR, DARK_GRAY, INPUT_BOX_COLOR_INACTIVE)
        self.input_box2_ui = InputBox(self.input_box2.x, self.input_box2.y, 
                                      self.input_box2.width, self.input_box2.height, 
                                      self.font_label, TEXT_COLOR, DARK_GRAY, INPUT_BOX_COLOR_INACTIVE)

        # Vị trí ban đầu của X và O để kéo
        x_drag_rect_initial_center = (self.screen_width / 2 - 100, 400)
        o_drag_rect_initial_center = (self.screen_width / 2 + 100, 400)

        # Vị trí thả cho người chơi 1 và 2
        self.drop_target1 = pygame.Rect(self.input_box1.x + self.input_box1.width + 20, self.input_box1.y, self.img_size, self.img_size)
        self.drop_target2 = pygame.Rect(self.input_box2.x + self.input_box2.width + 20, self.input_box2.y, self.img_size, self.img_size)

        # Khởi tạo trình xử lý kéo thả quân cờ
        self.drag_handler = PieceDragHandler(self.x_img, self.o_img, x_drag_rect_initial_center, o_drag_rect_initial_center, self.drop_target1, self.drop_target2)

        # Các chế độ chơi
        self.modes = {
            "turn_based": {"name": "20 giây mỗi lượt", "time_limit": 20},
            "total_time": {"name": "2 phút tổng cộng", "time_limit": 120}
        }
        self.selected_mode = None # Chế độ mặc định

        # --- Các nút chọn chế độ (Radio button) ---
        self.radio_button_y_start = 550
        self.radio_button_spacing = 40
        self.radio_button_radius = 15
        # Khu vực có thể click cho radio button (bao gồm cả nút tròn và chữ)
        self.radio_turn_based_rect = pygame.Rect(self.screen_width / 2 - 150, self.radio_button_y_start - self.radio_button_radius, 300, self.radio_button_radius * 2)
        self.radio_total_time_rect = pygame.Rect(self.screen_width / 2 - 150, self.radio_button_y_start + self.radio_button_spacing - self.radio_button_radius, 300, self.radio_button_radius * 2)

        self.cursor_manager = CursorManager()

    def run(self):
        mouse_pos = pygame.mouse.get_pos()

        self.player1_name = self.input_box1_ui.get_text()
        self.player2_name = self.input_box2_ui.get_text()

        # Điều kiện để kích hoạt nút "Bắt đầu"
        is_start_enabled = (self.player1_name.strip() and
                            self.player2_name.strip() and
                            self.drag_handler.player1_piece and
                            self.drag_handler.player2_piece and
                            self.selected_mode is not None)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            self.input_box1_ui.handle_event(event)
            self.input_box2_ui.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.radio_turn_based_rect.collidepoint(event.pos):
                    if self.selected_mode != "turn_based":
                        self.sound_manager.play_button_click()
                    self.selected_mode = "turn_based"
                elif self.radio_total_time_rect.collidepoint(event.pos):
                    if self.selected_mode != "total_time":
                        self.sound_manager.play_button_click()
                    self.selected_mode = "total_time"
                elif self.start_button.collidepoint(event.pos) and is_start_enabled:
                    self.sound_manager.play_button_click()
                    pygame.time.wait(100)
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # Khôi phục con trỏ
                    # Trả về tên và thời gian giới hạn dựa trên chế độ đã chọn (player1_name là X, player2_name là O)
                    if self.drag_handler.player1_piece == 'X':
                        return self.player1_name.strip(), self.player2_name.strip(), self.selected_mode, self.modes[self.selected_mode]["time_limit"]
                    elif self.drag_handler.player1_piece == 'O':
                        return self.player2_name.strip(), self.player1_name.strip(), self.selected_mode, self.modes[self.selected_mode]["time_limit"]

                elif self.back_button.collidepoint(event.pos):
                    self.sound_manager.play_button_click()
                    pygame.time.wait(100)
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # Khôi phục con trỏ
                    return 'back' # Quay lại menu chính
                else:
                    self.active_box = None
            
            self._handle_piece_drag_and_drop(event)

            if event.type == pygame.KEYDOWN:
                if self.active_box is not None:
                    # Reset con trỏ khi gõ phím để nó hiện lên ngay lập tức
                    self.cursor_visible = True
                    self.last_cursor_toggle = pygame.time.get_ticks()

                    if event.key == pygame.K_BACKSPACE:
                        if self.active_box == 1:
                            self.player1_name = self.player1_name[:-1]
                        elif self.active_box == 2:
                            self.player2_name = self.player2_name[:-1]
                    elif event.key == pygame.K_RETURN: # Nhấn Enter cũng tắt ô nhập liệu
                        self.active_box = None
                    else: # Nhập ký tự thông thường
                        # Xử lý dán (Ctrl+V hoặc Cmd+V)
                        if event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL or pygame.key.get_mods() & pygame.KMOD_GUI):
                            if self.active_box == 1:
                                self.player1_name = self._handle_paste(event, self.player1_name)
                            elif self.active_box == 2:
                                self.player2_name = self._handle_paste(event, self.player2_name)
                        if self.active_box == 1:
                            self.player1_name += event.unicode
                        else:
                            self.player2_name += event.unicode

        # --- Vẽ lên màn hình ---
        # Lấp đầy màn hình bằng một màu nền đặc trước khi vẽ ảnh nền trong suốt
        self.screen.fill(WHITE)
        self.screen.blit(self.background_img, (0, 0))

        # Sử dụng CursorManager để xử lý con trỏ chuột
        self.cursor_manager = CursorManager() # Reset mỗi frame
        self.cursor_manager.add_text_input(self.input_box1_ui)
        self.cursor_manager.add_text_input(self.input_box2_ui)
        self.cursor_manager.add_clickable_area(self.start_button, is_start_enabled)
        self.cursor_manager.add_clickable_area(self.back_button)
        self.cursor_manager.add_clickable_area(self.drag_handler.x_drag_rect)
        self.cursor_manager.add_clickable_area(self.drag_handler.o_drag_rect)
        self.cursor_manager.add_clickable_area(self.radio_turn_based_rect)
        self.cursor_manager.add_clickable_area(self.radio_total_time_rect)
        self.cursor_manager.update(mouse_pos)
        
        # Vẽ các ô nhập tên người chơi
        super()._draw_section_title(self.screen, "Người chơi 1:", TEXT_COLOR, self.font_label, self.input_box1.y - 30, self.screen_width, align_left_of_box=self.input_box1)
        self.input_box1_ui.draw(self.screen)
        super()._draw_section_title(self.screen, "Người chơi 2:", TEXT_COLOR, self.font_label, self.input_box2.y - 30, self.screen_width, align_left_of_box=self.input_box2)
        self.input_box2_ui.draw(self.screen)

        self._draw_piece_drag_and_drop(self.screen, mouse_pos, DRAG_COLOR, DARK_GRAY)

        # Hiển thị hướng dẫn kéo thả
        super()._draw_section_title(self.screen, "Kéo X hoặc O vào ô nhỏ để chọn quân cờ:", TEXT_COLOR, self.font_label, 320, self.screen_width)

        # Vẽ lựa chọn chế độ chơi
        super()._draw_section_title(self.screen, "Chọn chế độ thời gian:", TEXT_COLOR, self.font_label, 500, self.screen_width)

        # Vẽ Radio Buttons
        # Căn chỉnh vị trí X của vòng tròn và văn bản
        radio_x = self.radio_turn_based_rect.x + self.radio_button_radius

        # Lựa chọn 1: "20 giây mỗi lượt"
        super().draw_radio_button(self.screen, radio_x, self.radio_turn_based_rect.centery, self.radio_button_radius,
                                  self.selected_mode == "turn_based", self.modes["turn_based"]["name"],
                                  self.font_mode, TEXT_COLOR, BLUE)

        # Lựa chọn 2: "2 phút tổng cộng"
        super().draw_radio_button(self.screen, radio_x, self.radio_total_time_rect.centery, self.radio_button_radius,
                                  self.selected_mode == "total_time", self.modes["total_time"]["name"],
                                  self.font_mode, TEXT_COLOR, BLUE)

        # Nút Bắt đầu
        if is_start_enabled:
            if self.start_button.collidepoint(mouse_pos):
                button_color = BLUE_HOVER
            else:
                button_color = BLUE
        else:
            button_color = START_BUTTON_DISABLED_COLOR
        super().draw_button(self.screen, self.start_button, button_color, "Bắt đầu", self.font_button, WHITE, 10)

        # Vẽ nút Quay lại
        if self.back_button.collidepoint(mouse_pos):
            back_button_color = GRAY_HOVER
        else:
            back_button_color = DARK_GRAY
        super().draw_button(self.screen, self.back_button, back_button_color, "Quay lại", self.font_button, WHITE, 10)

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