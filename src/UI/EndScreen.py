import pygame

from manager.SoundManager import SoundManager

# Hằng số cho màu sắc và font chữ
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (40, 40, 40)
WINNER_TEXT = (255, 200, 0) # Màu vàng
WINNER_COLOR = (0, 150, 136)  # Màu xanh lá cây
BUTTON_COLOR = (0, 150, 136)
BUTTON_TEXT_COLOR = (255, 255, 255)
QUIT_BUTTON_COLOR = (211, 47, 47)  # Màu đỏ

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
    
    # Định nghĩa các nút, vị trí được căn giữa khu vực bàn cờ
    button_width, button_height = 300, 60
    
    # Nút "Chơi lại"
    play_again_button = pygame.Rect(0, 0, button_width, button_height)
    play_again_button.center = (board_rect.centerx, board_rect.centery)
    
    # Nút "Thoát"
    quit_button = pygame.Rect(0, 0, button_width, button_height)
    quit_button.center = (board_rect.centerx, board_rect.centery + 80)

    sound_manager = SoundManager()

    # Vòng lặp riêng cho màn hình kết thúc
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Coi việc đóng cửa sổ là thoát

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    sound_manager.play_button_click()
                    pygame.time.wait(100)
                    return True  # Chơi lại
                if quit_button.collidepoint(event.pos):
                    sound_manager.play_button_click()
                    pygame.time.wait(100)
                    return False  # Thoát

        # Vẽ lại nền gốc và lớp phủ chỉ trên bàn cờ
        screen.blit(background, (0, 0))
        screen.blit(overlay, board_rect.topleft)

        # Hiển thị thông báo thắng/hòa
        message = "Hòa!" if winner_name == "Draw" else f"{winner_name} thắng!"
        text_surf = font_title.render(message, True, WINNER_TEXT)
        text_rect = text_surf.get_rect(center=(board_rect.centerx, board_rect.centery - 100))
        screen.blit(text_surf, text_rect)

        # Vẽ nút "Chơi lại"
        pygame.draw.rect(screen, BUTTON_COLOR, play_again_button, border_radius=10)
        button_text_surf = font_button.render("Chơi lại", True, BUTTON_TEXT_COLOR)
        screen.blit(button_text_surf, button_text_surf.get_rect(center=play_again_button.center))

        # Vẽ nút "Thoát"
        pygame.draw.rect(screen, QUIT_BUTTON_COLOR, quit_button, border_radius=10)
        quit_text_surf = font_button.render("Thoát", True, BUTTON_TEXT_COLOR)
        screen.blit(quit_text_surf, quit_text_surf.get_rect(center=quit_button.center))

        pygame.display.flip()