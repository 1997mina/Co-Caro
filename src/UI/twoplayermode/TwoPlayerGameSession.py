import pygame

from ui.general.GameSession import GameSession
from ui.EndGameScreen import show_quit_confirmation_dialog
from ui.twoplayermode.TwoPlayerSetting import get_two_player_setting
from ui.twoplayermode.TwoPlayerInfoPanel import TwoPlayerInfoPanel

class TwoPlayerGameSession(GameSession):
    """
    Lớp quản lý phiên chơi game cho 2 người, kế thừa từ GameSession.
    """
    def __init__(self, screen):
        super().__init__(screen)

    def _setup_session(self):
        """
        Hiển thị màn hình cài đặt cho chế độ 2 người chơi, khởi tạo các thành phần.
        """
        player_data = get_two_player_setting(self.screen)
        if player_data is None:
            self.running = False
            return False

        p1_name_input, p2_name_input, p1_piece, time_mode, time_limit, first_turn = player_data

        p2_piece = 'O' if p1_piece == 'X' else 'X'
        player_names = {p1_piece: p1_name_input, p2_piece: p2_name_input}

        first_turn_char = p1_piece if first_turn == 'player1' else p2_piece

        # Gọi phương thức khởi tạo của lớp cha với các cài đặt đã thu thập
        super()._initialize_components(
            player_names=player_names,
            time_mode=time_mode,
            time_limit=time_limit,
            first_turn_char=first_turn_char,
            info_panel_class=TwoPlayerInfoPanel
        )
        return True

    def _handle_player_turn(self, event):
        """
        Xử lý lượt đi của người chơi.
        """
        if not self.game_state.is_playing():
            return

        # Xử lý click chuột để đi cờ
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseX, mouseY = event.pos
            if self.board.rect.collidepoint(mouseX, mouseY): # Sử dụng self.board.rect thay vì self.board_rect
                cell = self.board.get_cell_from_pos((mouseX, mouseY))
                if cell:
                    clicked_row, clicked_col = cell

                    if self.board.mark_square(clicked_row, clicked_col, self.current_player):
                        # Gọi phương thức xử lý chung sau khi có nước đi hợp lệ
                        self._post_move_processing(clicked_row, clicked_col)