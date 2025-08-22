import pygame

from manager.CursorManager import CursorManager
from components.Button import Button
from components.InputBox import InputBox
from components.Spinner import Spinner
from components.Dropdown import Dropdown
from ui.settings.ModeSetting import SettingUI
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
        self.img_size = 50
        self.x_img, self.o_img = super().load_piece(self.img_size)
        self.player1_piece = 'X' # Mặc định Người chơi 1 là X

        # Vị trí ô hiển thị quân cờ cho mỗi người chơi
        self.player1_piece_rect = pygame.Rect(self.input_box1.right + 20, self.input_box1.y, self.img_size, self.img_size)
        self.player2_piece_rect = pygame.Rect(self.input_box2.right + 20, self.input_box2.y, self.img_size, self.img_size)

        # Vị trí nút hoán đổi
        swap_button_x = self.player1_piece_rect.right + 15
        swap_button_y = (self.player1_piece_rect.centery + self.player2_piece_rect.centery) / 2 - self.swap_icon_img.get_height() / 2
        self.swap_button = Button(
            swap_button_x, swap_button_y, self.swap_icon_img.get_width(), self.swap_icon_img.get_height(),
            self.swap_icon_img, self.sound_manager,
            color=(240, 240, 240), hover_color=(200, 200, 200), pressed_color=(180, 180, 180),
            border_radius=5
        )

        # --- Dropdown chọn người đi trước ---
        self.first_turn = 'player1' # 'player1' hoặc 'player2'
        dropdown_width = 350
        dropdown_height = 50
        self.first_turn_dropdown = Dropdown(
            0, 0, dropdown_width, dropdown_height,
            ["Người chơi 1", "Người chơi 2"], "Người chơi 1", self.sound_manager,
            label_text="Người đi trước:", option_hover_color=BLUE_HOVER
        )
        self.first_turn_dropdown.set_center_component(self.screen_width // 2, 325)

        # --- Dropdown chọn chế độ thời gian ---
        self.time_mode_options = {
            "Theo lượt": "turn_based",
            "Tổng thời gian": "total_time",
            "Không giới hạn": "no_time"
        }
        self.selected_mode = "no_time" # Chế độ mặc định
        self.time_mode_dropdown = Dropdown(
            0, 0, dropdown_width, dropdown_height,
            list(self.time_mode_options.keys()), "Không giới hạn", self.sound_manager,
            label_text="Chế độ thời gian:", option_hover_color=BLUE_HOVER
        )
        self.time_mode_dropdown.set_center_component(self.screen_width // 2, self.first_turn_dropdown.rect.bottom + 120)

        # --- Spinner để tùy chỉnh thời gian ---
        spinner_y = self.time_mode_dropdown.rect.bottom + 100
        spinner_width = 150
        spinner_height = 50

        # Spinner cho chế độ theo lượt (giây)
        self.turn_time_options = [5, 10, 15, 20, 25, 30, 40]
        self.turn_time_spinner = Spinner(0, 0, spinner_width, spinner_height,
                                         min_val=None, max_val=None, # Không dùng cho chế độ list
                                         initial_val=20,
                                         sound_manager=self.sound_manager,
                                         label_text="Thời gian mỗi lượt:",
                                         options_list=self.turn_time_options,
                                         label_suffix="giây")
        self.turn_time_spinner.set_center_component(self.screen_width // 2, spinner_y)

        # Spinner cho chế độ tổng thời gian với các giá trị tùy chỉnh
        self.total_time_map = {
            "0:30": 30, "1:00": 60, "2:00": 120, 
            "3:00": 180, "5:00": 300, "10:00": 600
        }
        self.total_time_spinner = Spinner(0, 0, spinner_width, spinner_height,
                                          min_val=None, max_val=None, # Không dùng cho chế độ list
                                          initial_val="2:00", 
                                          sound_manager=self.sound_manager, 
                                          label_text="Thời gian tổng cộng:",
                                          options_list=list(self.total_time_map.keys()))
        self.total_time_spinner.set_center_component(self.screen_width // 2, spinner_y)

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


    def run(self):
        mouse_pos = pygame.mouse.get_pos()
    
        self.player1_name = self.input_box1_ui.get_text()
        self.player2_name = self.input_box2_ui.get_text()

        # Điều kiện để kích hoạt nút "Bắt đầu"
        is_start_enabled = (self.player1_name.strip() and
                            self.player2_name.strip())
        self.start_button.is_enabled = is_start_enabled

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Xử lý sự kiện cho các thành phần UI
            self.input_box1_ui.handle_event(event)
            self.input_box2_ui.handle_event(event)

            # Xử lý sự kiện cho nút hoán đổi
            if self.swap_button.handle_event(event):
                self.player1_piece = 'O' if self.player1_piece == 'X' else 'X'

            # Xử lý sự kiện cho dropdown chọn chế độ thời gian
            changed, handled = self.time_mode_dropdown.handle_event(event)
            if changed:
                selected_mode_text = self.time_mode_dropdown.get_selected_option()
                self.selected_mode = self.time_mode_options[selected_mode_text]
            if handled:
                continue
            
            if self.selected_mode == 'turn_based':
                self.turn_time_spinner.handle_event(event)
            elif self.selected_mode == 'total_time':
                self.total_time_spinner.handle_event(event)

            changed, handled = self.first_turn_dropdown.handle_event(event)
            if changed:
                selected_option = self.first_turn_dropdown.get_selected_option()
                if selected_option == "Người chơi 1":
                    self.first_turn = 'player1'
                elif selected_option == "Người chơi 2":
                    self.first_turn = 'player2'
            if handled:
                continue

            # Xử lý sự kiện cho nút Bắt đầu
            if self.start_button.handle_event(event):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                
                # Xác định giới hạn thời gian dựa trên chế độ và giá trị spinner
                time_limit = None
                if self.selected_mode == 'turn_based':
                    time_limit = self.turn_time_spinner.get_value()
                elif self.selected_mode == 'total_time':
                    selected_time_str = self.total_time_spinner.get_value()
                    time_limit = self.total_time_map[selected_time_str]

                return (
                    self.player1_name.strip(), 
                    self.player2_name.strip(), 
                    self.player1_piece, # Quân cờ của người chơi 1
                    self.selected_mode, 
                    time_limit,
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
        self.swap_button.draw(self.screen)

        # Vẽ spinner tương ứng với chế độ đã chọn
        if self.selected_mode == 'turn_based':
            self.turn_time_spinner.draw(self.screen)
        elif self.selected_mode == 'total_time':
            self.total_time_spinner.draw(self.screen)

        self.start_button.draw(self.screen)
        self.back_button.draw(self.screen)

        # Vẽ lựa chọn người đi trước
        self.first_turn_dropdown.draw(self.screen)

        # Vẽ dropdown chọn chế độ thời gian
        self.time_mode_dropdown.draw(self.screen)

        # Cập nhật con trỏ chuột
        self.cursor_manager.add_clickable_area(self.start_button.rect, self.start_button.is_enabled)
        self.cursor_manager.add_clickable_area(self.back_button.rect, self.back_button.is_enabled)
        self.time_mode_dropdown.add_to_cursor_manager(self.cursor_manager)
        
        if self.selected_mode == 'turn_based':
            self.turn_time_spinner.add_to_cursor_manager(self.cursor_manager)
        elif self.selected_mode == 'total_time':
            self.total_time_spinner.add_to_cursor_manager(self.cursor_manager)
        self.first_turn_dropdown.add_to_cursor_manager(self.cursor_manager) # Thêm dropdown vào cursor manager
        self.cursor_manager.add_clickable_area(self.swap_button.rect, True) # Thêm nút hoán đổi vào cursor manager
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