class AIPlayer:
    """
    Lớp chứa logic để máy tính (AI) tìm ra nước đi tốt nhất.
    Sử dụng thuật toán heuristic để đánh giá và chọn nước đi.
    """
    def __init__(self, ai_symbol, human_symbol, win_length=5):
        """
        Khởi tạo AI.
        Args:
            ai_symbol (str): Ký hiệu của AI (ví dụ: 'O').
            human_symbol (str): Ký hiệu của người chơi (ví dụ: 'X').
            win_length (int): Số quân cờ liên tiếp để thắng.
        """
        self.AI_SYMBOL = ai_symbol
        self.HUMAN_SYMBOL = human_symbol
        self.WIN_LENGTH = win_length
        # Bảng điểm cho các thế cờ
        self.SCORE_PATTERNS = {
            'FIVE': 10000000,  # 5 quân liên tiếp -> Thắng
            'LIVE_FOUR': 50000,    # 4 quân không bị chặn 2 đầu
            'DEAD_FOUR': 400,      # 4 quân bị chặn 1 đầu
            'LIVE_THREE': 200,     # 3 quân không bị chặn 2 đầu
            'DEAD_THREE': 50,      # 3 quân bị chặn 1 đầu
            'LIVE_TWO': 10,        # 2 quân không bị chặn 2 đầu
            'DEAD_TWO': 5,         # 2 quân bị chặn 1 đầu
        }

    def find_best_move(self, board_logic):
        """
        Tìm và trả về tọa độ (hàng, cột) của nước đi tốt nhất.
        Args:
            board_logic (BoardLogic): Đối tượng logic của bàn cờ, chứa trạng thái bàn cờ.
        Returns:
            tuple: Tọa độ (hàng, cột) của nước đi tốt nhất, hoặc None nếu không tìm thấy.
        """
        best_score = -float('inf')
        best_move = None
        
        # Duyệt qua tất cả các ô trên bàn cờ
        for r in range(board_logic.height):
            for c in range(board_logic.width):
                # Nếu ô trống, xem xét đây là một nước đi tiềm năng
                if board_logic.board[r][c] == '':
                    # Tính điểm tấn công (nếu AI đi vào ô này)
                    attack_score = self._calculate_score(board_logic, r, c, self.AI_SYMBOL)
                    # Tính điểm phòng thủ (nếu người chơi đi vào ô này)
                    defense_score = self._calculate_score(board_logic, r, c, self.HUMAN_SYMBOL)
                    
                    # Điểm tổng của nước đi là tổng của tấn công và phòng thủ
                    # AI ưu tiên chặn nước đi mạnh của đối thủ cũng như tạo nước đi mạnh cho mình
                    current_score = attack_score + defense_score

                    if current_score > best_score:
                        best_score = current_score
                        best_move = (r, c)
                        
        return best_move

    def _calculate_score(self, board_logic, r, c, player_symbol):
        """
        Tính toán điểm số cho một nước đi tiềm năng tại (r, c) cho một người chơi.
        Điểm số được tính bằng cách đánh giá các đường ngang, dọc, chéo đi qua ô này.
        """
        total_score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Ngang, Dọc, Chéo chính, Chéo phụ

        for dr, dc in directions:
            line = []
            # Lấy một đoạn các ô cờ xung quanh (r, c) theo một hướng
            for i in range(-(self.WIN_LENGTH - 1), self.WIN_LENGTH):
                nr, nc = r + i * dr, c + i * dc
                if 0 <= nr < board_logic.height and 0 <= nc < board_logic.width:
                    line.append(board_logic.board[nr][nc])
                else:
                    line.append('WALL') # 'WALL' đại diện cho việc ra ngoài bàn cờ
            
            # Đánh giá đoạn vừa lấy được
            total_score += self._evaluate_line(line, player_symbol)
            
        return total_score

    def _evaluate_line(self, line, player_symbol):
        """
        Đánh giá một đường (line) các ô cờ và trả về điểm số dựa trên các mẫu (pattern).
        """
        score = 0
        opponent_symbol = self.HUMAN_SYMBOL if player_symbol == self.AI_SYMBOL else self.AI_SYMBOL

        # Duyệt qua các cửa sổ có kích thước WIN_LENGTH (5) và WIN_LENGTH + 1 (6)
        # Cửa sổ 6 ô để xác định "LIVE" (không bị chặn 2 đầu)
        # Cửa sổ 5 ô để xác định "DEAD" (bị chặn 1 đầu)

        # --- Đánh giá các mẫu 4 quân ---
        # Live Four: _XXXX_
        for i in range(len(line) - 5):
            window = line[i:i+6]
            if window.count(player_symbol) == 4 and window.count('') == 2:
                 if window[0] == '' and window[5] == '':
                    score += self.SCORE_PATTERNS['LIVE_FOUR']

        # --- Đánh giá các mẫu 3 quân ---
        # Live Three: _XXX_
        for i in range(len(line) - 4):
            window = line[i:i+5]
            if window.count(player_symbol) == 3 and window.count('') == 2:
                if window[0] == '' and window[4] == '':
                    score += self.SCORE_PATTERNS['LIVE_THREE']

        # --- Đánh giá các mẫu 2 quân ---
        # Live Two: _XX_
        for i in range(len(line) - 3):
            window = line[i:i+4]
            if window.count(player_symbol) == 2 and window.count('') == 2:
                if window[0] == '' and window[3] == '':
                    score += self.SCORE_PATTERNS['LIVE_TWO']

        # --- Đánh giá các mẫu bị chặn 1 đầu ---
        for i in range(len(line) - 4):
            window = line[i:i+5]
            # Dead Four: OXXXX_ hoặc _XXXXO
            if window.count(player_symbol) == 4 and window.count('') == 1:
                score += self.SCORE_PATTERNS['DEAD_FOUR']
            # Dead Three: OXXX_ hoặc _XXXO
            if window.count(player_symbol) == 3 and window.count('') == 1 and window.count(opponent_symbol) == 1:
                score += self.SCORE_PATTERNS['DEAD_THREE']
            # Dead Two: OXX_ hoặc _XXO
            if window.count(player_symbol) == 2 and window.count('') == 1 and window.count(opponent_symbol) == 1:
                score += self.SCORE_PATTERNS['DEAD_TWO']

        # --- Đánh giá trường hợp thắng ---
        for i in range(len(line) - (self.WIN_LENGTH - 1)):
            window = line[i:i+self.WIN_LENGTH]
            if window.count(player_symbol) == self.WIN_LENGTH:
                score += self.SCORE_PATTERNS['FIVE']

        return score
