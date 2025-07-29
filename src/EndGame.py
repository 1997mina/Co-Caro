import pygame

# Hằng số cho màu sắc và font chữ
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (40, 40, 40)
WINNER_COLOR = (0, 150, 136)  # Màu xanh lá cây
BUTTON_COLOR = (0, 150, 136)
BUTTON_TEXT_COLOR = (255, 255, 255)
QUIT_BUTTON_COLOR = (211, 47, 47)  # Màu đỏ

def show_end_screen(screen, winner_name):
    """
    Hiển thị màn hình kết thúc game với tên người thắng và các nút lựa chọn.
    Trả về True nếu người dùng muốn chơi lại, False nếu muốn thoát.
    """
    screen_width, screen_height = screen.get_size()
    font_title = pygame.font.SysFont("Times New Roman", 74, bold=True)
    font_button = pygame.font.SysFont("Times New Roman", 40, bold=True)

    # --- Tạo hiệu ứng mờ ---
    # 1. Tạo một bản sao của màn hình game hiện tại để làm mờ.
    background = screen.copy()

    # 2. Thu nhỏ bản sao đó xuống kích thước rất nhỏ, sau đó phóng to lại.
    #    Điều này tạo ra hiệu ứng pixelated/blur.
    scale_factor = 8
    small_surf = pygame.transform.smoothscale(
        background,
        (screen_width // scale_factor, screen_height // scale_factor)
    )
    blurred_background = pygame.transform.smoothscale(
        small_surf,
        (screen_width, screen_height)
    )

    # 3. Tạo một lớp phủ tối để làm mờ thêm và tăng độ tương phản cho văn bản
    dim_overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    dim_overlay.fill((0, 0, 0, 128))  # Màu đen bán trong suốt
    
    # Định nghĩa các nút
    play_again_button = pygame.Rect(screen_width / 2 - 150, 350, 300, 60)
    quit_button = pygame.Rect(screen_width / 2 - 150, 430, 300, 60)

    # Vòng lặp riêng cho màn hình kết thúc
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Coi việc đóng cửa sổ là thoát

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    return True  # Chơi lại
                if quit_button.collidepoint(event.pos):
                    return False  # Thoát

        # Vẽ nền đã được làm mờ và lớp phủ tối
        screen.blit(blurred_background, (0, 0))
        screen.blit(dim_overlay, (0, 0))

        # Hiển thị thông báo thắng/hòa
        message = "Hòa!" if winner_name == "Draw" else f"{winner_name} thắng!"
        text_surf = font_title.render(message, True, WINNER_COLOR)
        screen.blit(text_surf, text_surf.get_rect(center=(screen_width / 2, 250)))

        # Vẽ nút "Chơi lại"
        pygame.draw.rect(screen, BUTTON_COLOR, play_again_button, border_radius=10)
        button_text_surf = font_button.render("Chơi lại", True, BUTTON_TEXT_COLOR)
        screen.blit(button_text_surf, button_text_surf.get_rect(center=play_again_button.center))

        # Vẽ nút "Thoát"
        pygame.draw.rect(screen, QUIT_BUTTON_COLOR, quit_button, border_radius=10)
        quit_text_surf = font_button.render("Thoát", True, BUTTON_TEXT_COLOR)
        screen.blit(quit_text_surf, quit_text_surf.get_rect(center=quit_button.center))

        pygame.display.flip()