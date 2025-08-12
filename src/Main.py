import pygame
import sys

from ui.vsAiMode.aiGameSession import AIGameSession
from ui.MainMenu import show_main_menu
from ui.twoplayermode.TwoPlayerGameSession import TwoPlayerGameSession

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
            # Khởi tạo và chạy session cho 2 người chơi
            session = TwoPlayerGameSession(screen)
            session.run()
        elif choice == 'vs_ai':
            # Khởi tạo và chạy session cho chế độ vs AI
            session = AIGameSession(screen)
            session.run()
        elif choice == 'quit':
            break # Thoát khỏi vòng lặp chính của ứng dụng

    pygame.quit()
    sys.exit()