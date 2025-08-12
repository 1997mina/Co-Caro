import pygame

from logic.BoardLogic import BoardLogic
from manager.GameStateManager import GameStateManager
from manager.CursorManager import CursorManager
from manager.SoundManager import SoundManager
from manager.TimerManager import TimerManager
from ui.EndScreen import show_end_screen, show_quit_confirmation_dialog, show_final_victory_screen
from ui.GameBoard import GameBoard

class GameSession:
    """
    Lớp cơ sở (cha) cho các phiên chơi game (2 người, vs AI).
    Chứa các logic chung về vòng lặp game, quản lý trạng thái, xử lý sự kiện,
    và hiển thị màn hình kết thúc.
    """
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.running = True

        # Các thuộc tính sẽ được khởi tạo trong _initialize_components
        self.player_names = {}
        self.time_mode = "turn_based"
        self.time_limit = 30
        self.current_player = 'X'
        self.initial_player = 'X'
        self.match_history = []
        self.board = None
        self.game_logic = None
        self.sound_manager = None
        self.cursor_manager = None
        self.game_state = None
        self.timer = None
        self.winner = None
        self.winning_cells = []
        self.last_move = None

    def _initialize_components(self, player_names, time_mode, time_limit, first_turn_char, info_panel_class):
        """
        Khởi tạo các thành phần cốt lõi của game sau khi có cài đặt.
        """
        self.player_names = player_names
        self.time_mode = time_mode
        self.time_limit = time_limit
        self.current_player = first_turn_char
        self.initial_player = first_turn_char
        self.match_history = []

        # --- Cấu hình bàn cờ và panel ---
        self.cell_size = 40
        board_height_cells = self.screen_height // self.cell_size
        board_width_cells = (self.screen_width - 250) // self.cell_size
        panel_actual_width = self.screen_width - (board_width_cells * self.cell_size)
        board_pixel_width = board_width_cells * self.cell_size
        self.board_rect = pygame.Rect(panel_actual_width, 0, board_pixel_width, self.screen_height)

        # --- Khởi tạo các đối tượng quản lý và logic ---
        self.board = GameBoard(board_width_cells, board_height_cells, self.cell_size, self.screen_width, self.screen_height, self.player_names, info_panel_class)
        
        WIN_LENGTH = 5
        self.game_logic = BoardLogic(board_width_cells, board_height_cells, WIN_LENGTH)
        
        self.sound_manager = SoundManager()
        self.cursor_manager = CursorManager()
        self.game_state = GameStateManager(self.screen, self.board_rect, self.sound_manager)
        
        # Lớp con có thể cần truyền thêm tham số (ví dụ: ai_player)
        self._initialize_timer()

        # --- Reset các biến trạng thái cho ván mới ---
        self.winner = None
        self.winning_cells = []
        self.last_move = None

    def _initialize_timer(self):
        """Khởi tạo hoặc reset timer. Lớp con có thể ghi đè."""
        self.timer = TimerManager(self.time_limit, self.time_mode)
        self.timer.switch_turn(self.current_player)

    def _setup_session(self):
        """
        Lớp con BẮT BUỘC phải ghi đè phương thức này.
        - Hiển thị màn hình cài đặt tương ứng.
        - Lấy dữ liệu cài đặt.
        - Gọi self._initialize_components() với dữ liệu đó.
        - Trả về False nếu người dùng thoát khỏi màn hình cài đặt.
        """
        raise NotImplementedError("Lớp con phải triển khai phương thức _setup_session")

    def _handle_player_turn(self, event):
        """
        Lớp con BẮT BUỘC phải ghi đè phương thức này.
        Xử lý logic cho lượt đi của người chơi hoặc AI.
        """
        raise NotImplementedError("Lớp con phải triển khai phương thức _handle_player_turn")

    def _check_time_up(self):
        """Kiểm tra nếu hết giờ và xử lý."""
        if self.game_state.is_playing() and self.timer.is_time_up():
            self.game_state.set_game_over(True)
            self.winner = 'O' if self.current_player == 'X' else 'X'
            self.sound_manager.play_game_over()
            if len(self.match_history) < 5:
                self.match_history.append(self.winner)

    def _handle_events(self):
        """Xử lý các sự kiện chung của Pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                exit()

            if self.game_state.handle_event(event, self.timer, self.board):
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not self.game_state.game_over:
                    if show_quit_confirmation_dialog(self.screen, self.board_rect):
                        self.running = False
                    continue

            # Gọi phương thức xử lý lượt đi của lớp con
            self._handle_player_turn(event)

    def _update_cursor(self):
        """Cập nhật con trỏ chuột dựa trên các nút có thể click."""
        self.cursor_manager.reset()
        for button in self.board.player_info_panel.buttons_to_layout:
            self.cursor_manager.add_clickable_area(button.rect, button.is_enabled)
        self.cursor_manager.update(pygame.mouse.get_pos())

    def _draw_screen(self):
        """Vẽ tất cả các thành phần lên màn hình."""
        self.screen.fill((255, 255, 255))
        remaining_times = {'X': self.timer.get_remaining_time('X'), 'O': self.timer.get_remaining_time('O')}
        
        # Lớp con có thể cần truyền thêm tham số vào board.draw()
        self.board.draw(self.screen, self.current_player, 
                        remaining_times, self.time_mode, self.game_state.is_paused(),
                        self.winning_cells, self.last_move, self.match_history)
        
        self.game_state.draw_overlay()

    def _handle_game_over(self):
        """Xử lý logic khi một ván game kết thúc."""
        if not self.game_state.game_over:
            return

        winner_display_name = "Hòa" if self.winner == "Draw" else self.player_names.get(self.winner, "Unknown")

        # --- KIỂM TRA NGƯỜI THẮNG CHUNG CUỘC ---
        wins_X = self.match_history.count('X')
        wins_O = self.match_history.count('O')
        overall_winner = None
        if wins_X >= 3:
            overall_winner = 'X'
        elif wins_O >= 3:
            overall_winner = 'O'
        
        if overall_winner:
            final_winner_name = self.player_names.get(overall_winner, "Unknown")
            show_final_victory_screen(self.screen, final_winner_name, self.board_rect, self.match_history, self.board.x_img, self.board.o_img)
            self.running = False # Kết thúc phiên chơi
            return

        play_again = show_end_screen(self.screen, winner_display_name, self.board_rect, self.match_history, self.board.x_img, self.board.o_img)
        if play_again:
            self._reset_for_new_round()
        else:
            self.running = False

    def _reset_for_new_round(self):
        """Thiết lập lại trạng thái để bắt đầu ván mới."""
        self.board.reset()
        self.game_state.reset()
        self.current_player = self.initial_player
        self.winner = None
        self.last_move = None
        self.winning_cells = []
        self._initialize_timer()

    def _post_move_processing(self, row, col):
        """
        Xử lý logic sau khi một nước đi được thực hiện (bất kể là người hay AI).
        Bao gồm kiểm tra thắng, hòa, và đổi lượt.
        """
        self.sound_manager.play_move(self.current_player)
        self.last_move = (row, col)

        winning_line = self.game_logic.check_win(self.board.board, self.current_player, row, col)
        if winning_line:
            self.winner = self.current_player
            self.game_state.set_game_over(True)
            self.sound_manager.play_game_over()
            self.winning_cells = winning_line
            if len(self.match_history) < 5:
                self.match_history.append(self.winner)
        elif self.game_logic.is_board_full(self.board.board):
            self.winner = "Draw"
            self.game_state.set_game_over(True)
        else:
            # Đổi lượt chơi
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.timer.switch_turn(self.current_player)

    def run(self):
        """
        Vòng lặp chính của game session.
        """
        # Thiết lập session, nếu người dùng hủy, self.running sẽ là False
        if not self._setup_session():
            return

        while self.running:
            self._check_time_up()
            self._handle_events()
            self._update_cursor()
            self._draw_screen()
            self._handle_game_over()

            pygame.display.flip()

