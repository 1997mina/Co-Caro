import pygame

from utils.ResourcePath import resource_path
from manager.SoundManager import SoundManager
from components.Button import Button
from logic.ScoreIndicator import ScoreIndicator

class InfoPanel:
    """
    Lớp cơ sở (cha) cho các bảng thông tin.
    Chứa các thuộc tính và phương thức chung để vẽ thông tin người chơi,
    bộ đếm thời gian, và các nút điều khiển.
    """
    def __init__(self, rect, player_names, x_img, o_img):
        self.rect = rect
        self.player_names = player_names
        
        # Tạo phiên bản ảnh nhỏ hơn cho panel
        icon_size = 50
        self.x_img = pygame.transform.smoothscale(x_img, (icon_size, icon_size))
        self.o_img = pygame.transform.smoothscale(o_img, (icon_size, icon_size))
        
        # Tải và thay đổi kích thước ảnh đại diện người chơi mặc định
        player_icon_size = 90
        self.player_icon_img = pygame.image.load(resource_path('img/ingame/Player.png')).convert_alpha()
        self.player_icon_img = pygame.transform.smoothscale(self.player_icon_img, (player_icon_size, player_icon_size))
        
        # Fonts
        self.font_name = pygame.font.SysFont("Times New Roman", 32, bold=True)
        self.font_total_time_label = pygame.font.SysFont("Times New Roman", 24)
        self.font_score_title = pygame.font.SysFont("Times New Roman", 22, bold=True)
        self.font_turn = pygame.font.SysFont("Times New Roman", 24, italic=True)
        self.font_timer = pygame.font.SysFont("Arial", 42, bold=True)
        self.font_button = pygame.font.SysFont("Times New Roman", 24, bold=True)
        
        # Colors
        self.bg_color = (240, 240, 240)
        self.text_color = (30, 30, 30)
        self.divider_color = (200, 200, 200)
        self.timer_color = (60, 60, 60)
        self.timer_warning_color = (211, 47, 47) # Màu đỏ cảnh báo
        self.timer_inactive_color = (150, 150, 150) # Màu xám cho đồng hồ không hoạt động
        self.score_box_fill_color = (255, 193, 7) # Màu vàng
        self.score_box_empty_color = (200, 200, 200)
        self.score_box_border_color = (120, 120, 120)
        
        # Khởi tạo ScoreIndicator
        score_indicator_rect = pygame.Rect(self.rect.x, self.rect.bottom - 225, self.rect.width, 150)
        score_indicator_colors = {'text': self.text_color, 'fill': self.score_box_fill_color, 'border': self.score_box_border_color}
        self.score_indicator = ScoreIndicator(score_indicator_rect, self.font_score_title, self.font_timer, score_indicator_colors, x_img, o_img)

        # Tải hình ảnh cho các nút
        self.quit_img = pygame.image.load(resource_path('img/general/Quit.png')).convert_alpha()
        self.hint_img = pygame.image.load(resource_path('img/ingame/Hint.png')).convert_alpha()

        # Khởi tạo các nút
        button_size = 70
        icon_size_in_button = 40
        self.icon_size_in_button = (icon_size_in_button, icon_size_in_button)
        sound_manager = SoundManager()
        
        buttons_y = self.rect.height - 80

        # Nút Gợi ý
        # Vị trí X sẽ được tính toán động, ở đây chỉ cần Y
        self.hint_button = Button(0, buttons_y - button_size/2, button_size, button_size,
                                  pygame.transform.smoothscale(self.hint_img, self.icon_size_in_button), sound_manager,
                                  color=(100, 200, 255), hover_color=(130, 220, 255), pressed_color=(80, 180, 235))

        # Nút Cài đặt (Settings)
        self.settings_img = pygame.image.load(resource_path('img/ingame/Setting.png')).convert_alpha()
        self.settings_button = Button(0, buttons_y - button_size/2, button_size, button_size,
                                      pygame.transform.smoothscale(self.settings_img, self.icon_size_in_button), sound_manager,
                                      color=(255, 200, 0), hover_color=(255, 220, 50), pressed_color=(235, 180, 0))
        # Nút Thoát
        self.quit_button = Button(0, buttons_y - button_size/2, button_size, button_size,
                                  pygame.transform.smoothscale(self.quit_img, self.icon_size_in_button), sound_manager,
                                  color=(255, 100, 100), hover_color=(255, 130, 130), pressed_color=(235, 80, 80))

        # Danh sách các nút sẽ được hiển thị, lớp con sẽ định nghĩa danh sách này
        self.buttons_to_layout = []

    def _draw_buttons(self, screen, current_player, paused):
        """
        Vẽ các nút điều khiển (Thoát, Gợi ý).
        Các nút sẽ được tự động căn giữa và phân bố đều.
        """

        # --- Logic phân bố nút tự động ---
        num_buttons = len(self.buttons_to_layout)
        if num_buttons == 0:
            return

        button_width = self.buttons_to_layout[0].rect.width
        button_spacing = 20  # Khoảng cách giữa các nút

        total_width = (num_buttons * button_width) + ((num_buttons - 1) * button_spacing)
        start_x = self.rect.centerx - (total_width / 2)

        current_x = start_x
        for button in self.buttons_to_layout:
            # Cập nhật vị trí X của nút
            button.rect.x = current_x
            # Cập nhật vị trí bóng đổ tương ứng
            button.shadow_rect = button.rect.copy().move(button.shadow_offset)
            
            button.draw(screen)
            current_x += button_width + button_spacing

    def _draw_player_avatar(self, screen, player_name, player_area, y_cursor):
        """Vẽ ảnh đại diện cho người chơi, sử dụng phương thức _get_player_icon để hỗ trợ đa hình."""
        player_icon = self._get_player_icon(player_name)
        player_icon_rect = player_icon.get_rect(centerx=player_area.centerx, top=y_cursor)
        screen.blit(player_icon, player_icon_rect)
        return player_icon_rect.bottom

    def _get_player_icon(self, player_name):
        """Trả về ảnh đại diện phù hợp cho người chơi."""
        # Mặc định là ảnh người chơi, lớp con có thể ghi đè để thêm ảnh AI
        return self.player_icon_img

    def _draw_player_info(self, screen, player_char, player_name, player_score, player_time, is_current_player, time_mode, player_area):
        """Vẽ thông tin cho một người chơi cụ thể trong khu vực được chỉ định."""
        if is_current_player:
            pygame.draw.rect(screen, self.highlight_color, player_area, border_radius=10)
        
        y_cursor = player_area.y + 10

        # 1. Icon người chơi (gọi phương thức riêng để lớp con có thể tùy chỉnh)
        y_cursor = self._draw_player_avatar(screen, player_name, player_area, y_cursor)

        # 2. Tên người chơi
        name_surf = self.font_name.render(player_name, True, self.text_color)
        name_rect = name_surf.get_rect(centerx=player_area.centerx, top=y_cursor)
        screen.blit(name_surf, name_rect)
        y_cursor = name_rect.bottom + 15

        # 3. Biểu tượng X/O
        icon_img = self.x_img if player_char == 'X' else self.o_img

        # 3.1. Biểu tượng X/O làm watermark (mờ)
        watermark_icon_img = icon_img.copy()
        watermark_icon_img.set_alpha(40) # Đặt độ trong suốt
        watermark_icon_img = pygame.transform.smoothscale(watermark_icon_img, 
                                                          (int(watermark_icon_img.get_width() * 3), 
                                                           int(watermark_icon_img.get_height() * 3))) # Tăng kích thước
        watermark_rect = watermark_icon_img.get_rect(center=player_area.center)
        screen.blit(watermark_icon_img, watermark_rect)

        y_cursor_bottom = player_area.bottom - 20

        # 4. Vẽ bộ đếm thời gian
        # Chỉ vẽ đồng hồ cho các chế độ có giới hạn thời gian ('total_time' hoặc 'turn_based')
        if time_mode != "no_time" and (time_mode == "total_time" or (time_mode == "turn_based" and is_current_player)):
            timer_color = self.timer_color # Màu mặc định

            if player_time == float('inf'):
                timer_text = ""
            else:
                warning_threshold = 30 if time_mode == "total_time" else 10
                
                seconds = max(0, int(player_time))
                minutes = seconds // 60
                seconds_display = seconds % 60
                timer_text = f"{minutes:01d}:{seconds_display:02d}"

                if time_mode == "total_time" and not is_current_player:
                    timer_color = self.timer_inactive_color
                else:
                    timer_color = self.timer_warning_color if player_time < warning_threshold else self.timer_color

            timer_surf = self.font_timer.render(timer_text, True, timer_color)
            timer_rect = timer_surf.get_rect(centerx=player_area.centerx, bottom=y_cursor_bottom)
            screen.blit(timer_surf, timer_rect)
            y_cursor_bottom = timer_rect.top - 1

        # 5. Thông báo lượt chơi
        if is_current_player: # Kiểm tra xem đây có phải là người chơi hiện tại không
            # Kiểm tra nếu tên người chơi là "Máy tính" thì hiển thị thông báo khác
            if player_name == "Máy tính":
                turn_surf = self.font_turn.render("Máy đang suy nghĩ...", True, self.text_color)
            else:
                turn_surf = self.font_turn.render("Đến lượt bạn!", True, self.text_color)

            turn_rect = turn_surf.get_rect(centerx=player_area.centerx, bottom=y_cursor_bottom)
            screen.blit(turn_surf, turn_rect)

    def draw(self, screen, current_player, remaining_times, time_mode, paused, winning_cells=None, last_move=None, match_history=None, difficulty=None):
        """
        Vẽ toàn bộ bảng thông tin.
        """
        pygame.draw.rect(screen, self.bg_color, self.rect)
        
        area_width = self.rect.width - 20 # Chiều rộng vùng vẽ thông tin người chơi
        area_height = 250 # Chiều cao vùng vẽ thông tin người chơi
        margin_from_center = 10
        # Vị trí đường phân cách giữa 2 người chơi
        divider_y = self.rect.y + area_height + margin_from_center + 10 
        
        # --- Khu vực người chơi 1 ---
        p1_y = divider_y - margin_from_center - area_height
        p1_area = pygame.Rect(self.rect.x + 10, p1_y, area_width, area_height)
        self._draw_player_info(screen, 'X', self.player_names['X'], 0, remaining_times['X'], current_player == 'X', time_mode, p1_area)

        # --- Vẽ đường phân cách giữa thông tin 2 người chơi ---
        pygame.draw.line(screen, self.divider_color, (self.rect.x + 20, divider_y), (self.rect.right - 20, divider_y), 2)

        # --- Khu vực người chơi 2 ---
        p2_y = divider_y + margin_from_center
        p2_area = pygame.Rect(self.rect.x + 10, p2_y, area_width, area_height) # Vị trí và kích thước vùng vẽ thông tin người chơi O
        self._draw_player_info(screen, 'O', self.player_names['O'], 0, remaining_times['O'], current_player == 'O', time_mode, p2_area)

        # Vẽ ScoreIndicator
        if match_history is not None:
            self.score_indicator.draw(screen, match_history)

        self._draw_buttons(screen, current_player, paused)
