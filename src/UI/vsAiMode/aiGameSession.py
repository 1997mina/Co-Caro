import pygame
import threading

from logic.BoardLogic import BoardLogic
from logic.aiLogic import AIPlayer
from manager.GameStateManager import GameStateManager
from manager.CursorManager import CursorManager
from manager.SoundManager import SoundManager
from manager.TimerManager import TimerManager
from ui.EndScreen import show_end_screen, show_quit_confirmation_dialog, show_final_victory_screen
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
    
    # Giải nén 4 giá trị từ màn hình cài đặt
    player_name_from_input, human_player_char, first_turn, difficulty = game_settings

    # Đặt giá trị mặc định cho thời gian vì màn hình cài đặt không có
    time_mode = "turn_based" # Chỉ người chơi bị tính giờ
    time_limit = 25 # 20 giây cho người chơi

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

    # Khởi tạo lịch sử các ván đấu
    match_history = []

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
    game_state = GameStateManager(screen, board_rect, sound_manager)
    cursor_manager = CursorManager()
    timer = TimerManager(time_limit, time_mode, ai_player=ai_player_char)
    
    timer.switch_turn(current_player)
    winner = None
    winning_cells = []
    last_move = None # Lưu tọa độ nước đi cuối cùng
    hint_cell = None # Lưu tọa độ ô được gợi ý
    hint_used_this_round = False # Cờ để theo dõi việc sử dụng gợi ý
    
    # Biến để quản lý luồng của AI
    ai.set_difficulty(difficulty)
    ai_is_thinking = False
    ai_thread = None
    ai_move_result = None

    running = True
    while running:
        if game_state.is_playing():
            if timer.is_time_up():
                game_state.set_game_over(True)
                winner = 'O' if current_player == 'X' else 'X'
                sound_manager.play_game_over()
                # Cập nhật lịch sử đấu ngay lập tức
                if len(match_history) < 5:
                    match_history.append(winner)

            # --- Xử lý lượt đi của AI (sử dụng thread) ---
            # 1. Bắt đầu luồng tính toán nếu đến lượt AI và AI chưa "suy nghĩ"
            if current_player == ai_player_char and not ai_is_thinking:
                ai_is_thinking = True
                # Đồng bộ bàn cờ trước khi đưa vào luồng
                game_logic.board = [row[:] for row in board.board]
                is_first_move = not any(any(row) for row in game_logic.board)
                
                # Hàm mục tiêu cho luồng AI
                def run_ai_calculation():
                    nonlocal ai_move_result
                    ai_move_result = ai.find_best_move(game_logic, is_first_move) # Đặt giới hạn 8 giây

                ai_thread = threading.Thread(target=run_ai_calculation)
                ai_thread.start()

            # 2. Kiểm tra xem luồng AI đã tính toán xong chưa
            if ai_is_thinking and ai_move_result is not None:
                row, col = ai_move_result
                last_move = (row, col) # Lưu nước đi của AI
                board.mark_square(row, col, current_player)
                sound_manager.play_move(current_player)
                
                winning_line = game_logic.check_win(board.board, current_player, row, col)
                if winning_line:
                    winner = current_player
                    game_state.set_game_over(True)
                    sound_manager.play_game_over()
                    # Cập nhật lịch sử đấu ngay lập tức
                    if len(match_history) < 5:
                        match_history.append(winner)
                    winning_cells = winning_line
                elif game_logic.is_board_full(board.board):
                    winner = "Draw"
                    game_state.set_game_over(True)
                else:
                    current_player = human_player_char
                    timer.switch_turn(current_player)
                
                # Reset trạng thái của AI
                ai_is_thinking = False
                ai_move_result = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_state.handle_event(event, timer, board):
                continue

            # Xử lý nhấn phím ESC để thoát game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not game_state.game_over and not ai_is_thinking: # Chỉ hiển thị khi game chưa kết thúc và AI không đang suy nghĩ
                    if show_quit_confirmation_dialog(screen, board_rect):
                        running = False # Đặt cờ để thoát vòng lặp game
                        continue

            # --- Xử lý click nút Gợi ý ---
            if game_state.is_playing() and current_player == human_player_char:
                if board.player_info_panel.hint_button.handle_event(event):
                    hint_used_this_round = True # Đánh dấu là đã sử dụng gợi ý
                    # AI sẽ tìm nước đi tốt nhất cho người chơi hiện tại (là con người)
                    # Để làm điều này, chúng ta tạm thời coi AI là người chơi hiện tại
                    # và tìm nước đi tốt nhất cho "mình"
                    temp_ai = AIPlayer(ai_symbol=human_player_char, human_symbol=ai_player_char)
                    temp_ai.set_difficulty(difficulty)
                    game_logic.board = [row[:] for row in board.board]
                    is_first_move = not any(any(row) for row in game_logic.board)
                    hint_cell = temp_ai.find_best_move(game_logic, is_first_move)
                    # Không cần làm gì thêm, hint_cell sẽ được truyền vào board.draw()
                    continue

            # --- Lượt đi của người chơi ---
            if game_state.is_playing() and current_player != ai_player_char:
                # Xử lý click nút Thoát trên InfoPanel
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Chỉ cho phép thoát khi AI không đang suy nghĩ và nút thoát được nhấn
                    if board.player_info_panel.quit_button.rect.collidepoint(event.pos) and not ai_is_thinking:
                        sound_manager.play_button_click()
                        if show_quit_confirmation_dialog(screen, board_rect):
                            running = False
                            continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    if mouseX >= panel_actual_width:
                        clicked_row = mouseY // cell_size
                        clicked_col = (mouseX - panel_actual_width) // cell_size
                        if board.mark_square(clicked_row, clicked_col, current_player):
                            hint_cell = None # Xóa gợi ý sau khi người chơi đã đi
                            last_move = (clicked_row, clicked_col) # Lưu nước đi của người chơi
                            sound_manager.play_move(current_player)
                            winning_line = game_logic.check_win(board.board, current_player, clicked_row, clicked_col)
                            if winning_line:
                                winner = current_player
                                game_state.set_game_over(True)
                                sound_manager.play_game_over()
                                # Cập nhật lịch sử đấu ngay lập tức
                                if len(match_history) < 5:
                                    match_history.append(winner)
                                winning_cells = winning_line
                            elif game_logic.is_board_full(board.board):
                                winner = "Draw"
                                game_state.set_game_over(True)
                            else:
                                current_player = ai_player_char
                                timer.switch_turn(current_player)

        # --- Cập nhật trạng thái nút Gợi ý ---
        # Nút gợi ý chỉ được bật khi:
        # 1. Game đang diễn ra (không tạm dừng, không kết thúc)
        # 2. Đến lượt của người chơi
        # 3. Gợi ý chưa được sử dụng trong ván này
        is_hint_available = game_state.is_playing() and current_player == human_player_char and not hint_used_this_round
        board.player_info_panel.hint_button.is_enabled = is_hint_available

        # --- Cập nhật con trỏ chuột ---
        cursor_manager.reset()
        # Đăng ký các nút từ InfoPanel
        for button in board.player_info_panel.buttons_to_layout:
            cursor_manager.add_clickable_area(button.rect, button.is_enabled)
        # Cập nhật trạng thái con trỏ
        cursor_manager.update(pygame.mouse.get_pos())

        # --- Vẽ màn hình ---
        screen.fill((255, 255, 255))
        remaining_times = {'X': timer.get_remaining_time('X'), 'O': timer.get_remaining_time('O')}
        board.draw(screen, current_player, 
                   remaining_times, time_mode, game_state.is_paused(),
                   winning_cells, last_move, match_history, hint_cell, difficulty)
        game_state.draw_overlay()

        if game_state.game_over:
            winner_display_name = "Hòa" if winner == "Draw" else player_names.get(winner, "Unknown")

            # --- KIỂM TRA NGƯỜI THẮNG CHUNG CUỘC ---
            wins_X = match_history.count('X')
            wins_O = match_history.count('O')
            overall_winner = None
            if wins_X >= 3:
                overall_winner = 'X'
            elif wins_O >= 3:
                overall_winner = 'O'
            
            if overall_winner:
                final_winner_name = player_names.get(overall_winner, "Unknown")
                show_final_victory_screen(screen, final_winner_name, board_rect, match_history, board.x_img, board.o_img)
                running = False # Kết thúc phiên chơi
                continue # Bỏ qua phần còn lại của vòng lặp

            play_again = show_end_screen(screen, winner_display_name, board_rect, match_history, board.x_img, board.o_img)
            if play_again:
                # Reset game
                board.reset()
                game_state.reset()
                current_player = initial_player # Quay về người đi đầu của ván
                winner = None
                hint_used_this_round = False # Reset cờ gợi ý cho ván mới
                hint_cell = None
                last_move = None
                winning_cells = []
                timer = TimerManager(time_limit, time_mode, ai_player=ai_player_char)
                timer.switch_turn(initial_player)
            else:
                running = False # Thoát về menu chính

        pygame.display.flip()
