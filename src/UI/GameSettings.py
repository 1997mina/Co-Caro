import pygame
import sys

from components.Button import Button
from components.CheckBox import CheckBox
from manager.SoundManager import SoundManager
from manager.SettingsManager import SettingsManager
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
GREEN = (40, 167, 69)
GREEN_HOVER = (45, 180, 75)
GREEN_PRESSED = (35, 150, 60)

DEFAULT_WIDTH = 1000
DEFAULT_HEIGHT = 800

def _load_and_scale_background(screen_width, screen_height):
    """
    Tải và co dãn hình nền cho màn hình cài đặt.
    """
    background_img = pygame.image.load(resource_path('img/general/Background.jpg')).convert()
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

    # Thiết lập độ mờ cho ảnh nền
    background_img.set_alpha(50)
    return background_img

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
    original_fullscreen = settings_manager.get('fullscreen')
    original_board_size = settings_manager.get('board_size')
    original_music_volume = settings_manager.get('music_volume')

    # Tạo các biến tạm để lưu trạng thái cài đặt chưa được lưu
    # Điều này cho phép người dùng hủy thay đổi bằng cách nhấn "Quay lại"
    temp_fullscreen = original_fullscreen
    temp_board_size = original_board_size

    # Khởi tạo SoundManager MỘT LẦN để quản lý tài nguyên hiệu quả
    sound_manager = SoundManager()

    # Checkbox toàn màn hình
    checkbox_size = 50
    check_image_path = resource_path('img/settings/Check.png')

    fullscreen_checkbox = CheckBox(0, 0, checkbox_size, checkbox_size, # Kích thước hình vuông
                                   "Toàn màn hình", TEXT_COLOR, 36, sound_manager,
                                   initial_state=temp_fullscreen,
                                   check_image_path=check_image_path, text_spacing=30)
    fullscreen_checkbox.set_center_component(screen_width // 2, screen_height // 2 - 100)

    # Slider cho kích thước bàn cờ
    slider_width = 500
    slider_height = 20
    board_size_slider = Slider(0, 0, slider_width, slider_height,
                               10, 30, temp_board_size, sound_manager,
                               "Kích thước bàn cờ: ")
    board_size_slider.set_center_component(screen_width // 2, fullscreen_checkbox.rect.bottom + 100)

    # Slider cho âm lượng nhạc nền
    music_volume_slider = Slider(0, 0, slider_width, slider_height,
                                 0, 100, int(original_music_volume * 100), sound_manager,
                                 "Âm lượng nhạc nền: ", value_suffix="%")
    music_volume_slider.set_center_component(screen_width // 2, board_size_slider.track_rect.bottom + 100)


    button_width = 200
    button_height = 60
    buttons_y = screen_height - button_height - 50
    button_spacing = 100
    
    # Tính toán vị trí để hai nút (Lưu, Quay lại) được căn giữa
    total_buttons_width = button_width * 2 + button_spacing
    start_x = (screen_width - total_buttons_width) / 2

    font_button = pygame.font.SysFont("Times New Roman", 40, bold=True)

    back_button = Button(
        start_x, buttons_y, button_width, button_height,
        font_button.render("Quay lại", True, WHITE), sound_manager,
        color=BACK_COLOR, hover_color=BACK_HOVER_COLOR, pressed_color=BACK_PRESSED_COLOR,
        border_radius=10
    )

    save_button = Button(
        start_x + button_width + button_spacing, buttons_y, button_width, button_height,
        font_button.render("Lưu", True, WHITE), sound_manager,
        color=GREEN, hover_color=GREEN_HOVER, pressed_color=GREEN_PRESSED,
        border_radius=10, disabled_color=(150, 150, 150)
    )

    running = True
    # Biến để hiển thị thông báo "Đã lưu"
    show_saved_message = False
    saved_message_timer = 0

    while running:
        # Kiểm tra xem cài đặt có thay đổi so với bản gốc không
        # để quyết định có bật nút "Lưu" hay không.
        settings_changed = (temp_fullscreen != original_fullscreen or
                            temp_board_size != original_board_size)
        # Âm lượng nhạc được xử lý trực tiếp và lưu ngay, không cần nút "Lưu"
        # nên ta không cần kiểm tra nó ở đây.

        # Vô hiệu hóa nút Lưu nếu không có gì thay đổi hoặc ngay sau khi lưu
        save_button.is_enabled = settings_changed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Xử lý sự kiện cho checkbox
            if fullscreen_checkbox.handle_event(event):
                # Cập nhật trạng thái tạm thời, không lưu ngay
                temp_fullscreen = fullscreen_checkbox.is_checked()
                if temp_fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))

                # Cập nhật lại kích thước màn hình sau khi thay đổi chế độ
                screen_width, screen_height = screen.get_size()

                # Tải lại và co dãn hình nền cho kích thước mới (nếu cần)
                background_img = _load_and_scale_background(screen_width, screen_height)

                # Cập nhật vị trí các phần tử UI để căn giữa lại
                fullscreen_checkbox.set_center_component(screen_width // 2, screen_height // 2 - 100)
                # Cập nhật vị trí các slider
                # Cần tính toán lại vị trí của slider âm lượng dựa trên vị trí của slider kích thước bàn cờ
                # và vị trí của slider kích thước bàn cờ dựa trên checkbox toàn màn hình.
                # Điều này đảm bảo chúng luôn ở đúng vị trí tương đối.
                board_size_slider.set_center_component(screen_width // 2, fullscreen_checkbox.rect.bottom + 100)
                music_volume_slider.set_center_component(screen_width // 2, board_size_slider.rect.bottom + 50)
                board_size_slider.set_center_component(screen_width // 2, fullscreen_checkbox.rect.bottom + 100)
                
                # Căn giữa lại nhóm nút
                total_buttons_width = button_width * 2 + button_spacing
                start_x = (screen_width - total_buttons_width) / 2
                back_button.rect.x = start_x
                back_button.rect.y = screen_height - button_height - 50
                save_button.rect.x = start_x + button_width + button_spacing
                save_button.rect.y = screen_height - button_height - 50

            # Xử lý sự kiện cho slider và lưu nếu giá trị thay đổi
            if board_size_slider.handle_event(event):
                # Cập nhật giá trị tạm thời
                temp_board_size = board_size_slider.get_value()

            # Xử lý sự kiện cho slider âm lượng
            if music_volume_slider.handle_event(event):
                # Lấy giá trị từ slider (0-100) và chuyển thành (0.0-1.0)
                new_volume = music_volume_slider.get_value() / 100.0
                # Gọi phương thức mới của SoundManager để thay đổi âm lượng và lưu cài đặt
                sound_manager.set_music_volume(new_volume)

            # Xử lý sự kiện cho nút Lưu
            if save_button.handle_event(event):
                settings_manager.set('fullscreen', temp_fullscreen) # Lưu trạng thái toàn màn hình
                settings_manager.set('board_size', temp_board_size)
                # Âm lượng đã được lưu trực tiếp, không cần lưu ở đây.
                # Cập nhật trạng thái gốc sau khi lưu, để nút "Lưu" bị vô hiệu hóa
                original_fullscreen = temp_fullscreen
                original_board_size = temp_board_size

                # Hiển thị thông báo "Đã lưu!" trong 2 giây
                show_saved_message = True
                saved_message_timer = pygame.time.get_ticks()

            # Xử lý sự kiện cho nút quay lại
            if back_button.handle_event(event):
                running = False

        # Cập nhật con trỏ chuột
        cursor_manager = CursorManager() # Reset mỗi frame
        cursor_manager.add_clickable_area(fullscreen_checkbox.get_clickable_area(), True)
        cursor_manager.add_clickable_area(save_button.rect, save_button.is_enabled)
        cursor_manager.add_clickable_area(back_button.rect, back_button.is_enabled)
        music_volume_slider.add_to_cursor_manager(cursor_manager)
        board_size_slider.add_to_cursor_manager(cursor_manager) # Thêm slider vào cursor manager
        cursor_manager.update(pygame.mouse.get_pos())

        # Vẽ các thành phần lên màn hình
        screen.fill(BG_COLOR)

        # Vẽ hình nền
        screen.blit(background_img, (0, 0))

        # Vẽ tiêu đề
        font = pygame.font.SysFont("Times New Roman", 48, bold=True)
        title_text = font.render("Cài đặt", True, TITLE_COLOR)
        title_rect = title_text.get_rect(center=(screen_width // 2, 60))
        screen.blit(title_text, title_rect)

        # Vẽ checkbox
        fullscreen_checkbox.draw(screen)

        # Vẽ slider
        board_size_slider.draw(screen)

        # Vẽ slider âm lượng nhạc nền
        music_volume_slider.draw(screen)

        # Vẽ nút Lưu
        save_button.draw(screen)

        # Vẽ nút quay lại
        back_button.draw(screen)

        # Hiển thị thông báo "Đã lưu!"
        if show_saved_message:
            current_time = pygame.time.get_ticks()
            if current_time - saved_message_timer < 2000: # Hiển thị trong 2000ms (2 giây)
                font_saved = pygame.font.SysFont("Times New Roman", 28, italic=True)
                saved_text = font_saved.render("Đã lưu cài đặt!", True, GREEN)
                saved_rect = saved_text.get_rect(center=(screen_width // 2, save_button.rect.top - 30))
                screen.blit(saved_text, saved_rect)
            else:
                show_saved_message = False

        pygame.display.flip()