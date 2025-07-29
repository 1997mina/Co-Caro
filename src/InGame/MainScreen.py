import pygame
import os
from InGame.PlayerInfoPanel import PlayerInfoPanel

class GameBoard:
    def __init__(self, board_width_cells, board_height_cells, cell_size, screen_width, screen_height, player_names):
        self.board_width_cells = board_width_cells
        self.board_height_cells = board_height_cells
        self.cell_size = cell_size
        self.board = [['' for _ in range(board_width_cells)] for _ in range(board_height_cells)]

        # Tải và thay đổi kích thước hình ảnh
        self.padding = int(self.cell_size * 0.1)
        img_size = self.cell_size - (2 * self.padding)

        # Giả sử bạn có thư mục 'img' với file 'x.png' và 'o.png'
        self.x_img = pygame.image.load(os.path.join('img', 'X.png')).convert_alpha()
        self.o_img = pygame.image.load(os.path.join('img', 'O.png')).convert_alpha()
        self.x_img_scaled = pygame.transform.scale(self.x_img, (img_size, img_size))
        self.o_img_scaled = pygame.transform.scale(self.o_img, (img_size, img_size))

        # Kích thước của bảng game (pixel)
        self.board_pixel_width = self.board_width_cells * self.cell_size
        self.board_pixel_height = self.board_height_cells * self.cell_size

        # Khởi tạo PlayerInfoPanel
        panel_width = screen_width - self.board_pixel_width
        panel_rect = pygame.Rect(0, 0, panel_width, screen_height)
        self.player_info_panel = PlayerInfoPanel(panel_rect, player_names, self.x_img, self.o_img)

    def mark_square(self, row, col, player):
        """Đánh dấu một ô trên bàn cờ nếu ô đó còn trống."""
        if self.board[row][col] == '':
            self.board[row][col] = player
            return True
        return False

    def reset(self):
        """Xóa toàn bộ bàn cờ để bắt đầu ván mới."""
        self.board = [['' for _ in range(self.board_width_cells)] for _ in range(self.board_height_cells)]

    def draw(self, screen, current_player):
        """Vẽ bàn cờ và các quân cờ X, O."""
        # Vẽ PlayerInfoPanel
        self.player_info_panel.draw(screen, current_player)

        # Vẽ bàn cờ (dịch sang phải panel_width)
        board_offset_x = self.player_info_panel.rect.width
        for row in range(self.board_height_cells):
            for col in range(self.board_width_cells):
                rect = pygame.Rect(board_offset_x + col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1) # Draw cell borders

                # Tính toán vị trí để vẽ ảnh (có padding)
                img_pos_x = board_offset_x + col * self.cell_size + self.padding
                img_pos_y = row * self.cell_size + self.padding

                # Vẽ quân cờ nếu ô đã được đánh dấu
                player = self.board[row][col]
                if player == 'X':
                    screen.blit(self.x_img_scaled, (img_pos_x, img_pos_y))
                elif player == 'O':
                    screen.blit(self.o_img_scaled, (img_pos_x, img_pos_y))
