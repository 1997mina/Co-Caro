import pygame

from BeforeGame.PieceDragHandler import PieceDragHandler

# Hằng số cho màu sắc và font chữ
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (40, 40, 40)
INPUT_BOX_COLOR_INACTIVE = (200, 200, 200)
INPUT_BOX_COLOR_ACTIVE = (100, 100, 100)
BUTTON_COLOR = (0, 150, 136)
DRAG_COLOR = (150, 150, 150)
DRAG_HIGHLIGHT_COLOR = (100, 100, 100)
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

    # Tải và thay đổi kích thước hình ảnh X và O
    img_size = 50
    x_img = pygame.transform.scale(pygame.image.load('img/X.png'), (img_size, img_size))
    o_img = pygame.transform.scale(pygame.image.load('img/O.png'), (img_size, img_size))

    # Các ô nhập liệu và nhãn
    input_box_width = 500
    input_box1 = pygame.Rect((screen_width - input_box_width) / 2, 80, input_box_width, 50)
    input_box2 = pygame.Rect((screen_width - input_box_width) / 2, 200, input_box_width, 50)
    player1_name = ""
    player2_name = ""
    active_box = None  # Có thể là 1 hoặc 2, hoặc None

    # Vị trí ban đầu của X và O để kéo
    x_drag_rect_initial_center = (screen_width / 2 - 100, 400)
    o_drag_rect_initial_center = (screen_width / 2 + 100, 400)

    # Vị trí thả cho người chơi 1 và 2
    drop_target1 = pygame.Rect(input_box1.x + input_box1.width + 20, input_box1.y, img_size, img_size)
    drop_target2 = pygame.Rect(input_box2.x + input_box2.width + 20, input_box2.y, img_size, img_size)

    # Khởi tạo trình xử lý kéo thả quân cờ
    drag_handler = PieceDragHandler(x_img, o_img, x_drag_rect_initial_center, o_drag_rect_initial_center, drop_target1, drop_target2)

    # Nút Bắt đầu
    start_button = pygame.Rect(screen_width / 2 - 100, 480, 200, 60)
    
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active_box = 1
                elif input_box2.collidepoint(event.pos):
                    active_box = 2
                elif start_button.collidepoint(event.pos):
                    # Chỉ bắt đầu khi cả hai người chơi đã nhập tên và đã chọn quân cờ
                    if player1_name.strip() and player2_name.strip() and drag_handler.player1_piece and drag_handler.player2_piece:
                        game_running = False
                else:
                    active_box = None
                
                # Bắt đầu kéo
                drag_handler.handle_mouse_down(event.pos)

            if event.type == pygame.MOUSEMOTION:
                drag_handler.handle_mouse_motion(event.pos)

            if event.type == pygame.MOUSEBUTTONUP:
                drag_handler.handle_mouse_up(event.pos)

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

        # Nhập tên người chơi 1
        label1_surf = font_label.render("Người chơi 1:", True, TEXT_COLOR)
        screen.blit(label1_surf, label1_surf.get_rect(midbottom=input_box1.midtop, y=input_box1.top - 50))
        pygame.draw.rect(screen, INPUT_BOX_COLOR_ACTIVE if active_box == 1 else INPUT_BOX_COLOR_INACTIVE, input_box1, 2)
        screen.blit(font_input.render(player1_name, True, TEXT_COLOR), (input_box1.x + 10, input_box1.y + 10))

        # Nhập tên người chơi 2
        label2_surf = font_label.render("Người chơi 2:", True, TEXT_COLOR)
        screen.blit(label2_surf, label2_surf.get_rect(midbottom=input_box2.midtop, y=input_box2.top - 50))
        pygame.draw.rect(screen, INPUT_BOX_COLOR_ACTIVE if active_box == 2 else INPUT_BOX_COLOR_INACTIVE, input_box2, 2)
        screen.blit(font_input.render(player2_name, True, TEXT_COLOR), (input_box2.x + 10, input_box2.y + 10))

        # Vẽ các ô thả quân cờ
        pygame.draw.rect(screen, DRAG_HIGHLIGHT_COLOR if drop_target1.collidepoint(pygame.mouse.get_pos()) and drag_handler.dragging else DRAG_COLOR, drop_target1, 2)
        pygame.draw.rect(screen, DRAG_HIGHLIGHT_COLOR if drop_target2.collidepoint(pygame.mouse.get_pos()) and drag_handler.dragging else DRAG_COLOR, drop_target2, 2)

        # Hiển thị quân cờ đã chọn
        if drag_handler.player1_piece == 'X':
            screen.blit(x_img, drop_target1.topleft)
        elif drag_handler.player1_piece == 'O':
            screen.blit(o_img, drop_target1.topleft)
        
        if drag_handler.player2_piece == 'X':
            screen.blit(x_img, drop_target2.topleft)
        elif drag_handler.player2_piece == 'O':
            screen.blit(o_img, drop_target2.topleft)

        # Vẽ quân cờ X và O để kéo
        # Chỉ vẽ nếu chưa được chọn hoặc đang được kéo
        if not drag_handler.player1_piece == 'X' and not drag_handler.player2_piece == 'X' or (drag_handler.dragging and drag_handler.dragged_piece == 'X'):
            screen.blit(x_img, drag_handler.x_drag_rect)
        if not drag_handler.player1_piece == 'O' and not drag_handler.player2_piece == 'O' or (drag_handler.dragging and drag_handler.dragged_piece == 'O'):
            screen.blit(o_img, drag_handler.o_drag_rect)

        # Hiển thị hướng dẫn kéo thả
        drag_instruction_surf = font_label.render("Kéo X hoặc O vào ô nhỏ để chọn quân cờ", True, TEXT_COLOR)
        screen.blit(drag_instruction_surf, drag_instruction_surf.get_rect(center=(screen_width / 2, 320)))

        # Nút Bắt đầu
        pygame.draw.rect(screen, BUTTON_COLOR, start_button)
        button_text_surf = font_button.render("Bắt đầu", True, BUTTON_TEXT_COLOR)
        screen.blit(button_text_surf, button_text_surf.get_rect(center=start_button.center))

        pygame.display.flip()
    
    # Trả về tên người chơi và quân cờ đã chọn
    # Đảm bảo player1_name luôn là 'X' và player2_name luôn là 'O'
    # Nếu người chơi 1 chọn O, thì người chơi 2 sẽ là X và ngược lại (đã được xử lý trong PieceDragHandler)
    if drag_handler.player1_piece == 'X':
        return player1_name.strip(), player2_name.strip()
    elif drag_handler.player1_piece == 'O':
        # Hoán đổi tên nếu người chơi 1 chọn O
        return player2_name.strip(), player1_name.strip()
    else:
        # Trường hợp không chọn quân cờ (không nên xảy ra với logic hiện tại)
        return player1_name.strip(), player2_name.strip()