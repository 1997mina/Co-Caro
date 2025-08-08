import pygame
import sys

from manager.CursorManager import CursorManager
from utils.ResourcePath import resource_path
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
    background_img = pygame.image.load(resource_path('img/Background.jpg')).convert()
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
    
    two_players_icon = pygame.image.load(resource_path('img/mainmenu/TwoPlayers.png')).convert_alpha()
    two_players_icon = pygame.transform.scale(two_players_icon, (icon_size, icon_size))
    
    vs_ai_icon = pygame.image.load(resource_path('img/mainmenu/vsAI.png')).convert_alpha()
    vs_ai_icon = pygame.transform.scale(vs_ai_icon, (icon_size, icon_size))
    
    quit_icon = pygame.image.load(resource_path('img/mainmenu/Quit.png')).convert_alpha()
    quit_icon = pygame.transform.scale(quit_icon, (icon_size, icon_size))

    # Định nghĩa các nút biểu tượng
    button_width = icon_size + 40 # Tăng kích thước nút để có thêm padding
    button_height = icon_size + 40
    button_spacing = 120 # Khoảng cách giữa các nút

    button_total_width = (button_width * 3) + (button_spacing * 2)
    start_x = (screen_width - button_total_width) / 2
    button_y = screen_height / 2 - 60

    two_players_button_rect = pygame.Rect(start_x, button_y, button_width, button_height)
    vs_ai_button_rect = pygame.Rect(start_x + button_width + button_spacing, button_y, button_width, button_height)
    quit_button_rect = pygame.Rect(start_x + 2 * (button_width + button_spacing), button_y, button_width, button_height)

    # Lưu thông tin các nút vào một dictionary để dễ quản lý, bao gồm cả icon
    buttons = {
        '2_players': {'rect': two_players_button_rect, 'text': 'Chơi 2 người', 'icon': two_players_icon, 'enabled': True},
        'vs_ai': {'rect': vs_ai_button_rect, 'text': 'Chơi với máy', 'icon': vs_ai_icon, 'enabled': True},
        'quit': {'rect': quit_button_rect, 'text': 'Thoát Game', 'icon': quit_icon, 'enabled': True}
    }

    sound_manager = SoundManager()
    cursor_manager = CursorManager()

    # Vòng lặp chính của menu
    while True:
        mouse_pos = pygame.mouse.get_pos()

        # Sử dụng CursorManager để quản lý con trỏ
        cursor_manager = CursorManager() # Reset mỗi frame
        for action, button_info in buttons.items():
            cursor_manager.add_clickable_area(button_info['rect'], button_info['enabled'])
        cursor_manager.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click chuột trái
                    for action, button_info in buttons.items():
                        if button_info['rect'].collidepoint(mouse_pos) and button_info['enabled']:
                            sound_manager.play_button_click()
                            pygame.time.wait(100) # Đợi một chút để âm thanh phát
                            # Khôi phục con trỏ chuột về mặc định trước khi thoát khỏi menu
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                            return action  # Trả về hành động được chọn

        # Vẽ các thành phần lên màn hình
        screen.fill(BG_COLOR)
        screen.blit(background_img, (0, 0)) # Vẽ hình nền
        screen.blit(title_surf, title_rect)

        for action, button_info in buttons.items():
            rect = button_info['rect']
            text = button_info['text']
            icon = button_info['icon']
            enabled = button_info['enabled']

            # Chọn màu dựa trên trạng thái của nút (thường, hover, vô hiệu hóa)
            if rect.collidepoint(mouse_pos) and enabled:
                if action == 'quit':
                    color = QUIT_HOVER_COLOR # Màu đỏ nhạt hơn khi hover
                elif action == 'vs_ai':
                    color = VS_AI_HOVER_COLOR # Màu vàng nhạt hơn khi hover
                else:
                    color = TWO_PLAYERS_HOVER_COLOR
            else:
                if action == 'quit':
                    color = QUIT_BUTTON_COLOR
                elif action == 'vs_ai':
                    color = VS_AI_BUTTON_COLOR # Màu vàng cho nút AI
                else:
                    color = TWO_PLAYERS_COLOR

            # Vẽ nền nút
            pygame.draw.rect(screen, color, rect, border_radius=15) # Tăng border_radius cho nút lớn hơn
            screen.blit(icon, icon.get_rect(center=rect.center))

            text_surf = font_button_text.render(text, True, TEXT_COLOR)
            text_rect = text_surf.get_rect(center=(rect.centerx, rect.bottom + 45))
            screen.blit(text_surf, text_rect)

        pygame.display.flip()