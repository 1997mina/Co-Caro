import pygame

from components.Button import Button
from manager.SoundManager import SoundManager
from manager.SettingsManager import SettingsManager
from components.Slider import Slider
from manager.CursorManager import CursorManager

# Hằng số
WHITE = (255, 255, 255)
TITLE_COLOR = (40, 40, 40)
BACK_COLOR = (100, 100, 100)
BACK_HOVER_COLOR = (130, 130, 130)
BACK_PRESSED_COLOR = (80, 80, 80)
FILL_COLOR = (0, 120, 215) # Xanh dương cho phần đã điền của slider

class InGameSettings:
    """
    Hiển thị hộp thoại cài đặt nhanh trong game (chỉ âm lượng).
    Hộp thoại này sẽ vẽ đè lên màn hình game hiện tại.
    """
    def __init__(self, screen, board_rect):
        self.screen = screen
        self.board_rect = board_rect
        self.sound_manager = SoundManager()
        self.settings_manager = SettingsManager()
        self.cursor_manager = CursorManager()

        # --- Tạo một lớp phủ bán trong suốt chỉ cho khu vực bàn cờ ---
        self.background = self.screen.copy()
        self.overlay = pygame.Surface(self.board_rect.size, pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 150))

        # --- Hộp thoại ---
        dialog_width = 650
        dialog_height = 350
        self.dialog_rect = pygame.Rect(0, 0, dialog_width, dialog_height)
        self.dialog_rect.center = self.board_rect.center
        self.dialog_bg_color = (230, 230, 230)
        self.dialog_border_color = (100, 100, 100)

        # --- Tiêu đề ---
        font_title = pygame.font.SysFont("Times New Roman", 48, bold=True)
        self.title_surf = font_title.render("Cài đặt Âm thanh", True, TITLE_COLOR)
        self.title_rect = self.title_surf.get_rect(centerx=self.dialog_rect.centerx, top=self.dialog_rect.top + 15)

        # --- Thanh trượt ---
        slider_width = 450
        slider_height = 20
        original_music_volume = self.settings_manager.get('music_volume')
        original_sfx_volume = self.settings_manager.get('sfx_volume')

        self.music_volume_slider = Slider(0, 0, slider_width, slider_height,
                                     0, 100, int(original_music_volume * 100), self.sound_manager,
                                     "Âm lượng nhạc nền: ", value_suffix="%",
                                     track_fill_color=FILL_COLOR)
        self.music_volume_slider.set_center_component(self.dialog_rect.centerx, self.dialog_rect.centery - 30)

        self.sfx_volume_slider = Slider(0, 0, slider_width, slider_height,
                                   0, 100, int(original_sfx_volume * 100), self.sound_manager,
                                   "Âm lượng hiệu ứng: ", value_suffix="%",
                                   track_fill_color=FILL_COLOR)
        self.sfx_volume_slider.set_center_component(self.dialog_rect.centerx, self.dialog_rect.centery + 80)

        # --- Nút Đóng ---
        close_button_width = 180
        close_button_height = 50
        self.close_button = Button(self.dialog_rect.centerx - close_button_width / 2, self.dialog_rect.bottom - close_button_height - 20,
                              close_button_width, close_button_height,
                              pygame.font.SysFont("Times New Roman", 32, bold=True).render("Đóng", True, WHITE), self.sound_manager,
                              color=BACK_COLOR, hover_color=BACK_HOVER_COLOR, pressed_color=BACK_PRESSED_COLOR,
                              border_radius=10)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False # Signal to stop running

            if self.music_volume_slider.handle_event(event):
                new_volume = self.music_volume_slider.get_value() / 100.0
                self.sound_manager.set_music_volume(new_volume)

            if self.sfx_volume_slider.handle_event(event):
                new_volume = self.sfx_volume_slider.get_value() / 100.0
                self.sound_manager.set_sfx_volume(new_volume)

            if self.close_button.handle_event(event):
                return False # Signal to stop running
        return True # Signal to continue running

    def _update_cursor(self):
        mouse_pos = pygame.mouse.get_pos()
        self.cursor_manager.reset()
        self.music_volume_slider.add_to_cursor_manager(self.cursor_manager)
        self.sfx_volume_slider.add_to_cursor_manager(self.cursor_manager)
        self.cursor_manager.add_clickable_area(self.close_button.rect, True)
        self.cursor_manager.update(mouse_pos)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.overlay, self.board_rect.topleft)
        pygame.draw.rect(self.screen, self.dialog_bg_color, self.dialog_rect, border_radius=15)
        pygame.draw.rect(self.screen, self.dialog_border_color, self.dialog_rect, 3, border_radius=15)

        self.screen.blit(self.title_surf, self.title_rect)
        self.music_volume_slider.draw(self.screen)
        self.sfx_volume_slider.draw(self.screen)
        self.close_button.draw(self.screen)

        pygame.display.flip()

    def show(self):
        running = True
        while running:
            running = self._handle_events()
            self._update_cursor()
            self._draw()