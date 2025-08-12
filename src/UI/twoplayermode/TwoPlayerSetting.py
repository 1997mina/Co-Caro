import pygame

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
PIECE_BUTTON_COLOR = (220, 220, 220)
PIECE_BUTTON_HOVER = (200, 200, 200)
PIECE_BUTTON_SELECTED = (150, 200, 255)

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
        self.input_box1 = pygame.Rect((self.screen_width - input_box_width) / 2, 105, input_box_width, 50)
        self.input_box2 = pygame.Rect((self.screen_width - input_box_width) / 2, 175, input_box_width, 50)

        self.input_box1_ui = InputBox(self.input_box1.x, self.input_box1.y
                                      , self.input_box1.width, self.input_box1.height, 
                                      self.font_label, TEXT_COLOR, (100, 100, 100), (200, 200, 200))
        self.input_box2_ui = InputBox(self.input_box2.x, self.input_box2.y, 
                                      self.input_box2.width, self.input_box2.height, 
                                      self.font_label, TEXT_COLOR, (100, 100, 100), (200, 200, 200))
        
        # --- Cài đặt chọn quân cờ ---
        self.player1_piece = 'X' # Mặc định Người chơi 1 là X

        # Vị trí ô hiển thị quân cờ cho mỗi người chơi
        self.player1_piece_rect = pygame.Rect(self.input_box1.right + 20, self.input_box1.y, self.img_size, self.img_size)
        self.player2_piece_rect = pygame.Rect(self.input_box2.right + 20, self.input_box2.y, self.img_size, self.img_size)

        # Vị trí nút hoán đổi
        swap_button_x = self.player1_piece_rect.right + 15
        swap_button_y = (self.player1_piece_rect.centery + self.player2_piece_rect.centery) / 2 - self.swap_icon_img.get_height() / 2
        self.swap_button_rect = self.swap_icon_img.get_rect(topleft=(swap_button_x, swap_button_y))

        # Các chế độ chơi
        self.modes = {
            "turn_based": {"name": "20 giây mỗi lượt", "time_limit": 20},
            "total_time": {"name": "2 phút tổng cộng", "time_limit": 120}
        }
        self.selected_mode = None # Chế độ mặc định

        # --- Các nút chọn chế độ (Radio button) ---
        self.radio_button_y_start = 325
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
        
        # --- Các nút chọn người đi trước ---
        self.first_turn = None # 'player1' hoặc 'player2'
        
        turn_button_width, turn_button_height = 200, 50
        turn_button_y = self.radio_button_y_start + mode_button_height + 10 + mode_button_height + 100 # Tăng khoảng cách
        turn_button_spacing = 80 # Khoảng cách giữa các nút
        
        self.player1_first_button = Button(self.screen_width / 2 - turn_button_width - turn_button_spacing / 2, turn_button_y, turn_button_width, turn_button_height,
                                          self.font_mode.render("Người chơi 1", True, TEXT_COLOR), self.sound_manager,
                                          color=MODE_BUTTON_COLOR_INACTIVE, hover_color=MODE_BUTTON_HOVER, pressed_color=BLUE_HOVER,
                                          selected_color=BLUE_HOVER, border_radius=10)

        self.player2_first_button = Button(self.screen_width / 2 + turn_button_spacing / 2, turn_button_y, turn_button_width, turn_button_height,
                                      self.font_mode.render("Người chơi 2", True, TEXT_COLOR), self.sound_manager,
                                      color=MODE_BUTTON_COLOR_INACTIVE, hover_color=MODE_BUTTON_HOVER, pressed_color=BLUE_HOVER,
                                      selected_color=BLUE_HOVER, border_radius=10)

        self.turn_buttons = [self.player1_first_button, self.player2_first_button]



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
        self.cursor_manager = CursorManager()

    def _update_selection_buttons(self, selected_button, button_group):
        """Cập nhật trạng thái is_selected cho một nhóm các nút."""
        for button in button_group:
            button.is_selected = (button == selected_button)

    def run(self):
        mouse_pos = pygame.mouse.get_pos()
    
        self.player1_name = self.input_box1_ui.get_text()
        self.player2_name = self.input_box2_ui.get_text()

        # Điều kiện để kích hoạt nút "Bắt đầu"
        is_start_enabled = (self.player1_name.strip() and
                            self.player2_name.strip() and
                            self.player1_piece is not None and # Luôn có giá trị mặc định
                            self.first_turn is not None and
                            self.selected_mode is not None) # Chỉ cần người chơi 1 chọn
        self.start_button.is_enabled = is_start_enabled

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Xử lý sự kiện cho các thành phần UI
            self.input_box1_ui.handle_event(event)
            self.input_box2_ui.handle_event(event)

            # Xử lý sự kiện cho các nút chọn quân cờ
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Xử lý cho nút hoán đổi
                if self.swap_button_rect.collidepoint(event.pos):
                    self.player1_piece = 'O' if self.player1_piece == 'X' else 'X'
                    self.sound_manager.play_button_click()

            if self.turn_based_button.handle_event(event):
                self.selected_mode = "turn_based"
                self._update_selection_buttons(self.turn_based_button, [self.turn_based_button, self.total_time_button])
            
            if self.total_time_button.handle_event(event):
                self.selected_mode = "total_time"
                self._update_selection_buttons(self.total_time_button, [self.turn_based_button, self.total_time_button])

            # Xử lý sự kiện cho các nút chọn lượt đi đầu
            if self.player1_first_button.handle_event(event):
                self.first_turn = 'player1'
                self._update_selection_buttons(self.player1_first_button, self.turn_buttons)
            if self.player2_first_button.handle_event(event):
                self.first_turn = 'player2'
                self._update_selection_buttons(self.player2_first_button, self.turn_buttons)

            if self.start_button.handle_event(event):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                # Trả về dữ liệu thô, việc xử lý logic sẽ do GameSession đảm nhiệm
                return (
                    self.player1_name.strip(), 
                    self.player2_name.strip(), 
                    self.player1_piece, # Quân cờ của người chơi 1
                    self.selected_mode, 
                    self.modes[self.selected_mode]["time_limit"], 
                    self.first_turn # 'player1' hoặc 'player2'
                )
            
            if self.back_button.handle_event(event):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                return 'back'


        # --- Vẽ lên màn hình ---
        self.screen.fill(WHITE)
        self.screen.blit(self.background_img, (0, 0))

        # Vẽ các ô nhập tên người chơi
        super()._draw_section_title(self.screen, "Nhập tên người chơi:", TEXT_COLOR, self.font_label, 75, self.screen_width)
        super()._draw_section_title(self.screen, "Người chơi 1:", TEXT_COLOR, self.font_label, self.input_box1.y - 30, self.screen_width, align_left_of_box=self.input_box1)
        self.input_box1_ui.draw(self.screen)
        super()._draw_section_title(self.screen, "Người chơi 2:", TEXT_COLOR, self.font_label, self.input_box2.y - 30, self.screen_width, align_left_of_box=self.input_box2) # This line is already present in the original code, so it's not part of the diff.
        self.input_box2_ui.draw(self.screen)

        # --- Vẽ khu vực quân cờ ---
        # Xác định quân cờ của người chơi 2
        player2_piece = 'O' if self.player1_piece == 'X' else 'X'
        
        # Lấy hình ảnh tương ứng
        p1_img = self.x_img if self.player1_piece == 'X' else self.o_img
        p2_img = self.x_img if player2_piece == 'X' else self.o_img
        
        # Vẽ quân cờ cho mỗi người chơi
        self.screen.blit(p1_img, self.player1_piece_rect)
        self.screen.blit(p2_img, self.player2_piece_rect)
        
        # Vẽ nút hoán đổi
        self.screen.blit(self.swap_icon_img, self.swap_button_rect)
            
        # Vẽ lựa chọn chế độ chơi
        super()._draw_section_title(self.screen, "Chọn chế độ thời gian:", TEXT_COLOR, self.font_label, self.radio_button_y_start - 30, self.screen_width)
        self.turn_based_button.draw(self.screen)
        self.total_time_button.draw(self.screen)

        # Vẽ lựa chọn người đi trước
        super()._draw_section_title(self.screen, "Chọn người đi trước:", TEXT_COLOR, self.font_label, self.player1_first_button.rect.y - 30, self.screen_width)
        self.player1_first_button.draw(self.screen)
        self.player2_first_button.draw(self.screen)

        self.start_button.draw(self.screen)
        self.back_button.draw(self.screen)

        # Cập nhật con trỏ chuột
        self.cursor_manager.add_clickable_area(self.start_button.rect, self.start_button.is_enabled)
        self.cursor_manager.add_clickable_area(self.back_button.rect, self.back_button.is_enabled)
        self.cursor_manager.add_clickable_area(self.turn_based_button.rect, True)
        self.cursor_manager.add_clickable_area(self.total_time_button.rect, True)
        self.cursor_manager.add_clickable_area(self.player1_first_button.rect, True)
        self.cursor_manager.add_clickable_area(self.player2_first_button.rect, True)
        self.cursor_manager.add_clickable_area(self.swap_button_rect, True)
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