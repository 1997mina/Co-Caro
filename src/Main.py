import pygame
import sys
import os

from ui.twoplayermode.TwoPlayerGameSession import start_two_players_session
from ui.MainMenu import show_main_menu
from ui.vsAiMode.aiGameSession import start_ai_game_session

if __name__ == '__main__':
    """
    Hàm chính của ứng dụng. Khởi tạo Pygame, hiển thị menu chính,
    và điều khiển luồng chính của game.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)

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
            start_two_players_session(screen)
        elif choice == 'vs_ai':
            start_ai_game_session(screen)
        elif choice == 'quit':
            break # Thoát khỏi vòng lặp chính của ứng dụng

    pygame.quit()
    sys.exit()