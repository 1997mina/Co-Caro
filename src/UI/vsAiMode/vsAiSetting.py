import pygame
import sys

from manager.CursorManager import CursorManager
from utils.ResourcePath import resource_path
from ui.general.SettingUI import SettingUI
from ui.components.InputBox import InputBox

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

        # Tải và thay đổi kích thước hình ảnh X và O
        img_size = 80
        self.x_img = pygame.transform.scale(pygame.image.load(resource_path('img/X.png')).convert_alpha(), (img_size, img_size))
        self.o_img = pygame.transform.scale(pygame.image.load(resource_path('img/O.png')).convert_alpha(), (img_size, img_size))

        # --- Ô nhập tên người chơi (sử dụng lớp InputBox) ---
        input_box_width = 500
        self.player_name_input_box = InputBox(
            self.screen_width / 2 - input_box_width / 2, 80, input_box_width, 50,
            self.font_label, TEXT_COLOR, DARK_GRAY, DARK_WHITE
        )

        # --- Trạng thái và các thành phần UI ---
        self.player_piece = None  # 'X' hoặc 'O'
        self.first_turn = None # 'player' hoặc 'ai'
        self.difficulty = None # 'easy', 'medium', 'hard'

        # 1. Các nút chọn quân cờ
        self.x_button_rect = pygame.Rect(self.screen_width / 2 - 150, 220, 120, 120)
        self.o_button_rect = pygame.Rect(self.screen_width / 2 + 30, 220, 120, 120)

        # 2. Các nút radio chọn lượt đi đầu
        self.radio_button_y = 450 # Y position for both radio buttons
        self.radio_button_radius = 15
        self.radio_player_first_rect = pygame.Rect(self.screen_width / 2 - 200, self.radio_button_y - self.radio_button_radius, 180, self.radio_button_radius * 2)
        self.radio_ai_first_rect = pygame.Rect(self.screen_width / 2 + 20, self.radio_button_y - self.radio_button_radius, 180, self.radio_button_radius * 2)

        # 3. Các nút chọn độ khó
        difficulty_button_width = 150
        difficulty_button_height = 50
        self.easy_button_rect = pygame.Rect(self.screen_width / 2 - 250, 560, difficulty_button_width, difficulty_button_height)
        self.medium_button_rect = pygame.Rect(self.screen_width / 2 - 75, 560, difficulty_button_width, difficulty_button_height)
        self.hard_button_rect = pygame.Rect(self.screen_width / 2 + 100, 560, difficulty_button_width, difficulty_button_height)

        self.cursor_manager = CursorManager()

    def run(self):
        """
        Hiển thị màn hình cài đặt cho ván chơi với máy.
        Trả về một tuple chứa (tên người chơi, quân cờ người chơi, người đi trước, độ khó) hoặc None nếu quay lại.
        """
        # Cập nhật trạng thái của ô nhập liệu (ví dụ: con trỏ nhấp nháy)
        self.player_name_input_box.update()
        mouse_pos = pygame.mouse.get_pos() # Cập nhật vị trí chuột mỗi vòng lặp

        # Lấy tên người chơi từ InputBox để kiểm tra điều kiện bắt đầu
        player_name = self.player_name_input_box.get_text()
        is_start_enabled = (self.player_piece is not None and 
                            player_name != "" and 
                            self.first_turn is not None and 
                            self.difficulty is not None)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Chuyển sự kiện cho ô nhập liệu để nó tự xử lý
            self.player_name_input_box.handle_event(event)

            # Xử lý các sự kiện click chuột cho các nút khác
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.x_button_rect.collidepoint(mouse_pos):
                    if self.player_piece != 'X': self.sound_manager.play_button_click()
                    self.player_piece = 'X'
                elif self.o_button_rect.collidepoint(mouse_pos):
                    if self.player_piece != 'O': self.sound_manager.play_button_click()
                    self.player_piece = 'O'
                elif self.radio_player_first_rect.collidepoint(mouse_pos):
                    if self.first_turn != 'player': self.sound_manager.play_button_click()
                    self.first_turn = 'player'
                elif self.radio_ai_first_rect.collidepoint(mouse_pos):
                    if self.first_turn != 'ai': self.sound_manager.play_button_click()
                    self.first_turn = 'ai'
                elif self.easy_button_rect.collidepoint(mouse_pos):
                    if self.difficulty != 'easy': self.sound_manager.play_button_click()
                    self.difficulty = 'easy'
                elif self.medium_button_rect.collidepoint(mouse_pos):
                    if self.difficulty != 'medium': self.sound_manager.play_button_click()
                    self.difficulty = 'medium'
                elif self.hard_button_rect.collidepoint(mouse_pos):
                    if self.difficulty != 'hard': self.sound_manager.play_button_click()
                    self.difficulty = 'hard'
                elif self.start_button.collidepoint(mouse_pos) and is_start_enabled:
                    self.sound_manager.play_button_click()
                    pygame.time.wait(100)
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return self.player_name_input_box.get_text(), self.player_piece, self.first_turn, self.difficulty
                elif self.back_button.collidepoint(mouse_pos):
                    self.sound_manager.play_button_click()
                    pygame.time.wait(100)
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return 'back'
            
        # --- Vẽ các thành phần ---
        self.screen.fill(WHITE)
        self.screen.blit(self.background_img, (0, 0))

        # Sử dụng CursorManager để xử lý con trỏ chuột
        self.cursor_manager = CursorManager() # Reset mỗi frame
        self.cursor_manager.add_text_input(self.player_name_input_box)
        self.cursor_manager.add_clickable_area(self.start_button, is_start_enabled)
        self.cursor_manager.add_clickable_area(self.back_button)
        self.cursor_manager.add_clickable_area(self.x_button_rect)
        self.cursor_manager.add_clickable_area(self.o_button_rect)
        self.cursor_manager.add_clickable_area(self.easy_button_rect)
        self.cursor_manager.add_clickable_area(self.medium_button_rect)
        self.cursor_manager.add_clickable_area(self.hard_button_rect)
        self.cursor_manager.update(mouse_pos)

        super()._draw_section_title(self.screen, "Nhập tên của bạn:", TEXT_COLOR, self.font_label, 0, self.screen_width, align_left_of_box=None)
        self.player_name_input_box.draw(self.screen)

        # Vẽ phần chọn quân cờ
        super()._draw_section_title(self.screen, "Chọn quân cờ của bạn:", TEXT_COLOR, self.font_label, 180, self.screen_width)
        super().draw_piece_button(self.screen, self.x_button_rect, self.x_img, self.player_piece, 'X', mouse_pos, YELLOW, SUPER_LIGHT_GRAY, DARK_WHITE)
        super().draw_piece_button(self.screen, self.o_button_rect, self.o_img, self.player_piece, 'O', mouse_pos, YELLOW, SUPER_LIGHT_GRAY, DARK_WHITE)
        
        # Vẽ phần chọn lượt đi
        super()._draw_section_title(self.screen, "Chọn người đi trước:", TEXT_COLOR, self.font_label, 400, self.screen_width)
        
        # Vẽ các nút radio sử dụng hàm mới
        super().draw_radio_button(self.screen, self.radio_player_first_rect.x + self.radio_button_radius, self.radio_player_first_rect.centery,
                          self.radio_button_radius, self.first_turn == 'player', "Bạn đi trước", self.font_mode, TEXT_COLOR, YELLOW)
        super().draw_radio_button(self.screen, self.radio_ai_first_rect.x + self.radio_button_radius, self.radio_ai_first_rect.centery,
                          self.radio_button_radius, self.first_turn == 'ai', "Máy đi trước", self.font_mode, TEXT_COLOR, YELLOW)

        # Vẽ phần chọn độ khó
        super()._draw_section_title(self.screen, "Chọn độ khó:", TEXT_COLOR, self.font_label, 520, self.screen_width)

        # Nút dễ
        super().draw_button(self.screen, self.easy_button_rect, YELLOW if self.difficulty == 'easy' else (LIGHT_GRAY if self.easy_button_rect.collidepoint(mouse_pos) else MEDIUM_GRAY), "Dễ", self.font_mode, TEXT_COLOR, 10)

        # Nút trung bình
        super().draw_button(self.screen, self.medium_button_rect, YELLOW if self.difficulty == 'medium' else (LIGHT_GRAY if self.medium_button_rect.collidepoint(mouse_pos) else MEDIUM_GRAY), "Trung bình", self.font_mode, TEXT_COLOR, 10)

        # Nút khó
        super().draw_button(self.screen, self.hard_button_rect, YELLOW if self.difficulty == 'hard' else (LIGHT_GRAY if self.hard_button_rect.collidepoint(mouse_pos) else MEDIUM_GRAY), "Khó", self.font_mode, TEXT_COLOR, 10)

        # Vẽ nút Bắt đầu và Quay lại
        start_btn_color = (YELLOW_HOVER if self.start_button.collidepoint(mouse_pos) else YELLOW) if is_start_enabled else LIGHT_GRAY # Màu nền
        start_text_color = TEXT_COLOR if is_start_enabled else WHITE # Màu chữ
        super().draw_button(self.screen, self.start_button, start_btn_color, "Bắt đầu", self.font_button, start_text_color, 10)

        back_btn_color = DARK_GRAY_HOVER if self.back_button.collidepoint(mouse_pos) else DARK_GRAY # Màu nền
        super().draw_button(self.screen, self.back_button, back_btn_color, "Quay lại", self.font_button, WHITE, 10) # Màu chữ luôn là trắng

        pygame.display.flip()

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