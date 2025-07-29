import pygame

# Hằng số cho màu sắc và font chữ
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (40, 40, 40)
INPUT_BOX_COLOR_INACTIVE = (200, 200, 200)
INPUT_BOX_COLOR_ACTIVE = (100, 100, 100)
BUTTON_COLOR = (0, 150, 136)
BUTTON_TEXT_COLOR = (255, 255, 255)

def get_player_names(screen):
    """
    Hiển thị màn hình để người dùng nhập tên và trả về tên của họ.
    """
    screen_width, screen_height = screen.get_size()
    font_title = pygame.font.SysFont("Times New Roman", 60, bold=True)
    font_label = pygame.font.SysFont("Times New Roman", 36)
    font_input = pygame.font.SysFont("Times New Roman", 32)
    font_button = pygame.font.SysFont("Times New Roman", 40, bold=True)

    # Các ô nhập liệu và nhãn
    input_box1 = pygame.Rect(screen_width / 2 - 150, 200, 300, 50)
    input_box2 = pygame.Rect(screen_width / 2 - 150, 350, 300, 50)
    player1_name = ""
    player2_name = ""
    active_box = None  # Có thể là 1 hoặc 2, hoặc None

    # Nút Bắt đầu
    start_button = pygame.Rect(screen_width / 2 - 100, 450, 200, 60)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Thoát hoàn toàn nếu cửa sổ bị đóng ở màn hình này

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active_box = 1
                elif input_box2.collidepoint(event.pos):
                    active_box = 2
                elif start_button.collidepoint(event.pos):
                    # Chỉ bắt đầu khi cả hai người chơi đã nhập tên
                    if player1_name.strip() and player2_name.strip():
                        running = False
                else:
                    active_box = None

            if event.type == pygame.KEYDOWN:
                if active_box == 1:
                    if event.key == pygame.K_BACKSPACE:
                        player1_name = player1_name[:-1]
                    else:
                        player1_name += event.unicode
                elif active_box == 2:
                    if event.key == pygame.K_BACKSPACE:
                        player2_name = player2_name[:-1]
                    else:
                        player2_name += event.unicode

        # --- Vẽ lên màn hình ---
        screen.fill(BG_COLOR)

        # Tiêu đề
        title_surf = font_title.render("Cờ Caro", True, TEXT_COLOR)
        screen.blit(title_surf, title_surf.get_rect(center=(screen_width / 2, 80)))

        # Nhập tên người chơi 1
        label1_surf = font_label.render("Người chơi 1 (X):", True, TEXT_COLOR)
        screen.blit(label1_surf, label1_surf.get_rect(center=(screen_width / 2, 160)))
        pygame.draw.rect(screen, INPUT_BOX_COLOR_ACTIVE if active_box == 1 else INPUT_BOX_COLOR_INACTIVE, input_box1, 2)
        screen.blit(font_input.render(player1_name, True, TEXT_COLOR), (input_box1.x + 10, input_box1.y + 10))

        # Nhập tên người chơi 2
        label2_surf = font_label.render("Người chơi 2 (O):", True, TEXT_COLOR)
        screen.blit(label2_surf, label2_surf.get_rect(center=(screen_width / 2, 310)))
        pygame.draw.rect(screen, INPUT_BOX_COLOR_ACTIVE if active_box == 2 else INPUT_BOX_COLOR_INACTIVE, input_box2, 2)
        screen.blit(font_input.render(player2_name, True, TEXT_COLOR), (input_box2.x + 10, input_box2.y + 10))

        # Nút Bắt đầu
        pygame.draw.rect(screen, BUTTON_COLOR, start_button)
        button_text_surf = font_button.render("Bắt đầu", True, BUTTON_TEXT_COLOR)
        screen.blit(button_text_surf, button_text_surf.get_rect(center=start_button.center))

        pygame.display.flip()

    return player1_name.strip(), player2_name.strip()