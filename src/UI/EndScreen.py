import pygame

from manager.SoundManager import SoundManager
from ui.components.Button import Button

# Hằng số cho màu sắc và font chữ
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (40, 40, 40)
WINNER_TEXT = (255, 200, 0) # Màu vàng cho chữ "thắng/hòa"

# Màu sắc cho nút
BUTTON_TEXT_COLOR = (255, 255, 255)
PLAY_AGAIN_COLOR = (0, 150, 136)
PLAY_AGAIN_HOVER_COLOR = (0, 180, 160)
PLAY_AGAIN_PRESSED_COLOR = (0, 130, 116)
QUIT_COLOR = (211, 47, 47)
QUIT_HOVER_COLOR = (255, 80, 80)
QUIT_PRESSED_COLOR = (190, 30, 30)

def show_end_screen(screen, winner_name, board_rect):
    """
    Hiển thị màn hình kết thúc game với tên người thắng và các nút lựa chọn.
    Trả về True nếu người dùng muốn chơi lại, False nếu muốn thoát.
    """
    font_title = pygame.font.SysFont("Times New Roman", 74, bold=True)
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
        board_rect.centerx - button_width / 2, board_rect.centery - button_height / 2,
        button_width, button_height,
        font_button.render("Chơi lại", True, BUTTON_TEXT_COLOR), sound_manager,
        color=PLAY_AGAIN_COLOR, hover_color=PLAY_AGAIN_HOVER_COLOR, pressed_color=PLAY_AGAIN_PRESSED_COLOR, 
        border_radius=10
    )
    quit_button = Button(
        board_rect.centerx - button_width / 2, board_rect.centery + 80 - button_height / 2,
        button_width, button_height,
        font_button.render("Thoát", True, BUTTON_TEXT_COLOR), sound_manager,
        color=QUIT_COLOR, hover_color=QUIT_HOVER_COLOR, pressed_color=QUIT_PRESSED_COLOR,
        border_radius=10
    )

    # Vòng lặp riêng cho màn hình kết thúc
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Coi việc đóng cửa sổ là thoát
            
            if play_again_button.handle_event(event):
                return True # Chơi lại
            if quit_button.handle_event(event):
                return False # Thoát

        # Vẽ lại nền gốc và lớp phủ chỉ trên bàn cờ
        screen.blit(background, (0, 0))
        screen.blit(overlay, board_rect.topleft)

        # Hiển thị thông báo thắng/hòa
        message = "Hòa!" if winner_name == "Draw" else f"{winner_name} thắng!"
        text_surf = font_title.render(message, True, WINNER_TEXT)
        text_rect = text_surf.get_rect(center=(board_rect.centerx, board_rect.centery - 100))
        screen.blit(text_surf, text_rect)

        # Vẽ các nút
        play_again_button.draw(screen)
        quit_button.draw(screen)

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
        board_rect.centerx - button_width / 2, board_rect.centery - button_height / 2,
        button_width, button_height,
        font_button.render("Thoát", True, BUTTON_TEXT_COLOR), sound_manager,
        color=QUIT_COLOR, hover_color=QUIT_HOVER_COLOR, pressed_color=QUIT_PRESSED_COLOR,
        border_radius=10
    )
    stay_button = Button(
        board_rect.centerx - button_width / 2, board_rect.centery + 80 - button_height / 2,
        button_width, button_height,
        font_button.render("Ở lại", True, BUTTON_TEXT_COLOR), sound_manager,
        color=(100, 100, 100), hover_color=(130, 130, 130), pressed_color=(80, 80, 80),
        border_radius=10
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False # Đóng cửa sổ = hủy bỏ
            
            if quit_button.handle_event(event):
                return True # Xác nhận thoát
            if stay_button.handle_event(event):
                return False # Hủy bỏ

        screen.blit(background, (0, 0))
        screen.blit(overlay, board_rect.topleft)

        message = "Bạn có chắc muốn thoát?"
        text_surf = font_title.render(message, True, WINNER_TEXT)
        text_rect = text_surf.get_rect(center=(board_rect.centerx, board_rect.centery - 80))
        screen.blit(text_surf, text_rect)

        # Vẽ các nút
        quit_button.draw(screen)
        stay_button.draw(screen)

        pygame.display.flip()