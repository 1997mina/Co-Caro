import pygame

class TimerManager:
    """
    Lớp quản lý bộ đếm thời gian cho cả ván đấu.
    Hỗ trợ chế độ "theo lượt" (turn_based) và "tổng thời gian" (total_time).
    """
    def __init__(self, time_limit, mode, ai_player=None):
        """
        Khởi tạo bộ đếm.
        :param time_limit: Giới hạn thời gian (giây). Có thể là None.
        :param mode: Chế độ chơi ("turn_based", "total_time", hoặc None để không giới hạn).
        :param ai_player: Quân cờ của AI ('X' hoặc 'O'), nếu có. AI sẽ không bị giới hạn thời gian.
        """
        self.ai_player = ai_player
        self.mode = mode
        if mode is None:
            # Chế độ không giới hạn thời gian
            self.turn_time_limit = float('inf')
            self.total_times = {'X': float('inf'), 'O': float('inf')}
        else:
            self.turn_time_limit = time_limit if mode == "turn_based" else float('inf')
            self.total_times = {'X': time_limit, 'O': time_limit}

        self.current_player = None
        self.turn_start_time = 0
        self.paused = False
        self.pause_start_time = 0

    def switch_turn(self, player):
        """Chuyển lượt và cập nhật thời gian."""
        now = pygame.time.get_ticks()
        if self.current_player and self.mode == "total_time":
            elapsed_seconds = (now - self.turn_start_time) / 1000
            self.total_times[self.current_player] -= elapsed_seconds
        
        self.current_player = player
        self.turn_start_time = now

    def pause(self):
        """Tạm dừng bộ đếm thời gian."""
        if not self.paused:
            self.paused = True
            self.pause_start_time = pygame.time.get_ticks()

    def resume(self):
        """Tiếp tục bộ đếm thời gian sau khi tạm dừng."""
        if self.paused:
            self.paused = False
            pause_duration = pygame.time.get_ticks() - self.pause_start_time
            # Bù lại thời gian đã tạm dừng bằng cách đẩy mốc thời gian bắt đầu về phía trước
            self.turn_start_time += pause_duration

    def get_remaining_time(self, player):
        """
        Lấy thời gian còn lại cho một người chơi cụ thể.
        :return: Thời gian còn lại (giây).
        """
        if player == self.ai_player:
            return float('inf')

        if self.paused: # Nếu đang tạm dừng, trả về thời gian tại thời điểm tạm dừng
            return self.get_time_at_tick(self.pause_start_time, player)
        if self.mode == "turn_based":
            if player == self.current_player:
                elapsed_seconds = (pygame.time.get_ticks() - self.turn_start_time) / 1000
                return max(0, self.turn_time_limit - elapsed_seconds)
            return self.turn_time_limit # Thời gian của người chơi không trong lượt
        
        # Chế độ total_time
        remaining = self.total_times[player]
        if player == self.current_player:
            elapsed_seconds = (pygame.time.get_ticks() - self.turn_start_time) / 1000
            remaining -= elapsed_seconds
        return max(0, remaining)

    def get_time_at_tick(self, tick, player):
        """Tính toán thời gian còn lại tại một mốc tick cụ thể (dùng cho lúc tạm dừng)."""
        if player == self.ai_player:
            return float('inf')

        if self.mode == "turn_based":
            if player == self.current_player:
                elapsed_seconds = (tick - self.turn_start_time) / 1000
                return max(0, self.turn_time_limit - elapsed_seconds)
            return self.turn_time_limit
        
        remaining = self.total_times[player]
        if player == self.current_player:
            elapsed_seconds = (tick - self.turn_start_time) / 1000
            remaining -= elapsed_seconds
        return max(0, remaining)

    def is_time_up(self):
        """Kiểm tra xem người chơi hiện tại đã hết giờ chưa."""
        if self.current_player == self.ai_player:
            return False # AI không bao giờ hết giờ
        return self.get_remaining_time(self.current_player) <= 0
