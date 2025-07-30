import pygame

from sys import exit
from BeforeGame.EnterNameDialog import get_player_names
from InGame.EndScreen import show_end_screen
from InGame.BoardLogic import BoardLogic
from InGame.TimerLogic import TurnTimer
from InGame.MainScreen import GameBoard

if __name__ == '__main__':
    pygame.init()

    # Screen dimensions
    screen_width = 1000
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Cờ Caro")

    # --- Màn hình nhập tên ---
    player_data = get_player_names(screen)
    if player_data is None:
        pygame.quit()
        exit()
    player1_name, player2_name = player_data
    player_names = {'X': player1_name, 'O': player2_name}

    # Game dimensions
    # Tính toán kích thước để đảm bảo các ô cờ vừa khít và không có khoảng trống
    cell_size = 40
    board_height_cells = screen_height // cell_size

    # Tính toán chiều rộng thực tế của panel và bàn cờ.
    # Panel sẽ có chiều rộng TỐI THIỂU là 250px, phần dư từ phép chia ô cờ
    # sẽ được thêm vào panel để lấp đầy màn hình.
    board_width_cells = (screen_width - 250) // cell_size
    panel_actual_width = screen_width - (board_width_cells * cell_size)

    # Khởi tạo bàn cờ và logic game
    board = GameBoard(board_width_cells, board_height_cells, cell_size, screen_width, screen_height, player_names)

    # Khởi tạo logic game
    WIN_LENGTH = 5
    game_logic = BoardLogic(board_width_cells, board_height_cells, WIN_LENGTH)

    # Các biến trạng thái game
    current_player = 'X'
    game_over = False
    winner = None

    # --- Khởi tạo bộ đếm thời gian ---
    timer = TurnTimer(time_limit_seconds=20)
    timer.start_turn()

    running = True
    while running:
        # --- Tính toán thời gian còn lại ---
        remaining_time = timer.get_remaining_time()
        if not game_over:
            if timer.is_time_up():
                # Hết giờ, tự động đổi lượt
                current_player = 'O' if current_player == 'X' else 'X'
                timer.start_turn()
        else:
            remaining_time = timer.time_limit  # Không cần đếm khi game kết thúc

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Chỉ xử lý click chuột khi game chưa kết thúc
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                # Chỉ xử lý click nếu nó nằm trong khu vực bàn cờ
                if mouseX >= panel_actual_width:
                    clicked_row = mouseY // cell_size
                    # Bù trừ cho độ rộng của panel khi tính cột
                    clicked_col = (mouseX - panel_actual_width) // cell_size

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
                            # Nếu game chưa kết thúc, đổi lượt chơi
                            current_player = 'O' if current_player == 'X' else 'X'
                        
                        # Reset bộ đếm thời gian cho lượt mới sau khi đi
                        timer.start_turn()
        
        screen.fill((255, 255, 255))  # Fill background white
        board.draw(screen, current_player, remaining_time)

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
                timer.start_turn() # Reset timer cho game mới
            else:
                running = False # Thoát khỏi vòng lặp game

        pygame.display.flip()

    pygame.quit()