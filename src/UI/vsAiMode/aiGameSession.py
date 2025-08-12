import pygame
import threading

from logic.aiLogic import AIPlayer
from manager.TimerManager import TimerManager
from ui.EndScreen import show_quit_confirmation_dialog
from ui.general.GameSession import GameSession
from ui.vsAiMode.vsAiSetting import get_ai_game_settings
from ui.vsAiMode.vsAiInfoPanel import vsAiInfoPanel

class AIGameSession(GameSession):
    """
    Lớp quản lý phiên chơi game với AI, kế thừa từ GameSession.
    Xử lý các logic đặc thù như lượt đi của AI, gợi ý, và màn hình cài đặt.
    """
    def __init__(self, screen):
        super().__init__(screen)
        # Các thuộc tính đặc thù cho AI session
        self.ai_player = None
        self.human_player_char = None
        self.ai_player_char = None
        self.difficulty = None

        # Quản lý luồng của AI
        self.ai_is_thinking = False
        self.ai_thread = None
        self.ai_move_result = None

        # Quản lý gợi ý
        self.hint_cell = None
        self.hint_used_this_round = False

    def _setup_session(self):
        """
        Hiển thị màn hình cài đặt cho chế độ AI, khởi tạo các thành phần.
        """
        game_settings = get_ai_game_settings(self.screen)
        if game_settings is None:
            self.running = False
            return False

        player_name_input, self.human_player_char, first_turn, self.difficulty = game_settings
        self.ai_player_char = 'O' if self.human_player_char == 'X' else 'X'

        player_name = player_name_input.strip() or "Người chơi"
        ai_name = "Máy tính"

        player_names = {self.human_player_char: player_name, self.ai_player_char: ai_name}
        first_turn_char = self.human_player_char if first_turn == 'player' else self.ai_player_char

        # Khởi tạo AI
        self.ai_player = AIPlayer(ai_symbol=self.ai_player_char, human_symbol=self.human_player_char)
        self.ai_player.set_difficulty(self.difficulty)

        # Gọi phương thức khởi tạo của lớp cha
        super()._initialize_components(
            player_names=player_names,
            time_mode="turn_based",
            time_limit=25,
            first_turn_char=first_turn_char,
            info_panel_class=vsAiInfoPanel
        )
        return True

    def _initialize_timer(self):
        """Ghi đè để Timer không tính giờ cho AI."""
        self.timer = TimerManager(self.time_limit, self.time_mode, ai_player=self.ai_player_char)
        self.timer.switch_turn(self.current_player)

    def _check_ai_move(self):
        """Kiểm tra và xử lý nếu AI đã tính toán xong nước đi."""
        if self.ai_is_thinking and self.ai_move_result is not None:
            row, col = self.ai_move_result
            self.board.mark_square(row, col, self.current_player)
            self._post_move_processing(row, col)

            # Reset trạng thái AI
            self.ai_is_thinking = False
            self.ai_move_result = None

    def _handle_player_turn(self, event):
        """Xử lý lượt đi cho cả người chơi và AI."""
        # Xử lý click nút Thoát trên InfoPanel (chức năng tương tự phím ESC)
        if self.board.player_info_panel.quit_button.handle_event(event):
            if show_quit_confirmation_dialog(self.screen, self.board_rect):
                self.running = False
            return
        # --- Lượt đi của AI ---
        if self.game_state.is_playing() and self.current_player == self.ai_player_char and not self.ai_is_thinking:
            self.ai_is_thinking = True
            self.game_logic.board = [row[:] for row in self.board.board]
            is_first_move = not any(any(row) for row in self.game_logic.board)

            def run_ai_calculation():
                self.ai_move_result = self.ai_player.find_best_move(self.game_logic, is_first_move)

            self.ai_thread = threading.Thread(target=run_ai_calculation)
            self.ai_thread.start()

        # --- Lượt đi của người chơi ---
        if self.game_state.is_playing() and self.current_player == self.human_player_char:
            # Xử lý click nút Gợi ý
            if self.board.player_info_panel.hint_button.handle_event(event):
                self.hint_used_this_round = True
                temp_ai = AIPlayer(ai_symbol=self.human_player_char, human_symbol=self.ai_player_char)
                temp_ai.set_difficulty(self.difficulty)
                self.game_logic.board = [row[:] for row in self.board.board]
                is_first_move = not any(any(row) for row in self.game_logic.board)
                self.hint_cell = temp_ai.find_best_move(self.game_logic, is_first_move)
                return

            # Xử lý click lên bàn cờ
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseX, mouseY = event.pos
                if self.board_rect.collidepoint(mouseX, mouseY):
                    clicked_row = mouseY // self.cell_size
                    clicked_col = (mouseX - self.board_rect.left) // self.cell_size
                    if self.board.mark_square(clicked_row, clicked_col, self.current_player):
                        self.hint_cell = None  # Xóa gợi ý sau khi người chơi đi
                        self._post_move_processing(clicked_row, clicked_col)

    def _update_cursor(self):
        """Ghi đè để xử lý con trỏ khi AI đang suy nghĩ."""
        super()._update_cursor()
        if self.ai_is_thinking:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_WAIT)

    def _draw_screen(self):
        """Ghi đè để vẽ thêm các yếu tố của AI (gợi ý, độ khó)."""
        self.screen.fill((255, 255, 255))
        remaining_times = {'X': self.timer.get_remaining_time('X'), 'O': self.timer.get_remaining_time('O')}

        # Cập nhật trạng thái nút Gợi ý
        is_hint_available = self.game_state.is_playing() and self.current_player == self.human_player_char and not self.hint_used_this_round
        self.board.player_info_panel.hint_button.is_enabled = is_hint_available

        self.board.draw(self.screen, self.current_player,
                        remaining_times, self.time_mode, self.game_state.is_paused(),
                        self.winning_cells, self.last_move, self.match_history,
                        self.hint_cell, self.difficulty) # Thêm tham số cho AI

        self.game_state.draw_overlay()

    def _reset_for_new_round(self):
        """Ghi đè để reset thêm các trạng thái của AI."""
        super()._reset_for_new_round()
        self.hint_cell = None
        self.hint_used_this_round = False
        self.ai_is_thinking = False
        self.ai_move_result = None
        if self.ai_thread and self.ai_thread.is_alive():
            # Đây là một tình huống khó xử lý, trong khuôn khổ hiện tại,
            # ta chỉ đơn giản bỏ qua kết quả của luồng cũ.
            pass

    def _handle_events(self):
        """Ghi đè để ngăn chặn một số hành động khi AI đang suy nghĩ."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                exit()

            # Ngăn các sự kiện khác nếu AI đang suy nghĩ
            if self.ai_is_thinking:
                continue

            if self.game_state.handle_event(event, self.timer, self.board):
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not self.game_state.game_over:
                    if show_quit_confirmation_dialog(self.screen, self.board_rect):
                        self.running = False
                    continue

            self._handle_player_turn(event)

    def run(self):
        """
        Ghi đè vòng lặp chính để kiểm tra nước đi của AI mỗi vòng.
        """
        if not self._setup_session():
            return

        while self.running:
            self._check_ai_move() # Kiểm tra kết quả từ luồng AI
            self._check_time_up()
            self._handle_events()
            self._update_cursor()
            self._draw_screen()
            self._handle_game_over()

            pygame.display.flip()