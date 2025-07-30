class BoardLogic:
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
        Nếu thắng, trả về danh sách tọa độ của các ô thắng.
        Nếu không, trả về None.
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)] # Ngang, Dọc, Chéo chính, Chéo phụ
        for dr, dc in directions:
            winning_line = self._check_direction(board, player, row, col, dr, dc)
            if winning_line:
                return winning_line
        return None

    def _check_direction(self, board, player, row, col, dr, dc):
        """
        Kiểm tra một hướng cụ thể (dr, dc) từ vị trí (row, col).
        Nếu đủ số quân cờ để thắng, trả về danh sách tọa độ các ô.
        Nếu không, trả về None.
        """
        line_cells = [(row, col)]
        
        # Đếm theo hướng (dr, dc)
        r, c = row + dr, col + dc
        while 0 <= r < self.height and 0 <= c < self.width and board[r][c] == player:
            line_cells.append((r, c))
            r, c = r + dr, c + dc

        # Đếm theo hướng ngược lại (-dr, -dc)
        r, c = row - dr, col - dc
        while 0 <= r < self.height and 0 <= c < self.width and board[r][c] == player:
            line_cells.append((r, c))
            r, c = r - dr, c - dc
        
        if len(line_cells) >= self.win_length:
            return line_cells
        return None

    def is_board_full(self, board):
        """Kiểm tra xem bàn cờ đã đầy chưa (hòa)."""
        for r in range(self.height):
            for c in range(self.width):
                if board[r][c] == '':
                    return False
        return True