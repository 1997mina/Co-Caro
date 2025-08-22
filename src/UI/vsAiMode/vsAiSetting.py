import pygame
import sys

from utils.ResourcePath import resource_path
from ui.settings.ModeSetting import SettingUI
from components.Button import Button
from manager.CursorManager import CursorManager
from components.InputBox import InputBox
from components.Dropdown import Dropdown

# Hằng số cho màu sắc và font chữ, giữ cho giao diện nhất quán
WHITE = (255, 255, 255)
DARK_WHITE = (200, 200, 200)
TEXT_COLOR = (40, 40, 40)
YELLOW = (255, 193, 7)
YELLOW_HOVER = (255, 213, 79) # Màu vàng nhạt hơn khi hover
DARK_GRAY = (100, 100, 100)
DARK_GRAY_HOVER = (130, 130, 130)
MEDIUM_GRAY = (150, 150, 150)
LIGHT_GRAY = (180, 180, 180)
SUPER_LIGHT_GRAY = (220, 220, 220)

class VsAiSetting(SettingUI):
    def __init__(self, screen):
        super().__init__(screen)

        self.x_img, self.o_img = super().load_piece(80)

        # --- Ô nhập tên người chơi (sử dụng lớp InputBox) ---
        input_box_width = 400 # Giảm chiều rộng để có chỗ cho nút Dán
        self.player_name_input_box = InputBox(
            self.screen_width / 2 - input_box_width / 2, 80, input_box_width, 50,
            self.font_label, TEXT_COLOR, DARK_GRAY, DARK_WHITE
        )

        # --- Trạng thái và các thành phần UI ---
        self.player_piece = None  # 'X' hoặc 'O'
        self.first_turn = 'player' # 'player' hoặc 'ai', mặc định là người chơi đi trước
        self.difficulty = 'medium' # 'easy', 'medium', 'hard'

        # 1. Các nút chọn quân cờ
        button_size = 120
        button_y = 220
        
        self.x_button = Button(self.screen_width / 2 - 150, button_y, button_size, button_size,
                               self.x_img, self.sound_manager,
                               color=SUPER_LIGHT_GRAY, hover_color=LIGHT_GRAY,
                               pressed_color=YELLOW_HOVER, selected_color=YELLOW,
                               border_radius=10, shadow_offset=(5, 5))
        
        self.o_button = Button(self.screen_width / 2 + 30, button_y, button_size, button_size,
                               self.o_img, self.sound_manager,
                               color=SUPER_LIGHT_GRAY, hover_color=LIGHT_GRAY,
                               pressed_color=YELLOW_HOVER, selected_color=YELLOW,
                               border_radius=10, shadow_offset=(5, 5))

        self.piece_buttons = [self.x_button, self.o_button]

        # Kích thước Dropdown
        dropdown_width = 350
        dropdown_height = 50

        # 2. Phần chọn độ khó
        difficulty_options = ["Dễ", "Trung bình", "Khó"]
        self.difficulty_dropdown = Dropdown(0, 0, dropdown_width, dropdown_height,
                                            difficulty_options, "Trung bình", self.sound_manager,
                                            "Chọn độ khó:", option_hover_color=YELLOW_HOVER)
        self.difficulty_dropdown.set_center_component(self.screen_width // 2, 440)

        # 3. Dropdown chọn lượt đi đầu
        first_turn_options = ["Bạn đi trước", "Máy đi trước"]
        self.first_turn_dropdown = Dropdown(0, 0, dropdown_width, dropdown_height,
                                            first_turn_options, "Bạn đi trước", self.sound_manager,
                                            "Người đi trước:", option_hover_color=YELLOW_HOVER)
        self.first_turn_dropdown.set_center_component(self.screen_width // 2, 570)

        # Nút Bắt đầu
        button_width = 200
        button_height = 60
        start_button_x = self.screen_width / 2 + 50
        start_button_y = 700
        
        self.start_button = Button(
            start_button_x, start_button_y, button_width, button_height,
            self.font_button.render("Bắt đầu", True, TEXT_COLOR), self.sound_manager,
            color=YELLOW, hover_color=YELLOW_HOVER, pressed_color=YELLOW_HOVER,
            disabled_color=LIGHT_GRAY, border_radius=10
        )

        self.cursor_manager = CursorManager()
    
    def _update_selection_buttons(self, selected_button, button_group):
        """Cập nhật trạng thái is_selected cho một nhóm các nút."""
        for button in button_group:
            button.is_selected = (button == selected_button)

    def run(self):
        """
        Hiển thị màn hình cài đặt cho ván chơi với máy.
        Trả về một tuple chứa (tên người chơi, quân cờ người chơi, người đi trước, độ khó) hoặc None nếu quay lại.
        """
        # Cập nhật trạng thái của ô nhập liệu (ví dụ: con trỏ nhấp nháy)
        self.player_name_input_box.update()

        # Lấy tên người chơi từ InputBox để kiểm tra điều kiện bắt đầu
        player_name = self.player_name_input_box.get_text()
        is_start_enabled = (self.player_piece is not None and 
                            player_name.strip() != "") # Các dropdown đã có giá trị mặc định
        self.start_button.is_enabled = is_start_enabled
        self.difficulty = self._get_english_difficulty(self.difficulty_dropdown.get_selected_option()) # Lấy giá trị từ dropdown

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos() # Lấy mouse_pos ở đầu vòng lặp sự kiện
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Chuyển sự kiện cho ô nhập liệu để nó tự xử lý
            self.player_name_input_box.handle_event(event)

            # --- Xử lý sự kiện cho các nút chọn quân cờ ---
            if self.x_button.handle_event(event):
                self.player_piece = 'X'
                self._update_selection_buttons(self.x_button, self.piece_buttons)
            if self.o_button.handle_event(event):
                self.player_piece = 'O'
                self._update_selection_buttons(self.o_button, self.piece_buttons)

            # --- Xử lý sự kiện cho dropdown độ khó ---
            changed, handled = self.difficulty_dropdown.handle_event(event)
            if changed:
                self.difficulty = self._get_english_difficulty(self.difficulty_dropdown.get_selected_option())
            if handled:
                continue

            # Xử lý sự kiện cho dropdown chọn lượt đi đầu
            changed, handled = self.first_turn_dropdown.handle_event(event)
            if changed:
                self.first_turn = 'player' if self.first_turn_dropdown.get_selected_option() == "Bạn đi trước" else 'ai'
            if handled:
                continue

            # Xử lý sự kiện cho các nút Bắt đầu và Quay lại
            if self.start_button.handle_event(event):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                return self.player_name_input_box.get_text(), self.player_piece, self.first_turn, self.difficulty
            if self.back_button.handle_event(event):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                return 'back'
            
        # --- Vẽ các thành phần ---
        self.screen.fill(WHITE)
        self.screen.blit(self.background_img, (0, 0))

        super()._draw_section_title(self.screen, "Nhập tên của bạn:", TEXT_COLOR, self.font_label, 50, self.screen_width, align_left_of_box=None)
        self.player_name_input_box.draw(self.screen)

        # Vẽ phần chọn quân cờ
        mouse_pos = pygame.mouse.get_pos()
        super()._draw_section_title(self.screen, "Chọn quân cờ của bạn:", TEXT_COLOR, self.font_label, 190, self.screen_width)
        self.x_button.draw(self.screen)
        self.o_button.draw(self.screen)

        # Vẽ các nút Bắt đầu và Quay lại
        self.start_button.draw(self.screen)
        self.back_button.draw(self.screen)

        # Vẽ Dropdown
        self.first_turn_dropdown.draw(self.screen)
        self.difficulty_dropdown.draw(self.screen)

        # Cập nhật con trỏ chuột cho InputBox
        self.player_name_input_box.handle_mouse_cursor(mouse_pos)

        # Cập nhật con trỏ chuột
        self.cursor_manager.add_clickable_area(self.start_button.rect, self.start_button.is_enabled)
        self.cursor_manager.add_clickable_area(self.back_button.rect, self.back_button.is_enabled)
        self.cursor_manager.add_clickable_area(self.x_button.rect, True)
        self.cursor_manager.add_clickable_area(self.o_button.rect, True)
        self.first_turn_dropdown.add_to_cursor_manager(self.cursor_manager)
        self.difficulty_dropdown.add_to_cursor_manager(self.cursor_manager)
        self.cursor_manager.update(mouse_pos)

        pygame.display.flip()

    def _get_english_difficulty(self, difficulty_vn):
        """Chuyển đổi độ khó tiếng Việt sang tiếng Anh."""
        if difficulty_vn == 'Dễ':
            return 'easy'
        elif difficulty_vn == 'Trung bình':
            return 'medium'
        elif difficulty_vn == 'Khó':
            return 'hard'

def get_ai_game_settings(screen):
    """
    Hàm tiện ích để khởi tạo và gọi màn hình cài đặt AI.
    """
    settings_ui = VsAiSetting(screen)
    running = True

    while running:
        result = settings_ui.run() # run() trả về tuple, 'back', hoặc None
        if result == 'back':
            return None # Quay lại menu chính
        elif result is not None:
            return result # Trả về cài đặt

        pygame.time.wait(10) # Đợi một chút để tránh ngốn CPU