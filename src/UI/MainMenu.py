import pygame
import sys
import os

# Hằng số cho màu sắc và font chữ
TITLE_COLOR = (40, 40, 40)
BUTTON_COLOR = (0, 150, 136)
BUTTON_HOVER_COLOR = (0, 180, 160)
BUTTON_DISABLED_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = (255, 255, 255)
BG_COLOR = (240, 240, 240)

def show_main_menu(screen):
    """
    Hiển thị menu chính của game và xử lý lựa chọn của người dùng.
    """
    screen_width, screen_height = screen.get_size()

    # Tải hình nền
    background_img = pygame.image.load(os.path.join('img', 'Background.jpg')).convert()
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

    # Thiết lập độ mờ cho ảnh nền
    background_img.set_alpha(50)

    # Fonts
    font_title = pygame.font.SysFont("Times New Roman", 96, bold=True)
    font_button = pygame.font.SysFont("Times New Roman", 40, bold=True)

    # Tiêu đề game
    title_surf = font_title.render("Cờ Caro", True, TITLE_COLOR)
    title_rect = title_surf.get_rect(center=(screen_width / 2, screen_height / 4))

    # Định nghĩa các nút
    button_width, button_height = 400, 70
    button_y_start = screen_height / 2 - 50
    button_spacing = 90

    two_players_button = pygame.Rect(0, 0, button_width, button_height)
    two_players_button.center = (screen_width / 2, button_y_start)

    vs_ai_button = pygame.Rect(0, 0, button_width, button_height)
    vs_ai_button.center = (screen_width / 2, button_y_start + button_spacing)

    quit_button = pygame.Rect(0, 0, button_width, button_height)
    quit_button.center = (screen_width / 2, button_y_start + 2 * button_spacing)

    # Lưu thông tin các nút vào một dictionary để dễ quản lý
    buttons = {
        '2_players': {'rect': two_players_button, 'text': 'Chơi 2 người', 'enabled': True},
        'vs_ai': {'rect': vs_ai_button, 'text': 'Chơi với máy (Chưa có)', 'enabled': False},
        'quit': {'rect': quit_button, 'text': 'Thoát Game', 'enabled': True}
    }

    # Vòng lặp chính của menu
    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click chuột trái
                    for action, button_info in buttons.items():
                        if button_info['rect'].collidepoint(mouse_pos) and button_info['enabled']:
                            # Khôi phục con trỏ chuột về mặc định trước khi thoát khỏi menu
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                            return action  # Trả về hành động được chọn

        # Thay đổi con trỏ chuột khi di chuột qua các nút
        cursor_changed = False
        for action, button_info in buttons.items():
            if button_info['rect'].collidepoint(mouse_pos) and button_info['enabled']:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                cursor_changed = True
                break
        if not cursor_changed:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Vẽ các thành phần lên màn hình
        screen.fill(BG_COLOR)
        screen.blit(background_img, (0, 0)) # Vẽ hình nền
        screen.blit(title_surf, title_rect)

        for action, button_info in buttons.items():
            rect = button_info['rect']
            text = button_info['text']
            enabled = button_info['enabled']

            # Chọn màu dựa trên trạng thái của nút (thường, hover, vô hiệu hóa)
            if not enabled:
                color = BUTTON_DISABLED_COLOR
            elif rect.collidepoint(mouse_pos):
                color = BUTTON_HOVER_COLOR
            else:
                color = BUTTON_COLOR

            pygame.draw.rect(screen, color, rect, border_radius=15)
            text_surf = font_button.render(text, True, BUTTON_TEXT_COLOR)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        pygame.display.flip()