import pygame

from sys import exit
from SettingFrame.TwoPlayerSetting import get_player_names
from InGame.EndScreen import show_end_screen
from InGame.BoardLogic import BoardLogic
from Manager.TimerManager import TimerManager
from InGame.GameBoard import GameBoard
from Manager.SoundManager import SoundManager
from Manager.GameStateManager import GameStateManager

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
    player1_name, player2_name, time_mode, time_limit = player_data
    player_names = {'X': player1_name, 'O': player2_name}
    
    # Tính toán kích thước để đảm bảo các ô cờ vừa khít và không có khoảng trống
    cell_size = 40
    board_height_cells = screen_height // cell_size

    # Tính toán chiều rộng thực tế của panel và bàn cờ.
    # Panel sẽ có chiều rộng TỐI THIỂU là 250px, phần dư từ phép chia ô cờ
    # sẽ được thêm vào panel để lấp đầy màn hình.
    board_width_cells = (screen_width - 250) // cell_size
    panel_actual_width = screen_width - (board_width_cells * cell_size)
    board_pixel_width = board_width_cells * cell_size

    # Xác định khu vực bàn cờ để làm mờ khi tạm dừng
    board_rect = pygame.Rect(panel_actual_width, 0, board_pixel_width, screen_height)

    # Khởi tạo bàn cờ và logic game
    board = GameBoard(board_width_cells, board_height_cells, cell_size, screen_width, screen_height, player_names)

    # Khởi tạo logic game
    WIN_LENGTH = 5
    game_logic = BoardLogic(board_width_cells, board_height_cells, WIN_LENGTH)

    # --- Khởi tạo các trình quản lý ---
    current_player = 'X'
    winning_cells = [] # Lưu tọa độ các ô thắng

    # --- Khởi tạo trình quản lý âm thanh ---
    sound_manager = SoundManager()

    # --- Khởi tạo bộ đếm thời gian ---
    timer = TimerManager(time_limit, time_mode)
    timer.switch_turn(current_player)
    
    # --- Khởi tạo trình quản lý trạng thái game ---
    game_state = GameStateManager(screen, board_rect)
    winner = None

    running = True
    while running:
        # --- Tính toán thời gian còn lại ---
        if game_state.is_playing():
            if timer.is_time_up():
                # Hết giờ, người chơi hiện tại bị xử thua.
                game_state.set_game_over(True)
                winner = 'O' if current_player == 'X' else 'X'
                sound_manager.play_game_over()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Ưu tiên xử lý sự kiện của game state (như nút pause)
            if game_state.handle_event(event, timer, board):
                continue # Nếu sự kiện đã được xử lý, bỏ qua phần còn lại

            # Chỉ xử lý logic game nếu game đang chạy
            if game_state.is_playing():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    # Chỉ xử lý click nếu nó nằm trong khu vực bàn cờ
                    if mouseX >= panel_actual_width:
                        clicked_row = mouseY // cell_size
                        # Bù trừ cho độ rộng của panel khi tính cột
                        clicked_col = (mouseX - panel_actual_width) // cell_size
                        if board.mark_square(clicked_row, clicked_col, current_player):
                            sound_manager.play_move(current_player)
                            # Kiểm tra thắng
                            winning_line = game_logic.check_win(board.board, current_player, clicked_row, clicked_col)
                            if winning_line:
                                winner = current_player
                                game_state.set_game_over(True)
                                sound_manager.play_game_over()
                                winning_cells = winning_line
                            # Kiểm tra hòa
                            elif game_logic.is_board_full(board.board):
                                winner = "Draw"
                                game_state.set_game_over(True)
                            else:
                                # Nếu game chưa kết thúc, đổi lượt chơi
                                current_player = 'O' if current_player == 'X' else 'X'
                            # Chuyển lượt cho timer
                            timer.switch_turn(current_player)
        
        screen.fill((255, 255, 255))  # Fill background white
        # Lấy thời gian còn lại của cả hai người chơi để hiển thị
        remaining_times = {'X': timer.get_remaining_time('X'), 'O': timer.get_remaining_time('O')}
        board.draw(screen, current_player, remaining_times, time_mode, game_state.is_paused(), winning_cells)

        # Vẽ màn hình overlay nếu game đang tạm dừng
        game_state.draw_overlay()

        # Hiển thị thông báo khi game kết thúc
        if game_state.game_over:
            if winner == "Draw":
                winner_display_name = "Draw"
            else:
                winner_display_name = player_names.get(winner, "Unknown")
            
            # Hiển thị màn hình kết thúc và chờ lựa chọn của người dùng
            play_again = show_end_screen(screen, winner_display_name, board_rect)

            if play_again:
                # Thiết lập lại trạng thái game để bắt đầu ván mới
                board.reset()
                game_state.reset()
                current_player = 'X'
                winning_cells = [] # Xóa các ô thắng của ván trước
                timer = TimerManager(time_limit, time_mode) # Reset timer cho game mới
                timer.switch_turn(current_player)
            else:
                running = False # Thoát khỏi vòng lặp game

        pygame.display.flip()

    pygame.quit()