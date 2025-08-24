import pygame

from manager.SoundManager import SoundManager
from components.Button import Button
from manager.CursorManager import CursorManager

# Hằng số cho màu sắc và font chữ
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (40, 40, 40)
WINNER_TEXT = (255, 200, 0) # Màu vàng cho chữ "thắng/hòa"
DIALOG_BG_COLOR = (245, 245, 245)
DIALOG_BORDER_COLOR = (150, 150, 150)

# Màu sắc cho nút
BUTTON_TEXT_COLOR = (255, 255, 255)
PLAY_AGAIN_COLOR = (0, 150, 136)
PLAY_AGAIN_HOVER_COLOR = (0, 180, 160)
PLAY_AGAIN_PRESSED_COLOR = (0, 130, 116)
QUIT_COLOR = (211, 47, 47)
QUIT_HOVER_COLOR = (255, 80, 80)
QUIT_PRESSED_COLOR = (190, 30, 30)

def _draw_score_display(screen, container_rect, match_history, x_img, o_img, font_score, y_pos):
    """
    Vẽ hiển thị tỉ số trận đấu (X vs O).
    """
    wins_X = match_history.count('X')
    wins_O = match_history.count('O')
    
    # 1. Tạo surface cho phần text của tỉ số
    score_text_surf = font_score.render(f"{wins_X} - {wins_O}", True, TEXT_COLOR)
    
    # 2. Scale icon cho phù hợp
    icon_size = (50, 50)
    x_icon = pygame.transform.smoothscale(x_img, icon_size)
    o_icon = pygame.transform.smoothscale(o_img, icon_size)
    
    # 3. Tính toán tổng chiều rộng và vị trí để căn giữa
    padding = 15
    total_width = x_icon.get_width() + padding + score_text_surf.get_width() + padding + o_icon.get_width()
    start_x = container_rect.centerx - total_width / 2
    
    # 4. Xác định vị trí Y chung và vẽ các thành phần
    x_icon_rect = x_icon.get_rect(left=start_x, centery=y_pos)
    score_rect = score_text_surf.get_rect(left=x_icon_rect.right + padding, centery=y_pos)
    o_icon_rect = o_icon.get_rect(left=score_rect.right + padding, centery=y_pos)
    screen.blit(x_icon, x_icon_rect)
    screen.blit(score_text_surf, score_rect)
    screen.blit(o_icon, o_icon_rect)

def show_end_screen(screen, winner_name, board_rect, match_history, x_img, o_img):
    """
    Hiển thị màn hình kết thúc game với tên người thắng và các nút lựa chọn.
    Trả về True nếu người dùng muốn chơi lại, False nếu muốn thoát.
    """
    font_title = pygame.font.SysFont("Times New Roman", 74, bold=True)
    font_score = pygame.font.SysFont("Times New Roman", 42, bold=True)
    font_button = pygame.font.SysFont("Times New Roman", 40, bold=True)

    # Tạo một bản sao của màn hình game hiện tại để vẽ lên trên.
    background = screen.copy()

    # Tạo một lớp phủ tối chỉ cho khu vực bàn cờ, tương tự màn hình tạm dừng
    overlay = pygame.Surface(board_rect.size, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Màu đen bán trong suốt
    
    # Khởi tạo các nút bằng lớp Button
    button_width, button_height = 300, 60
    sound_manager = SoundManager()
    
    play_again_button = Button(
        0, 0,
        button_width, button_height,
        font_button.render("Tiếp Tục", True, BUTTON_TEXT_COLOR), sound_manager,
        color=PLAY_AGAIN_COLOR, hover_color=PLAY_AGAIN_HOVER_COLOR, pressed_color=PLAY_AGAIN_PRESSED_COLOR, 
        border_radius=10
    )
    quit_button = Button(
        0, 0,
        button_width, button_height,
        font_button.render("Thoát Game", True, BUTTON_TEXT_COLOR), sound_manager,
        color=QUIT_COLOR, hover_color=QUIT_HOVER_COLOR, pressed_color=QUIT_PRESSED_COLOR,
        border_radius=10
    )

    cursor_manager = CursorManager()
    # Vòng lặp riêng cho màn hình kết thúc
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Coi việc đóng cửa sổ là thoát
            
            if play_again_button.handle_event(event):
                return True # Chơi lại
            if quit_button.handle_event(event):
                return False # Thoát
        
        # Cập nhật con trỏ chuột
        mouse_pos = pygame.mouse.get_pos()
        cursor_manager.reset()
        cursor_manager.add_clickable_area(play_again_button.rect, True)
        cursor_manager.add_clickable_area(quit_button.rect, True)
        cursor_manager.update(mouse_pos)

        # --- Define content and layout ---
        message = "Hòa!" if winner_name == "Draw" else f"{winner_name} thắng!"
        text_surf = font_title.render(message, True, TEXT_COLOR)
        
        # Layout constants
        padding_x = 50
        padding_y = 40
        gap = 25
        score_display_height = 50 # Based on icon size in _draw_score_display

        # Calculate required size for the dialog box
        box_width = play_again_button.rect.width + 2 * padding_x
        box_height = (padding_y + 
                      text_surf.get_height() + gap + 
                      score_display_height + gap + 
                      play_again_button.rect.height + gap + 
                      quit_button.rect.height + 
                      padding_y)

        # Create the dialog box rect, centered on the board
        box_rect = pygame.Rect(0, 0, box_width, box_height)
        box_rect.center = board_rect.center

        # --- Position elements inside the box ---
        y_cursor = box_rect.top + padding_y
        text_rect = text_surf.get_rect(centerx=box_rect.centerx, top=y_cursor)
        y_cursor = text_rect.bottom + gap
        score_y_pos = y_cursor + score_display_height / 2
        y_cursor += score_display_height + gap
        play_again_button.rect.centerx = box_rect.centerx
        play_again_button.rect.top = y_cursor
        play_again_button.shadow_rect = play_again_button.rect.copy().move(play_again_button.shadow_offset)
        y_cursor = play_again_button.rect.bottom + gap
        quit_button.rect.centerx = box_rect.centerx
        quit_button.rect.top = y_cursor
        quit_button.shadow_rect = quit_button.rect.copy().move(quit_button.shadow_offset)

        # --- Draw everything ---
        screen.blit(background, (0, 0))
        screen.blit(overlay, board_rect.topleft)

        # Draw the dialog box
        pygame.draw.rect(screen, DIALOG_BG_COLOR, box_rect, border_radius=15)
        pygame.draw.rect(screen, DIALOG_BORDER_COLOR, box_rect, 3, border_radius=15)

        # Draw the content
        screen.blit(text_surf, text_rect)
        _draw_score_display(screen, box_rect, match_history, x_img, o_img, font_score, score_y_pos)
        play_again_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.flip()

def show_final_victory_screen(screen, final_winner_name, board_rect, match_history, x_img, o_img):
    """
    Hiển thị màn hình chiến thắng chung cuộc.
    """
    font_title = pygame.font.SysFont("Times New Roman", 80, bold=True)
    font_score = pygame.font.SysFont("Times New Roman", 42, bold=True)
    font_subtitle = pygame.font.SysFont("Times New Roman", 40, italic=True)
    font_button = pygame.font.SysFont("Times New Roman", 40, bold=True)

    background = screen.copy()
    overlay = pygame.Surface(board_rect.size, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))  # Lớp phủ tối hơn

    sound_manager = SoundManager()
    
    # Chỉ có một nút để quay về menu
    menu_button = Button(
        0, 0,
        300, 60,
        font_button.render("Về Menu Chính", True, BUTTON_TEXT_COLOR), sound_manager,
        color=PLAY_AGAIN_COLOR, hover_color=PLAY_AGAIN_HOVER_COLOR, pressed_color=PLAY_AGAIN_PRESSED_COLOR, 
        border_radius=10
    )

    cursor_manager = CursorManager()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if menu_button.handle_event(event):
                return # Thoát khỏi hàm

        mouse_pos = pygame.mouse.get_pos()
        cursor_manager.reset()
        cursor_manager.add_clickable_area(menu_button.rect, True)
        cursor_manager.update(mouse_pos)

        # --- Define content and layout ---
        message = f"{final_winner_name}"
        subtitle_message = "Chiến thắng chung cuộc!"
        text_surf = font_title.render(message, True, TEXT_COLOR)
        subtitle_surf = font_subtitle.render(subtitle_message, True, (80, 80, 80))

        # Layout constants
        box_padding_y = 40
        gap = 25
        score_display_height = 50

        # Calculate required size for the dialog box
        box_width = max(text_surf.get_width(), subtitle_surf.get_width(), menu_button.rect.width) + 100
        box_height = (box_padding_y +
                      text_surf.get_height() + gap +
                      subtitle_surf.get_height() + gap +
                      score_display_height + gap +
                      menu_button.rect.height +
                      box_padding_y)
        box_rect = pygame.Rect(0, 0, box_width, box_height)
        box_rect.center = board_rect.center

        # --- Position elements inside the box ---
        y_cursor = box_rect.top + box_padding_y
        text_rect = text_surf.get_rect(centerx=box_rect.centerx, top=y_cursor)
        y_cursor = text_rect.bottom + gap
        subtitle_rect = subtitle_surf.get_rect(centerx=box_rect.centerx, top=y_cursor)
        y_cursor = subtitle_rect.bottom + gap
        score_y_pos = y_cursor + score_display_height / 2
        y_cursor += score_display_height + gap
        menu_button.rect.centerx = box_rect.centerx
        menu_button.rect.top = y_cursor
        menu_button.shadow_rect = menu_button.rect.copy().move(menu_button.shadow_offset)

        # --- Draw everything ---
        screen.blit(background, (0, 0))
        screen.blit(overlay, board_rect.topleft)

        pygame.draw.rect(screen, DIALOG_BG_COLOR, box_rect, border_radius=15)
        pygame.draw.rect(screen, DIALOG_BORDER_COLOR, box_rect, 3, border_radius=15)

        screen.blit(text_surf, text_rect)
        screen.blit(subtitle_surf, subtitle_rect)
        _draw_score_display(screen, box_rect, match_history, x_img, o_img, font_score, score_y_pos)
        menu_button.draw(screen)

        pygame.display.flip()

def show_quit_confirmation_dialog(screen, board_rect):
    """
    Hiển thị hộp thoại xác nhận thoát game.
    Trả về True nếu người dùng xác nhận thoát, False nếu không.
    """
    font_title = pygame.font.SysFont("Times New Roman", 50, bold=True)
    font_button = pygame.font.SysFont("Times New Roman", 40, bold=True)

    background = screen.copy()
    overlay = pygame.Surface(board_rect.size, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))

    sound_manager = SoundManager()
    button_width, button_height = 250, 60
    
    # Khởi tạo các nút bằng lớp Button
    quit_button = Button(
        0, 0,
        button_width, button_height,
        font_button.render("Thoát", True, BUTTON_TEXT_COLOR), sound_manager,
        color=QUIT_COLOR, hover_color=QUIT_HOVER_COLOR, pressed_color=QUIT_PRESSED_COLOR,
        border_radius=10
    )
    stay_button = Button(
        0, 0,
        button_width, button_height,
        font_button.render("Tiếp tục", True, BUTTON_TEXT_COLOR), sound_manager,
        color=(100, 100, 100), hover_color=(130, 130, 130), pressed_color=(80, 80, 80),
        border_radius=10
    )

    cursor_manager = CursorManager()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False # Đóng cửa sổ = hủy bỏ
            
            if quit_button.handle_event(event):
                return True # Xác nhận thoát
            if stay_button.handle_event(event):
                return False # Hủy bỏ

        # Cập nhật con trỏ chuột
        mouse_pos = pygame.mouse.get_pos()
        cursor_manager.reset()
        cursor_manager.add_clickable_area(quit_button.rect, True)
        cursor_manager.add_clickable_area(stay_button.rect, True)
        cursor_manager.update(mouse_pos)

        # --- Define content and layout ---
        message = "Bạn có chắc muốn thoát?"
        text_surf = font_title.render(message, True, TEXT_COLOR)

        # Layout constants
        padding_x = 50
        padding_y = 40
        gap = 20

        # Calculate required size for the dialog box
        box_width = max(text_surf.get_width(), quit_button.rect.width) + 2 * padding_x
        box_height = (padding_y +
                      text_surf.get_height() + gap + 20 + # Extra gap
                      quit_button.rect.height + gap +
                      stay_button.rect.height +
                      padding_y)
        box_rect = pygame.Rect(0, 0, box_width, box_height)
        box_rect.center = board_rect.center

        # --- Position elements inside the box ---
        y_cursor = box_rect.top + padding_y
        text_rect = text_surf.get_rect(centerx=box_rect.centerx, top=y_cursor)
        y_cursor = text_rect.bottom + gap + 20 # Extra gap
        quit_button.rect.centerx = box_rect.centerx
        quit_button.rect.top = y_cursor
        quit_button.shadow_rect = quit_button.rect.copy().move(quit_button.shadow_offset)
        y_cursor = quit_button.rect.bottom + gap
        stay_button.rect.centerx = box_rect.centerx
        stay_button.rect.top = y_cursor
        stay_button.shadow_rect = stay_button.rect.copy().move(stay_button.shadow_offset)

        # --- Draw everything ---
        screen.blit(background, (0, 0))
        screen.blit(overlay, board_rect.topleft)

        pygame.draw.rect(screen, DIALOG_BG_COLOR, box_rect, border_radius=15)
        pygame.draw.rect(screen, DIALOG_BORDER_COLOR, box_rect, 3, border_radius=15)
        screen.blit(text_surf, text_rect)
        quit_button.draw(screen)
        stay_button.draw(screen)

        pygame.display.flip()