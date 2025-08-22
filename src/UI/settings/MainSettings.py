import pygame
import sys

from components.Button import Button
from manager.SoundManager import SoundManager
from manager.SettingsManager import SettingsManager
from components.Dropdown import Dropdown
from components.Slider import Slider
from manager.CursorManager import CursorManager
from utils.ResourcePath import resource_path

# Hằng số
WHITE = (255, 255, 255)
BG_COLOR = (240, 240, 240)
TITLE_COLOR = (40, 40, 40)
TEXT_COLOR = (30, 30, 30) 

# Màu nút Quay lại
BACK_COLOR = (100, 100, 100) # Xám đậm
BACK_HOVER_COLOR = (130, 130, 130)
BACK_PRESSED_COLOR = (80, 80, 80)

# Màu nút Lưu
GREEN = (60, 180, 80) # Màu xanh lá cây nhạt hơn
GREEN_HOVER = (70, 190, 90) # Nhạt hơn khi hover
GREEN_PRESSED = (50, 160, 70) # Hơi đậm hơn khi nhấn

MEDIUM_GRAY = (150, 150, 150)
LIGHT_GRAY = (180, 180, 180)
SUPER_LIGHT_GRAY = (200, 200, 200)

def _load_and_scale_background(screen_width, screen_height):
    """
    Tải và co dãn hình nền cho màn hình cài đặt.
    """
    background_img = pygame.image.load(resource_path('img/general/Background.jpg')).convert()
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

    # Thiết lập độ mờ cho ảnh nền
    background_img.set_alpha(50)
    return background_img

def _create_composite_icon(style_key, target_size):
    """
    Tạo một icon ghép từ 2 ảnh (X và O) cho một style.
    Nếu không tìm thấy file ảnh, sẽ hiển thị số thứ tự của style.
    """
    font_fallback = pygame.font.SysFont("Times New Roman", 50, bold=True)
    composite_surface = pygame.Surface(target_size, pygame.SRCALPHA)
    try:
        img_x = pygame.image.load(resource_path(f'img/pieces/{style_key}/X.png')).convert_alpha()
        img_o = pygame.image.load(resource_path(f'img/pieces/{style_key}/O.png')).convert_alpha()

        # Tính toán kích thước và vị trí để đặt 2 ảnh vào trong target_size
        piece_h = int(target_size[1] * 0.8) # Cao 80% so với chiều cao của vùng target
        piece_w = piece_h # Giả sử quân cờ vuông

        img_x_scaled = pygame.transform.smoothscale(img_x, (piece_w, piece_h))
        img_o_scaled = pygame.transform.smoothscale(img_o, (piece_w, piece_h))

        gap = 10 # Khoảng cách giữa 2 quân cờ
        total_icon_width = piece_w * 2 + gap
        start_x = (target_size[0] - total_icon_width) // 2            
        y_pos = (target_size[1] - piece_h) // 2

        composite_surface.blit(img_x_scaled, (start_x, y_pos))
        composite_surface.blit(img_o_scaled, (start_x + piece_w + gap, y_pos))
    except pygame.error:
        print(f"Cảnh báo: Không tìm thấy ảnh cho quân cờ '{style_key}'. Sử dụng text thay thế.")
        fallback_text = style_key.replace("style", "")
        text_surf = font_fallback.render(fallback_text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(target_size[0] / 2, target_size[1] / 2))
        composite_surface.blit(text_surf, text_rect)
        
    return composite_surface

def show_settings_screen(screen):
    """
    Hiển thị màn hình cài đặt.
    Hàm này sẽ chạy một vòng lặp riêng và thoát khi người dùng bấm "Quay lại".    
    """
    screen_width, screen_height = screen.get_size()

    # Tải hình nền
    background_img = _load_and_scale_background(screen_width, screen_height)

    # Khởi tạo SettingsManager để đọc/ghi cài đặt
    settings_manager = SettingsManager()

    # Lưu lại cài đặt gốc để so sánh, cho phép vô hiệu hóa nút "Lưu"
    original_board_size = settings_manager.get('board_size')
    original_music_volume = settings_manager.get('music_volume')
    original_sfx_volume = settings_manager.get('sfx_volume')
    # Lấy cài đặt hình dạng quân cờ, mặc định là 'style1' nếu chưa có
    original_piece_shape = settings_manager.get('piece_shape', 'style1')

    # Tạo các biến tạm để lưu trạng thái cài đặt chưa được lưu
    # Điều này cho phép người dùng hủy thay đổi bằng cách nhấn "Quay lại"
    temp_board_size = original_board_size
    temp_piece_shape = original_piece_shape

    # Khởi tạo các trình quản lý
    sound_manager = SoundManager()

    # Dropdown cho kích thước bàn cờ
    dropdown_width = 300
    dropdown_height = 50
    board_size_options = [f"{i}x{i}" for i in range(10, 31)]
    initial_board_size_option = f"{temp_board_size}x{temp_board_size}"
    board_size_dropdown = Dropdown(0, 0, dropdown_width, dropdown_height,
                                   board_size_options, initial_board_size_option, sound_manager,
                                   "Kích thước bàn cờ:", option_hover_color=GREEN_HOVER) # Thêm độ trong suốt
    board_size_dropdown.set_center_component(screen_width // 2, screen_height // 4 - 50)

    # Slider cho âm lượng nhạc nền
    slider_width = 500
    slider_height = 20
    music_volume_slider = Slider(0, 0, slider_width, slider_height,
                                 0, 100, int(original_music_volume * 100), sound_manager,
                                 "Âm lượng nhạc nền: ", value_suffix="%",
                                 knob_color=GREEN, knob_hover_color=GREEN_HOVER,
                                 track_color=MEDIUM_GRAY, track_fill_color=GREEN)
    music_volume_slider.set_center_component(screen_width // 2, board_size_dropdown.rect.bottom + 110)

    # Slider cho âm lượng hiệu ứng âm thanh
    sfx_volume_slider = Slider(0, 0, slider_width, slider_height,
                               0, 100, int(original_sfx_volume * 100), sound_manager,
                               "Âm lượng hiệu ứng: ", value_suffix="%",
                               knob_color=GREEN, knob_hover_color=GREEN_HOVER,
                               track_color=MEDIUM_GRAY, track_fill_color=GREEN)
    sfx_volume_slider.set_center_component(screen_width // 2, music_volume_slider.track_rect.bottom + 80)

    # --- Lựa chọn hình dạng quân cờ ---
    font_label = pygame.font.SysFont("Times New Roman", 35)
    piece_shape_title_surf = font_label.render("Chọn hình dạng quân cờ:", True, TEXT_COLOR)
    piece_shape_title_rect = piece_shape_title_surf.get_rect(center=(screen_width // 2, sfx_volume_slider.track_rect.bottom + 80))

    # Các nút chọn - kích thước mới để chứa 2 quân cờ
    piece_button_width = 180
    piece_button_height = 90
    piece_buttons_y = piece_shape_title_rect.bottom + 20
    piece_button_spacing = 40
    total_piece_buttons_width = (piece_button_width * 3) + (piece_button_spacing * 2)
    piece_start_x = (screen_width - total_piece_buttons_width) / 2

    font_button = pygame.font.SysFont("Times New Roman", 40, bold=True)

    # Tạo các icon ghép cho từng nút
    icon_target_size = (piece_button_width - 30, piece_button_height - 30)
    style1_icon = _create_composite_icon('style1', icon_target_size)
    style2_icon = _create_composite_icon('style2', icon_target_size)
    style3_icon = _create_composite_icon('style3', icon_target_size)

    piece_shape_buttons = {
        'style1': Button(piece_start_x, piece_buttons_y, piece_button_width, 
                         piece_button_height, style1_icon, sound_manager, 
                         color=LIGHT_GRAY, pressed_color=GREEN_PRESSED, 
                         hover_color=SUPER_LIGHT_GRAY, selected_color=GREEN, 
                         border_radius=10, shadow_offset=(6, 6)),
        'style2': Button(piece_start_x + piece_button_width + piece_button_spacing, 
                         piece_buttons_y, piece_button_width, piece_button_height, 
                         style2_icon, sound_manager, color=LIGHT_GRAY, pressed_color=GREEN_PRESSED, 
                         hover_color=SUPER_LIGHT_GRAY, selected_color=GREEN, 
                         border_radius=10, shadow_offset=(6, 6)),
        'style3': Button(piece_start_x + (piece_button_width + piece_button_spacing) * 2, 
                         piece_buttons_y, piece_button_width, piece_button_height, 
                         style3_icon, sound_manager, color=LIGHT_GRAY, pressed_color=GREEN_PRESSED, 
                         hover_color=SUPER_LIGHT_GRAY, selected_color=GREEN, 
                         border_radius=10, shadow_offset=(6, 6))
    }

    # Hàm helper để cập nhật trạng thái chọn của các nút
    def _update_piece_button_selection(selected_key):
        for key, button in piece_shape_buttons.items():
            button.is_selected = (key == selected_key)

    # Đặt trạng thái chọn ban đầu
    _update_piece_button_selection(temp_piece_shape)


    button_width = 200
    button_height = 60
    # Điều chỉnh vị trí Y của các nút Lưu/Quay lại
    buttons_y = screen_height - 100

    OK_button = Button(
        screen_width / 2 - button_width / 2, buttons_y, button_width, button_height,
        font_button.render("OK", True, WHITE), sound_manager,
        color=GREEN, hover_color=GREEN_HOVER, pressed_color=GREEN_PRESSED,
        border_radius=10
    )

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Xử lý sự kiện cho dropdown và cập nhật giá trị tạm thời
            changed, handled = board_size_dropdown.handle_event(event)
            if changed:
                selected_str = board_size_dropdown.get_selected_option()
                # Lấy số từ chuỗi "15x15" -> 15
                temp_board_size = int(selected_str.split('x')[0])
            if handled:
                continue

            # Xử lý sự kiện cho slider âm lượng
            if music_volume_slider.handle_event(event):
                # Lấy giá trị từ slider (0-100) và chuyển thành (0.0-1.0)
                new_volume = music_volume_slider.get_value() / 100.0
                # Gọi phương thức mới của SoundManager để thay đổi âm lượng và lưu cài đặt
                sound_manager.set_music_volume(new_volume)
            
            # Xử lý sự kiện cho slider âm lượng hiệu ứng
            if sfx_volume_slider.handle_event(event):
                new_volume = sfx_volume_slider.get_value() / 100.0
                # Gọi phương thức của SoundManager để cập nhật âm lượng SFX ngay lập tức và lưu cài đặt
                sound_manager.set_sfx_volume(new_volume)

            # Xử lý sự kiện cho các nút chọn hình dạng quân cờ
            for shape_key, shape_button in piece_shape_buttons.items():
                if shape_button.handle_event(event):
                    temp_piece_shape = shape_key
                    _update_piece_button_selection(shape_key)

            # Xử lý sự kiện cho nút OK
            if OK_button.handle_event(event):
                # Lưu tất cả các cài đặt khi nhấn OK
                settings_manager.set('board_size', temp_board_size)
                settings_manager.set('piece_shape', temp_piece_shape)
                # Âm lượng đã được lưu trực tiếp, không cần lưu ở đây.
                running = False

        # Cập nhật con trỏ chuột
        cursor_manager = CursorManager() # Reset mỗi frame
        cursor_manager.add_clickable_area(OK_button.rect, OK_button.is_enabled)
        music_volume_slider.add_to_cursor_manager(cursor_manager)
        sfx_volume_slider.add_to_cursor_manager(cursor_manager)
        board_size_dropdown.add_to_cursor_manager(cursor_manager)
        for shape_button in piece_shape_buttons.values():
            cursor_manager.add_clickable_area(shape_button.rect, shape_button.is_enabled)

        cursor_manager.update(pygame.mouse.get_pos())

        # Vẽ các thành phần lên màn hình
        screen.fill(BG_COLOR)

        # Vẽ hình nền
        screen.blit(background_img, (0, 0))

        # Vẽ tiêu đề
        font = pygame.font.SysFont("Times New Roman", 54, bold=True)
        title_text = font.render("Cài đặt", True, TITLE_COLOR)
        title_rect = title_text.get_rect(center=(screen_width // 2, 60))
        screen.blit(title_text, title_rect)

        music_volume_slider.draw(screen)
        sfx_volume_slider.draw(screen)

        # Vẽ khu vực chọn quân cờ
        screen.blit(piece_shape_title_surf, piece_shape_title_rect)
        for shape_button in piece_shape_buttons.values():
            shape_button.draw(screen)
        
        OK_button.draw(screen)

        # Vẽ dropdown cuối cùng để nó hiển thị trên các thành phần khác
        board_size_dropdown.draw(screen)

        pygame.display.flip()