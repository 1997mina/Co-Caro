import pygame
import os

from Handler.PieceDragHandler import PieceDragHandler

# Hằng số cho màu sắc và font chữ
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (40, 40, 40)
INPUT_BOX_COLOR_INACTIVE = (200, 200, 200)
INPUT_BOX_COLOR_ACTIVE = (100, 100, 100)
BUTTON_COLOR = (0, 150, 136)
DRAG_COLOR = (150, 150, 150)
DRAG_HIGHLIGHT_COLOR = (100, 100, 100) # Màu highlight khi kéo vào ô thả
BUTTON_TEXT_COLOR = (255, 255, 255)
MODE_BUTTON_COLOR_INACTIVE = (220, 220, 220)
MODE_BUTTON_COLOR_ACTIVE = (0, 150, 136)

def get_player_names(screen):
    """
    Hiển thị màn hình để người dùng nhập tên và trả về tên của họ.
    """
    screen_width, screen_height = screen.get_size()
    font_title = pygame.font.SysFont("Times New Roman", 60, bold=True)
    font_label = pygame.font.SysFont("Times New Roman", 36)
    font_input = pygame.font.SysFont("Times New Roman", 32)
    font_button = pygame.font.SysFont("Times New Roman", 40, bold=True)
    font_mode = pygame.font.SysFont("Times New Roman", 28)

    # Tải hình nền
    background_img = pygame.image.load(os.path.join('img', 'Background.jpg')).convert()
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

    # Thiết lập độ mờ cho ảnh nền
    background_img.set_alpha(50)

    # Tải và thay đổi kích thước hình ảnh X và O
    img_size = 50
    x_img_raw = pygame.image.load('img/X.png').convert_alpha()
    o_img_raw = pygame.image.load('img/O.png').convert_alpha()
    x_img = pygame.transform.scale(x_img_raw, (img_size, img_size))
    o_img = pygame.transform.scale(o_img_raw, (img_size, img_size))

    # Các ô nhập liệu và nhãn
    input_box_width = 500
    input_box1 = pygame.Rect((screen_width - input_box_width) / 2, 80, input_box_width, 50)
    input_box2 = pygame.Rect((screen_width - input_box_width) / 2, 150, input_box_width, 50)
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

    # Các chế độ chơi
    modes = {
        "turn_based": {"name": "20 giây mỗi lượt", "time_limit": 20},
        "total_time": {"name": "2 phút tổng cộng", "time_limit": 120}
    }
    selected_mode = "turn_based" # Chế độ mặc định

    # --- Các nút chọn chế độ (Radio button) ---
    radio_button_y_start = 550
    radio_button_spacing = 40
    radio_button_radius = 15
    # Khu vực có thể click cho radio button (bao gồm cả nút tròn và chữ)
    radio_turn_based_rect = pygame.Rect(screen_width / 2 - 150, radio_button_y_start - radio_button_radius, 300, radio_button_radius * 2)
    radio_total_time_rect = pygame.Rect(screen_width / 2 - 150, radio_button_y_start + radio_button_spacing - radio_button_radius, 300, radio_button_radius * 2)

    # Nút Bắt đầu
    button_width = 200
    button_height = 60
    start_button = pygame.Rect(screen_width / 2 + 50, 700, button_width, button_height)

    # Nút Quay lại
    back_button = pygame.Rect(screen_width / 2 - 50 - button_width, 700, button_width, button_height)
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None # Trả về None để báo hiệu người dùng muốn thoát

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active_box = 1
                elif input_box2.collidepoint(event.pos):
                    active_box = 2
                elif radio_turn_based_rect.collidepoint(event.pos):
                    selected_mode = "turn_based"
                elif radio_total_time_rect.collidepoint(event.pos):
                    selected_mode = "total_time"
                elif start_button.collidepoint(event.pos):
                    # Chỉ bắt đầu khi cả hai người chơi đã nhập tên và đã chọn quân cờ
                    if player1_name.strip() and player2_name.strip() and drag_handler.player1_piece and drag_handler.player2_piece:
                        # Trả về tên và thời gian giới hạn dựa trên chế độ đã chọn
                        if drag_handler.player1_piece == 'X':
                            return player1_name.strip(), player2_name.strip(), selected_mode, modes[selected_mode]["time_limit"]
                        elif drag_handler.player1_piece == 'O':
                            return player2_name.strip(), player1_name.strip(), selected_mode, modes[selected_mode]["time_limit"]

                elif back_button.collidepoint(event.pos):
                    return None # Quay lại menu chính
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
        # Lấp đầy màn hình bằng một màu nền đặc trước khi vẽ ảnh nền trong suốt
        screen.fill(BG_COLOR)
        screen.blit(background_img, (0, 0))

        # Nhập tên người chơi 1
        label1_surf = font_label.render("Người chơi 1:", True, TEXT_COLOR) # Đặt nhãn bên trái ô nhập liệu
        screen.blit(label1_surf, (input_box1.x - label1_surf.get_width() - 20, input_box1.y + (input_box1.height - label1_surf.get_height()) / 2))
        pygame.draw.rect(screen, INPUT_BOX_COLOR_ACTIVE if active_box == 1 else INPUT_BOX_COLOR_INACTIVE, input_box1, 2)
        screen.blit(font_input.render(player1_name, True, TEXT_COLOR), (input_box1.x + 10, input_box1.y + 10))

        # Nhập tên người chơi 2
        label2_surf = font_label.render("Người chơi 2:", True, TEXT_COLOR) # Đặt nhãn bên trái ô nhập liệu
        screen.blit(label2_surf, (input_box2.x - label2_surf.get_width() - 20, input_box2.y + (input_box2.height - label2_surf.get_height()) / 2))
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

        # Vẽ lựa chọn chế độ chơi
        mode_label_surf = font_label.render("Chọn chế độ thời gian:", True, TEXT_COLOR)
        screen.blit(mode_label_surf, mode_label_surf.get_rect(center=(screen_width / 2, 500)))

        # --- Vẽ Radio Buttons ---
        radio_y1 = radio_turn_based_rect.centery
        radio_y2 = radio_total_time_rect.centery
        # Căn chỉnh vị trí X của vòng tròn và văn bản
        radio_x = radio_turn_based_rect.x + radio_button_radius
        text_x_offset = radio_button_radius + 10

        # Lựa chọn 1: "30 giây mỗi lượt"
        pygame.draw.circle(screen, TEXT_COLOR, (radio_x, radio_y1), radio_button_radius, 2)
        if selected_mode == "turn_based":
            pygame.draw.circle(screen, MODE_BUTTON_COLOR_ACTIVE, (radio_x, radio_y1), radio_button_radius - 4)
        turn_based_text_surf = font_mode.render(modes["turn_based"]["name"], True, TEXT_COLOR)
        screen.blit(turn_based_text_surf, (radio_x + text_x_offset, radio_y1 - turn_based_text_surf.get_height() / 2))

        # Lựa chọn 2: "3 phút tổng cộng"
        pygame.draw.circle(screen, TEXT_COLOR, (radio_x, radio_y2), radio_button_radius, 2)
        if selected_mode == "total_time":
            pygame.draw.circle(screen, MODE_BUTTON_COLOR_ACTIVE, (radio_x, radio_y2), radio_button_radius - 4)
        total_time_text_surf = font_mode.render(modes["total_time"]["name"], True, TEXT_COLOR)
        screen.blit(total_time_text_surf, (radio_x + text_x_offset, radio_y2 - total_time_text_surf.get_height() / 2))

        # Nút Bắt đầu
        pygame.draw.rect(screen, BUTTON_COLOR, start_button, border_radius=10)
        button_text_surf = font_button.render("Bắt đầu", True, BUTTON_TEXT_COLOR)
        screen.blit(button_text_surf, button_text_surf.get_rect(center=start_button.center))

        # Vẽ nút Quay lại
        pygame.draw.rect(screen, BUTTON_COLOR, back_button, border_radius=10)
        back_text_surf = font_button.render("Quay lại", True, BUTTON_TEXT_COLOR)
        screen.blit(back_text_surf, back_text_surf.get_rect(center=back_button.center))

        pygame.display.flip()