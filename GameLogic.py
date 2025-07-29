class GameLogic:
    def __init__(self, width, height, win_length=5):
        """
        Khởi tạo logic game.
        :param width: Chiều rộng bàn cờ
        :param height: Chiều cao bàn cờ
        :param win_length: Số quân cờ liên tiếp để thắng (mặc định là 5)
        """
        self.width = width
        self.height = height
        self.win_length = win_length

    def check_win(self, board, player, row, col):
        """
        Kiểm tra xem người chơi `player` có thắng sau khi đánh vào (row, col) không.
        """
        if self._check_direction(board, player, row, col, 0, 1):  # Ngang
            return True
        if self._check_direction(board, player, row, col, 1, 0):  # Dọc
            return True
        if self._check_direction(board, player, row, col, 1, 1):  # Chéo chính ( \ )
            return True
        if self._check_direction(board, player, row, col, 1, -1): # Chéo phụ ( / )
            return True
        return False

    def _check_direction(self, board, player, row, col, dr, dc):
        """Kiểm tra một hướng cụ thể (dr, dc) từ vị trí (row, col)."""
        count = 1
        # Đếm theo hướng (dr, dc)
        r, c = row + dr, col + dc
        while 0 <= r < self.height and 0 <= c < self.width and board[r][c] == player:
            count += 1
            r, c = r + dr, c + dc

        # Đếm theo hướng ngược lại (-dr, -dc)
        r, c = row - dr, col - dc
        while 0 <= r < self.height and 0 <= c < self.width and board[r][c] == player:
            count += 1
            r, c = r - dr, c - dc
        
        return count >= self.win_length

    def is_board_full(self, board):
        """Kiểm tra xem bàn cờ đã đầy chưa (hòa)."""
        for r in range(self.height):
            for c in range(self.width):
                if board[r][c] == '':
                    return False
        return True