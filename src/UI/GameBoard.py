import pygame

from utils.ResourcePath import resource_path

class GameBoard:
    def __init__(self, board_rect, board_size, cell_size, screen_height, player_names, info_panel_class, panel_width):
        self.rect = board_rect
        self.board_width_cells = board_size
        self.board_height_cells = board_size
        self.cell_size = cell_size
        self.board = [['' for _ in range(self.board_width_cells)] for _ in range(self.board_height_cells)]

        # Tải và thay đổi kích thước hình ảnh
        self.padding = int(self.cell_size * 0.1)
        img_size = self.cell_size - (2 * self.padding)

        # Tải hình ảnh X và O sử dụng resource_path
        self.x_img = pygame.image.load(resource_path('img/general/X.png')).convert_alpha()
        self.o_img = pygame.image.load(resource_path('img/general/O.png')).convert_alpha()
        self.x_img_scaled = pygame.transform.scale(self.x_img, (img_size, img_size))
        self.o_img_scaled = pygame.transform.scale(self.o_img, (img_size, img_size))

        # Khởi tạo InfoPanel với chiều rộng cố định được truyền vào
        panel_rect = pygame.Rect(0, 0, panel_width, screen_height)
        self.player_info_panel = info_panel_class(panel_rect, player_names, self.x_img, self.o_img)

    def mark_square(self, row, col, player):
        """Đánh dấu một ô trên bàn cờ nếu ô đó còn trống."""
        if self.board[row][col] == '':
            self.board[row][col] = player
            return True
        return False

    def reset(self):
        """Xóa toàn bộ bàn cờ để bắt đầu ván mới."""
        self.board = [['' for _ in range(self.board_width_cells)] for _ in range(self.board_height_cells)]

    def get_cell_from_pos(self, mouse_pos):
        """
        Lấy chỉ số (hàng, cột) của ô cờ từ tọa độ pixel của chuột.
        :param mouse_pos: Tuple (x, y) tọa độ của chuột.
        :return: Tuple (row, col) nếu click nằm trong bàn cờ, ngược lại trả về None.
        """
        # Kiểm tra xem click có nằm trong khu vực của bàn cờ không
        if not self.rect.collidepoint(mouse_pos):
            return None

        # Tính toán tọa độ tương đối của click so với góc trên bên trái của bàn cờ
        relative_x = mouse_pos[0] - self.rect.x
        relative_y = mouse_pos[1] - self.rect.y

        # Chuyển đổi tọa độ tương đối thành chỉ số hàng và cột
        return relative_y // self.cell_size, relative_x // self.cell_size

    def draw(self, screen, current_player, remaining_times, time_mode, paused, winning_cells=None, last_move=None, match_history=None, hint_cell=None, difficulty=None):
        """Vẽ bàn cờ và các quân cờ X, O."""
        # Vẽ PlayerInfoPanel
        self.player_info_panel.draw(screen, current_player, remaining_times, time_mode, paused, winning_cells, last_move, match_history, difficulty)
        
        # Vẽ highlight cho nước đi gần nhất (vẽ nền trước)
        if last_move:
            r, c = last_move
            highlight_rect = pygame.Rect(self.rect.x + c * self.cell_size, self.rect.y + r * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(screen, (180, 180, 180), highlight_rect) # Màu xám đậm hơn

        # Vẽ highlight cho ô được gợi ý (vẽ nền trước)
        if hint_cell:
            r, c = hint_cell
            # Tạo một surface bán trong suốt để vẽ highlight
            hint_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            hint_surface.fill((0, 255, 0, 120))  # Màu xanh lá, 120/255 độ trong suốt
            screen.blit(hint_surface, (self.rect.x + c * self.cell_size, self.rect.y + r * self.cell_size))

        for row in range(self.board_height_cells):
            for col in range(self.board_width_cells):
                rect = pygame.Rect(self.rect.x + col * self.cell_size, self.rect.y + row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1) # Draw cell borders

                # Tính toán vị trí để vẽ ảnh (có padding)
                img_pos_x = self.rect.x + col * self.cell_size + self.padding
                img_pos_y = self.rect.y + row * self.cell_size + self.padding

                # Vẽ quân cờ nếu ô đã được đánh dấu
                player = self.board[row][col]
                if player == 'X':
                    screen.blit(self.x_img_scaled, (img_pos_x, img_pos_y))
                elif player == 'O':
                    screen.blit(self.o_img_scaled, (img_pos_x, img_pos_y))

        # Vẽ highlight cho các ô thắng cuộc
        if winning_cells:
            # Tạo một surface bán trong suốt để vẽ highlight
            highlight_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            highlight_surface.fill((255, 255, 0, 100))  # Màu vàng, 100/255 độ trong suốt

            for r, c in winning_cells:
                highlight_rect = pygame.Rect(self.rect.x + c * self.cell_size, self.rect.y + r * self.cell_size, self.cell_size, self.cell_size)
                screen.blit(highlight_surface, highlight_rect.topleft)

            pygame.time.wait(1000) # Tạm dừng 1 giây trước khi hiển thị màn hình kết thúc