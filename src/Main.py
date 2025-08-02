import pygame
import sys

from GameSession import start_game_session
from ui.MainMenu import show_main_menu
from ui.vsAiMode.vsAiSetting import get_ai_game_settings

if __name__ == '__main__':
    """
    Hàm chính của ứng dụng. Khởi tạo Pygame, hiển thị menu chính,
    và điều khiển luồng chính của game.
    """
    pygame.init()

    # Screen dimensions
    screen_width = 1000
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Cờ Caro")

    # Vòng lặp chính của ứng dụng
    while True:
        choice = show_main_menu(screen)

        if choice == '2_players':
            start_game_session(screen)
        elif choice == 'vs_ai':
            # Gọi màn hình cài đặt cho chế độ chơi với máy
            ai_settings = get_ai_game_settings(screen)
        elif choice == 'quit':
            break # Thoát khỏi vòng lặp chính của ứng dụng

    pygame.quit()
    sys.exit()