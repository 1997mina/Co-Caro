import pygame

from BeforeGame.EnterNameDialog import get_player_names
from EndGame import show_end_screen
from InGame.BoardLogic import BoardLogic
from InGame.GameBoard import GameBoard

if __name__ == '__main__':
    pygame.init()

    # Screen dimensions
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Cờ Caro")

    # --- Màn hình nhập tên ---
    player1_name, player2_name = get_player_names(screen)

    # Board dimensions
    cell_size = 40
    board_width = screen_width // cell_size
    board_height = screen_height // cell_size
    board = GameBoard(board_width, board_height, cell_size)

    # Khởi tạo logic game
    WIN_LENGTH = 5
    game_logic = BoardLogic(board_width, board_height, WIN_LENGTH)

    # Các biến trạng thái game
    current_player = 'X'
    game_over = False
    winner = None
    player_names = {'X': player1_name, 'O': player2_name}

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Chỉ xử lý click chuột khi game chưa kết thúc
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // cell_size
                clicked_col = mouseX // cell_size

                # Nếu ô hợp lệ và còn trống, đánh dấu và đổi lượt
                if board.mark_square(clicked_row, clicked_col, current_player):
                    # Kiểm tra thắng
                    if game_logic.check_win(board.board, current_player, clicked_row, clicked_col):
                        winner = current_player
                        game_over = True
                    # Kiểm tra hòa
                    elif game_logic.is_board_full(board.board):
                        winner = "Draw"
                        game_over = True
                    else:
                        # Đổi lượt chơi
                        current_player = 'O' if current_player == 'X' else 'X'

        screen.fill((255, 255, 255))  # Fill background white
        board.draw(screen)

        # Hiển thị thông báo khi game kết thúc
        if game_over:
            if winner == "Draw":
                winner_display_name = "Draw"
            else:
                winner_display_name = player_names.get(winner, "Unknown")
            
            # Hiển thị màn hình kết thúc và chờ lựa chọn của người dùng
            play_again = show_end_screen(screen, winner_display_name)

            if play_again:
                # Thiết lập lại trạng thái game để bắt đầu ván mới
                board.reset()
                game_over = False
                winner = None
                current_player = 'X'
            else:
                running = False # Thoát khỏi vòng lặp game

        pygame.display.flip()

    pygame.quit()