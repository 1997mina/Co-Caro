import pygame
import os
import sys

from manager.SoundManager import SoundManager

# Hằng số cho màu sắc và font chữ, giữ cho giao diện nhất quán
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (40, 40, 40)
VS_AI_COLOR = (255, 193, 7)
START_BUTTON_COLOR = (204, 0, 0)
START_BUTTON_HOVER_COLOR = (230, 0, 0)
INPUT_BOX_COLOR_INACTIVE = (200, 200, 200)
INPUT_BOX_COLOR_ACTIVE = (100, 100, 100)
START_BUTTON_DISABLED_COLOR = (180, 180, 180)
BUTTON_TEXT_COLOR = (255, 255, 255)
BACK_BUTTON_COLOR = (100, 100, 100)
BACK_BUTTON_HOVER_COLOR = (130, 130, 130)
PIECE_BG_COLOR = (220, 220, 220)
PIECE_BG_HOVER_COLOR = (200, 200, 200)

def get_ai_game_settings(screen):
    """
    Hiển thị màn hình cài đặt cho ván chơi với máy.
    Trả về một tuple chứa (tên người chơi, quân cờ người chơi, người đi trước) hoặc None nếu quay lại.
    """
    screen_width, screen_height = screen.get_size()
    font_label = pygame.font.SysFont("Times New Roman", 36)
    font_input = pygame.font.SysFont("Times New Roman", 32)
    font_button = pygame.font.SysFont("Times New Roman", 40, bold=True)
    font_mode = pygame.font.SysFont("Times New Roman", 28)

    # Tải hình nền
    background_img = pygame.image.load(os.path.join('img', 'Background.jpg')).convert()
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
    background_img.set_alpha(50)

    # Tải và thay đổi kích thước hình ảnh X và O
    img_size = 80
    x_img = pygame.transform.scale(pygame.image.load('img/X.png').convert_alpha(), (img_size, img_size))
    o_img = pygame.transform.scale(pygame.image.load('img/O.png').convert_alpha(), (img_size, img_size))

    # --- Ô nhập tên người chơi ---
    input_box_width = 500
    player_name_input_box = pygame.Rect(screen_width / 2 - input_box_width / 2, 80, input_box_width, 50)
    player_name = ""
    active_box = False # Trạng thái ô nhập liệu có đang được chọn không

    # --- Trạng thái và các thành phần UI ---
    player_piece = None  # 'X' hoặc 'O'
    first_turn = 'player'  # 'player' hoặc 'ai'

    # 1. Các nút chọn quân cờ
    x_button_rect = pygame.Rect(screen_width / 2 - 150, 240, 120, 120)
    o_button_rect = pygame.Rect(screen_width / 2 + 30, 240, 120, 120)

    # 2. Các nút radio chọn lượt đi đầu
    radio_button_y = 480 # Y position for both radio buttons
    radio_button_radius = 15
    radio_player_first_rect = pygame.Rect(screen_width / 2 - 200, radio_button_y - radio_button_radius, 180, radio_button_radius * 2)
    radio_ai_first_rect = pygame.Rect(screen_width / 2 + 20, radio_button_y - radio_button_radius, 180, radio_button_radius * 2)

    # 3. Nút Bắt đầu và Quay lại
    button_width, button_height = 200, 60
    start_button = pygame.Rect(screen_width / 2 + 50, 650, button_width, button_height)
    back_button = pygame.Rect(screen_width / 2 - 50 - button_width, 650, button_width, button_height)

    sound_manager = SoundManager()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos() # Cập nhật vị trí chuột mỗi vòng lặp
        is_start_enabled = player_piece is not None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if player_name_input_box.collidepoint(mouse_pos):
                    active_box = True
                else:
                    active_box = False
                if x_button_rect.collidepoint(mouse_pos):
                    if player_piece != 'X': sound_manager.play_button_click()
                    player_piece = 'X'
                elif o_button_rect.collidepoint(mouse_pos):
                    if player_piece != 'O': sound_manager.play_button_click()
                    player_piece = 'O'
                elif radio_player_first_rect.collidepoint(mouse_pos):
                    if first_turn != 'player': sound_manager.play_button_click()
                    first_turn = 'player'
                elif radio_ai_first_rect.collidepoint(mouse_pos):
                    if first_turn != 'ai': sound_manager.play_button_click()
                    first_turn = 'ai'
                elif start_button.collidepoint(mouse_pos) and is_start_enabled:
                    sound_manager.play_button_click()
                    pygame.time.wait(100)
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return player_name.strip(), player_piece, first_turn
                elif back_button.collidepoint(mouse_pos):
                    sound_manager.play_button_click()
                    pygame.time.wait(100)
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return None
            if event.type == pygame.KEYDOWN:
                if active_box:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_RETURN: # Nhấn Enter cũng tắt ô nhập liệu
                        active_box = False
                    else:
                        player_name += event.unicode


        # --- Vẽ các thành phần ---
        screen.fill(BG_COLOR)
        screen.blit(background_img, (0, 0))

        # Thay đổi con trỏ chuột khi di chuột qua các nút
        if (is_start_enabled and start_button.collidepoint(mouse_pos)) or \
           back_button.collidepoint(mouse_pos) or \
           x_button_rect.collidepoint(mouse_pos) or \
           o_button_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif player_name_input_box.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM) # Con trỏ văn bản
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Vẽ ô nhập tên người chơi
        player_name_label_surf = font_label.render("Nhập tên của bạn:", True, TEXT_COLOR)
        screen.blit(player_name_label_surf, player_name_label_surf.get_rect(center=(screen_width / 2, player_name_input_box.y - 30)))
        pygame.draw.rect(screen, INPUT_BOX_COLOR_ACTIVE if active_box else INPUT_BOX_COLOR_INACTIVE, player_name_input_box, 2)
        screen.blit(font_input.render(player_name, True, TEXT_COLOR), (player_name_input_box.x + 10, player_name_input_box.y + 10))

        # Vẽ phần chọn quân cờ
        piece_label_surf = font_label.render("Chọn quân cờ của bạn:", True, TEXT_COLOR)
        screen.blit(piece_label_surf, piece_label_surf.get_rect(center=(screen_width / 2, 200)))
        # Nút X
        x_bg_color = VS_AI_COLOR if player_piece == 'X' else (PIECE_BG_HOVER_COLOR if x_button_rect.collidepoint(mouse_pos) else PIECE_BG_COLOR)
        pygame.draw.rect(screen, x_bg_color, x_button_rect, border_radius=15)
        screen.blit(x_img, x_img.get_rect(center=x_button_rect.center))
        # Nút O
        o_bg_color = VS_AI_COLOR if player_piece == 'O' else (PIECE_BG_HOVER_COLOR if o_button_rect.collidepoint(mouse_pos) else PIECE_BG_COLOR)
        pygame.draw.rect(screen, o_bg_color, o_button_rect, border_radius=15)
        screen.blit(o_img, o_img.get_rect(center=o_button_rect.center))

        # Vẽ phần chọn lượt đi
        turn_label_surf = font_label.render("Chọn người đi trước:", True, TEXT_COLOR)
        screen.blit(turn_label_surf, turn_label_surf.get_rect(center=(screen_width / 2, 420)))
        # Nút radio
        radio_y = radio_player_first_rect.centery # Both buttons share the same Y center
        radio_x_player = radio_player_first_rect.x + radio_button_radius
        radio_x_ai = radio_ai_first_rect.x + radio_button_radius
        text_x_offset = radio_button_radius + 10
        # Lựa chọn "Bạn đi trước"
        pygame.draw.circle(screen, TEXT_COLOR, (radio_x_player, radio_y), radio_button_radius, 2)
        if first_turn == 'player':
            pygame.draw.circle(screen, VS_AI_COLOR, (radio_x_player, radio_y), radio_button_radius - 4)
        player_text = font_mode.render("Bạn đi trước", True, TEXT_COLOR)
        screen.blit(player_text, (radio_x_player + text_x_offset, radio_y - player_text.get_height() / 2))
        # Lựa chọn "Máy đi trước"
        pygame.draw.circle(screen, TEXT_COLOR, (radio_x_ai, radio_y), radio_button_radius, 2)
        if first_turn == 'ai':
            pygame.draw.circle(screen, VS_AI_COLOR, (radio_x_ai, radio_y), radio_button_radius - 4)
        ai_text = font_mode.render("Máy đi trước", True, TEXT_COLOR)
        screen.blit(ai_text, (radio_x_ai + text_x_offset, radio_y - ai_text.get_height() / 2))

        # Vẽ nút Bắt đầu và Quay lại
        start_btn_color = (START_BUTTON_HOVER_COLOR if start_button.collidepoint(mouse_pos) else START_BUTTON_COLOR) if is_start_enabled else START_BUTTON_DISABLED_COLOR
        pygame.draw.rect(screen, start_btn_color, start_button, border_radius=10)
        start_text = font_button.render("Bắt đầu", True, BUTTON_TEXT_COLOR)
        screen.blit(start_text, start_text.get_rect(center=start_button.center))

        back_btn_color = BACK_BUTTON_HOVER_COLOR if back_button.collidepoint(mouse_pos) else BACK_BUTTON_COLOR
        pygame.draw.rect(screen, back_btn_color, back_button, border_radius=10)
        back_text = font_button.render("Quay lại", True, BUTTON_TEXT_COLOR)
        screen.blit(back_text, back_text.get_rect(center=back_button.center))

        pygame.display.flip()
