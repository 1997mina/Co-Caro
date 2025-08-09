import pygame
import sys

from manager.CursorManager import CursorManager
from utils.ResourcePath import resource_path
from ui.components.Button import Button
from manager.SoundManager import SoundManager

# Hằng số cho màu sắc và font chữ
TEXT_COLOR = (30, 30, 30)
TITLE_COLOR = (40, 40, 40)
TWO_PLAYERS_COLOR = (0, 120, 215) # Màu xanh nước biển
TWO_PLAYERS_HOVER_COLOR = (0, 150, 255) # Màu xanh nước biển nhạt hơn khi hover
VS_AI_BUTTON_COLOR = (255, 193, 7) # Màu vàng
VS_AI_HOVER_COLOR = (255, 213, 79) # Màu vàng nhạt hơn khi hover
QUIT_BUTTON_COLOR = (255, 100, 100) # Màu đỏ nhạt
QUIT_HOVER_COLOR = (255, 120, 120)
BG_COLOR = (240, 240, 240)

def show_main_menu(screen):
    """
    Hiển thị menu chính của game và xử lý lựa chọn của người dùng.
    """
    screen_width, screen_height = screen.get_size()

    # Tải hình nền
    background_img = pygame.image.load(resource_path('img/general/Background.jpg')).convert()
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

    # Thiết lập độ mờ cho ảnh nền
    background_img.set_alpha(50)

    # Fonts
    font_title = pygame.font.SysFont("Times New Roman", 90, bold=True)
    font_button_text = pygame.font.SysFont("Times New Roman", 36, bold=True)

    # Tiêu đề game
    title_surf = font_title.render("Cờ Caro", True, TITLE_COLOR)
    title_rect = title_surf.get_rect(center=(screen_width / 2, screen_height / 4 - 50))

    # Tải và thay đổi kích thước hình ảnh cho các nút
    icon_size = 120
    
    # Định nghĩa các nút biểu tượng
    button_size = icon_size + 60 # Tăng kích thước nút để có thêm padding
    button_spacing = 120 # Khoảng cách giữa các nút

    button_total_width = (button_size * 3) + (button_spacing * 2)
    start_x = (screen_width - button_total_width) / 2
    button_y = screen_height / 2 - 60

    sound_manager = SoundManager()

    # Khởi tạo các nút sử dụng lớp Button
    two_players_button = Button(start_x, button_y, button_size, button_size,
 pygame.transform.scale(pygame.image.load(resource_path('img/mainmenu/TwoPlayers.png')).convert_alpha(), (icon_size, icon_size)),
                                sound_manager, color=TWO_PLAYERS_COLOR, hover_color=TWO_PLAYERS_HOVER_COLOR,
                                pressed_color=TWO_PLAYERS_HOVER_COLOR, border_radius=-1, shadow_offset=(5, 5))

    vs_ai_button = Button(start_x + button_size + button_spacing, button_y, button_size, button_size,
                          pygame.transform.scale(pygame.image.load(resource_path('img/mainmenu/vsAI.png')).convert_alpha(), (icon_size, icon_size)),
                          sound_manager, color=VS_AI_BUTTON_COLOR, hover_color=VS_AI_HOVER_COLOR,
                          pressed_color=VS_AI_HOVER_COLOR, border_radius=-1, shadow_offset=(5, 5))

    quit_button = Button(start_x + 2 * (button_size + button_spacing), button_y, button_size, button_size,
                         pygame.transform.scale(pygame.image.load(resource_path('img/general/Quit.png')).convert_alpha(), (icon_size, icon_size)),
                         sound_manager, color=QUIT_BUTTON_COLOR, hover_color=QUIT_HOVER_COLOR,
                         pressed_color=QUIT_HOVER_COLOR, border_radius=-1, shadow_offset=(5, 5))

    buttons = [
        {'name': '2_players', 'button': two_players_button, 'text': 'Chơi 2 người'},
        {'name': 'vs_ai', 'button': vs_ai_button, 'text': 'Chơi với máy'},
        {'name': 'quit', 'button': quit_button, 'text': 'Thoát Game'}
    ]

    cursor_manager = CursorManager()

    # Vòng lặp chính của menu
    while True:
        mouse_pos = pygame.mouse.get_pos()

        # Sử dụng CursorManager để quản lý con trỏ
        cursor_manager = CursorManager() # Reset mỗi frame
        for btn_info in buttons:
            cursor_manager.add_clickable_area(btn_info['button'].rect, btn_info['button'].is_enabled)
        cursor_manager.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for btn_info in buttons:
                if btn_info['button'].handle_event(event):
                    pygame.time.wait(100) # Đợi một chút để âm thanh phát
                    # Khôi phục con trỏ chuột về mặc định trước khi thoát khỏi menu
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return btn_info['name'] # Trả về hành động được chọn

        # Vẽ các thành phần lên màn hình
        screen.fill(BG_COLOR)
        screen.blit(background_img, (0, 0)) # Vẽ hình nền
        screen.blit(title_surf, title_rect)

        for btn_info in buttons:
            btn_info['button'].draw(screen, -1)
            text_surf = font_button_text.render(btn_info['text'], True, TEXT_COLOR)
            text_rect = text_surf.get_rect(center=(btn_info['button'].rect.centerx, btn_info['button'].rect.bottom + 45))
            screen.blit(text_surf, text_rect)

        pygame.display.flip()