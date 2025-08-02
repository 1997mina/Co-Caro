import pygame
import time

from logic.BoardLogic import BoardLogic
from logic.aiLogic import AIPlayer
from manager.GameStateManager import GameStateManager
from manager.SoundManager import SoundManager
from manager.TimerManager import TimerManager
from ui.EndScreen import show_end_screen
from ui.GameBoard import GameBoard
from ui.vsAiMode.vsAiSetting import get_ai_game_settings
from ui.vsAiMode.vsAiInfoPanel import vsAiInfoPanel

def start_ai_game_session(screen):
    """
    Bắt đầu một phiên chơi game mới với AI.
    """
    screen_width, screen_height = screen.get_size()
    
    # --- Màn hình cài đặt ---
    game_settings = get_ai_game_settings(screen)
    if game_settings is None:
        return # Quay về menu chính
    
    # Giải nén 3 giá trị từ màn hình cài đặt
    player_name_from_input, human_player_char, first_turn = game_settings

    # Đặt giá trị mặc định cho thời gian vì màn hình cài đặt không có
    time_mode = "total_time"
    time_limit = 300 # 5 phút

    # Xác định quân cờ và tên của người chơi và AI
    ai_player_char = 'O' if human_player_char == 'X' else 'X'
    player_name = player_name_from_input.strip() or "Người chơi" # Tên mặc định nếu không nhập
    ai_name = "Máy tính"

    # Tạo từ điển tên người chơi dựa trên quân cờ
    if human_player_char == 'X':
        player_names = {'X': player_name, 'O': ai_name}
    else:
        player_names = {'X': ai_name, 'O': player_name}

    # Xác định người đi trước
    current_player = human_player_char if first_turn == 'player' else ai_player_char
    initial_player = current_player # Lưu lại người đi đầu để reset ván mới

    # --- Cấu hình bàn cờ và panel ---
    cell_size = 40
    board_height_cells = screen_height // cell_size
    board_width_cells = (screen_width - 250) // cell_size
    panel_actual_width = screen_width - (board_width_cells * cell_size)
    board_pixel_width = board_width_cells * cell_size
    board_rect = pygame.Rect(panel_actual_width, 0, board_pixel_width, screen_height)

    # Khởi tạo bàn cờ và logic game
    board = GameBoard(board_width_cells, board_height_cells, cell_size, screen_width, screen_height, player_names, vsAiInfoPanel)

    # Khởi tạo logic game
    WIN_LENGTH = 5
    game_logic = BoardLogic(board_width_cells, board_height_cells, WIN_LENGTH)
    # Khởi tạo AI với các quân cờ tương ứng
    ai = AIPlayer(ai_symbol=ai_player_char, human_symbol=human_player_char)

    # --- Khởi tạo các trình quản lý ---
    sound_manager = SoundManager()
    timer = TimerManager(time_limit, time_mode)
    game_state = GameStateManager(screen, board_rect)
    
    timer.switch_turn(current_player)
    winner = None
    winning_cells = []

    running = True
    while running:
        if game_state.is_playing():
            if timer.is_time_up():
                game_state.set_game_over(True)
                winner = 'O' if current_player == 'X' else 'X'
                sound_manager.play_game_over()

            # --- Lượt đi của AI ---
            if current_player == ai_player_char:
                pygame.time.wait(500) # Giả lập AI đang "suy nghĩ"
                # Đồng bộ trạng thái bàn cờ từ UI sang logic trước khi AI tính toán
                game_logic.board = board.board
                move = ai.find_best_move(game_logic)
                if move:
                    row, col = move
                    board.mark_square(row, col, current_player)
                    sound_manager.play_move(current_player)
                    
                    winning_line = game_logic.check_win(board.board, current_player, row, col)
                    if winning_line:
                        winner = current_player
                        game_state.set_game_over(True)
                        sound_manager.play_game_over()
                        winning_cells = winning_line
                    elif game_logic.is_board_full(board.board):
                        winner = "Draw"
                        game_state.set_game_over(True)
                    else:
                        current_player = human_player_char
                        timer.switch_turn(current_player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_state.handle_event(event, timer, board):
                continue

            # --- Lượt đi của người chơi ---
            if game_state.is_playing() and current_player != ai_player_char:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    if mouseX >= panel_actual_width:
                        clicked_row = mouseY // cell_size
                        clicked_col = (mouseX - panel_actual_width) // cell_size
                        if board.mark_square(clicked_row, clicked_col, current_player):
                            sound_manager.play_move(current_player)
                            winning_line = game_logic.check_win(board.board, current_player, clicked_row, clicked_col)
                            if winning_line:
                                winner = current_player
                                game_state.set_game_over(True)
                                sound_manager.play_game_over()
                                winning_cells = winning_line
                            elif game_logic.is_board_full(board.board):
                                winner = "Draw"
                                game_state.set_game_over(True)
                            else:
                                current_player = ai_player_char
                                timer.switch_turn(current_player)

        # --- Vẽ màn hình ---
        screen.fill((255, 255, 255))
        remaining_times = {'X': timer.get_remaining_time('X'), 'O': timer.get_remaining_time('O')}
        board.draw(screen, current_player, remaining_times, time_mode, game_state.is_paused(), winning_cells)
        game_state.draw_overlay()

        if game_state.game_over:
            winner_display_name = "Draw" if winner == "Draw" else player_names.get(winner, "Unknown")
            play_again = show_end_screen(screen, winner_display_name, board_rect)
            if play_again:
                # Reset game
                board.reset()
                game_state.reset()
                current_player = initial_player # Quay về người đi đầu của ván
                winning_cells = []
                timer = TimerManager(time_limit, time_mode)
                timer.switch_turn(initial_player)
            else:
                running = False # Thoát về menu chính

        pygame.display.flip()
