import random
import math

class AIPlayer:
    """
    Lớp chứa logic để máy tính (AI) tìm ra nước đi tốt nhất.
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
        self.WIN_LENGTH = win_length # Số quân cờ liên tiếp để thắng
        self.difficulty = None # 'easy', 'medium', 'hard'

        # Bảng điểm cho các thế cờ
        self.SCORE_PATTERNS = {
            # Điểm cho các chuỗi của AI
            'AI': {
                5: 100000000, # 5 quân -> Thắng chắc
                4: 100000, # 4 quân
                3: 1000, # 3 quân
                2: 10, # 2 quân
                1: 1 # 1 quân
            },
            # Điểm cho các chuỗi của người chơi (để chặn)
            5: 10000000, # 5 quân -> Thắng chắc
            4: 50000,    # 4 quân
            3: 200,      # 3 quân
            2: 10,       # 2 quân
            1: 1         # 1 quân
        }

    def set_difficulty(self, difficulty):
        """Đặt độ khó cho AI."""
        self.difficulty = difficulty
        self.SEARCH_DEPTH = 1 # Giữ nguyên độ sâu tìm kiếm là 1 cho mọi cấp độ

        if difficulty == 'easy':
            self.MAX_MOVES_TO_CONSIDER = 8  # Chỉ xét 8 nước đi tiềm năng nhất
            self.blunder_chance = 0.35      # 35% cơ hội mắc lỗi (chọn nước ngẫu nhiên)
        elif difficulty == 'medium':
            self.MAX_MOVES_TO_CONSIDER = 15 # Xét 15 nước
            self.blunder_chance = 0.10      # 10% cơ hội mắc lỗi
        elif difficulty == 'hard':
            self.MAX_MOVES_TO_CONSIDER = 30 # Xét 30 nước
            self.blunder_chance = 0         # 0% cơ hội mắc lỗi, luôn chọn nước tốt nhất

    def find_best_move(self, board_logic, is_first_move=False):
        """
        Tìm và trả về tọa độ (hàng, cột) của nước đi tốt nhất.
        Sử dụng Minimax với cắt tỉa Alpha-Beta.
        Args:
            time_limit (int): Thời gian tối đa (giây) cho phép AI suy nghĩ.
        Returns:
            tuple: Tọa độ (hàng, cột) của nước đi tốt nhất, hoặc None nếu không tìm thấy.
        """
        # Nếu là nước đi đầu tiên, đặt ở gần trung tâm để có khởi đầu tốt
        if is_first_move:
            center_r, center_c = board_logic.height // 2, board_logic.width // 2
            return (center_r, center_c)

        possible_moves = self._get_possible_moves(board_logic)
        if not possible_moves:
            return None

        # --- Tối ưu hóa: Sắp xếp nước đi (Move Ordering) ---
        # 1. Đánh giá sơ bộ và lưu điểm cho mỗi nước đi
        scored_moves = []
        for move in possible_moves:
            r, c = move
            board_logic.board[r][c] = self.AI_SYMBOL
            # Sử dụng _evaluate_board để có điểm số heuristic nhanh
            score = self._evaluate_board(board_logic)
            board_logic.board[r][c] = '' # Hoàn tác
            scored_moves.append((score, move))

        # 2. Sắp xếp các nước đi từ tốt nhất đến tệ nhất dựa trên điểm sơ bộ
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        # Giới hạn số lượng nước đi cần xem xét để tối ưu hóa
        sorted_moves = [move for score, move in scored_moves][:self.MAX_MOVES_TO_CONSIDER]
        # ----------------------------------------------------

        best_score = -float('inf')
        best_move = None
        top_moves = []

        # 3. Chạy Minimax trên danh sách đã được sắp xếp và giới hạn
        for move in sorted_moves:
            r, c = move
            board_logic.board[r][c] = self.AI_SYMBOL
            # Gọi minimax với độ sâu đã được cấu hình
            score = self._minimax(board_logic, self.SEARCH_DEPTH, -math.inf, math.inf, False)
            board_logic.board[r][c] = '' # Hoàn tác nước đi

            if score > best_score:
                best_score = score
                top_moves = [move] # Bắt đầu lại danh sách các nước đi tốt nhất
            elif score == best_score: # Nếu có cùng điểm số, thêm vào danh sách
                top_moves.append(move)

        # Chọn ngẫu nhiên từ các nước đi tốt nhất nếu có nhiều hơn một
        if top_moves:
            best_move = random.choice(top_moves)
        
        # --- Logic mắc lỗi (Blunder) dựa trên độ khó ---
        # Nếu một số ngẫu nhiên nhỏ hơn tỷ lệ mắc lỗi, AI sẽ chọn một nước đi ngẫu nhiên thay vì nước tốt nhất.
        if random.random() < self.blunder_chance and possible_moves:
            print(f"AI ({self.difficulty}): Oops! Making a random move.")
            return random.choice(possible_moves)
        else:
            # Nếu không mắc lỗi, trả về nước đi tốt nhất đã tìm thấy.
            # Nếu không tìm được (ví dụ: hết giờ), trả về nước đi đầu tiên trong danh sách đã sắp xếp.
            return best_move or (sorted_moves[0] if sorted_moves else None)
        
    def _minimax(self, board_logic, depth, alpha, beta, is_maximizing_player):
        """Thuật toán Minimax với cắt tỉa Alpha-Beta."""
        if depth == 0 or board_logic.check_win_from_any_position(self.AI_SYMBOL) or board_logic.check_win_from_any_position(self.HUMAN_SYMBOL):
            return self._evaluate_board(board_logic)

        possible_moves = self._get_possible_moves(board_logic)
        if not possible_moves: # Bàn cờ đầy
            return 0

        if is_maximizing_player: # Lượt của AI (Max)
            max_eval = -math.inf
            for move in possible_moves:
                r, c = move
                board_logic.board[r][c] = self.AI_SYMBOL
                evaluation = self._minimax(board_logic, depth - 1, alpha, beta, False)
                board_logic.board[r][c] = ''
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break # Cắt tỉa Beta
            return max_eval
        else: # Lượt của người chơi (Min)
            min_eval = math.inf
            for move in possible_moves:
                r, c = move
                board_logic.board[r][c] = self.HUMAN_SYMBOL
                evaluation = self._minimax(board_logic, depth - 1, alpha, beta, True)
                board_logic.board[r][c] = ''
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break # Cắt tỉa Alpha
            return min_eval

    def _evaluate_window(self, window):
        """
        Đánh giá một "cửa sổ" (một đoạn 5 ô) và cho điểm.
        Điểm dương cho AI, điểm âm cho người chơi.
        """
        score = 0
        ai_count = window.count(self.AI_SYMBOL)
        human_count = window.count(self.HUMAN_SYMBOL)

        # Nếu cửa sổ có cả quân của AI và người chơi -> không có tiềm năng -> 0 điểm
        if ai_count > 0 and human_count > 0:
            return 0

        if ai_count > 0: # Cửa sổ tấn công của AI (AI đang xây dựng chuỗi)
            score = self.SCORE_PATTERNS['AI'].get(ai_count, 0)
        elif human_count > 0: # Cửa sổ phòng thủ (chặn người chơi)
            # Điểm phòng thủ thường được ưu tiên hơn một chút so với tấn công của AI để đảm bảo chặn
            score = -self.SCORE_PATTERNS.get(human_count, 0) * 1.1

        return score

    def _evaluate_board(self, board_logic):
        """
        Đánh giá toàn bộ bàn cờ một cách hiệu quả.
        Điểm dương là lợi thế cho AI, điểm âm là lợi thế cho người chơi.
        """
        total_score = 0
        board = board_logic.board
        height, width = board_logic.height, board_logic.width

        # Duyệt qua tất cả các cửa sổ có thể có trên bàn cờ
        for r in range(board_logic.height):
            for c in range(board_logic.width):
                # Cửa sổ ngang
                if c <= width - self.WIN_LENGTH:
                    window = [board[r][c+i] for i in range(self.WIN_LENGTH)]
                    total_score += self._evaluate_window(window)
                # Cửa sổ dọc
                if r <= height - self.WIN_LENGTH:
                    window = [board[r+i][c] for i in range(self.WIN_LENGTH)]
                    total_score += self._evaluate_window(window)
                # Cửa sổ chéo xuôi (\)
                if r <= height - self.WIN_LENGTH and c <= width - self.WIN_LENGTH:
                    window = [board[r+i][c+i] for i in range(self.WIN_LENGTH)]
                    total_score += self._evaluate_window(window)
                # Cửa sổ chéo ngược (/)
                if r <= height - self.WIN_LENGTH and c >= self.WIN_LENGTH - 1:
                    window = [board[r+i][c-i] for i in range(self.WIN_LENGTH)]
                    total_score += self._evaluate_window(window)
        return total_score

    def _get_possible_moves(self, board_logic):
        """
        Lấy danh sách các nước đi hợp lệ.
        Tối ưu: chỉ xem xét các ô trống gần các quân cờ đã có.
        """
        possible_moves = []
        for r in range(board_logic.height):
            for c in range(board_logic.width):
                if board_logic.board[r][c] == '':
                    # Chỉ xét các ô có lân cận đã được đánh
                    if board_logic.has_neighbor(r, c):
                        possible_moves.append((r, c))
        return possible_moves if possible_moves else board_logic.get_empty_cells()
