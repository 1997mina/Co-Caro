import pygame
import os

class GameBoard:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.board = [['' for _ in range(width)] for _ in range(height)]

        # Tải và thay đổi kích thước hình ảnh
        self.padding = int(self.cell_size * 0.1)
        img_size = self.cell_size - (2 * self.padding)

        # Giả sử bạn có thư mục 'img' với file 'x.png' và 'o.png'
        self.x_img = pygame.transform.scale(pygame.image.load(os.path.join('img', 'X.png')), (img_size, img_size))
        self.o_img = pygame.transform.scale(pygame.image.load(os.path.join('img', 'O.png')), (img_size, img_size))

    def mark_square(self, row, col, player):
        """Đánh dấu một ô trên bàn cờ nếu ô đó còn trống."""
        if self.board[row][col] == '':
            self.board[row][col] = player
            return True
        return False

    def reset(self):
        """Xóa toàn bộ bàn cờ để bắt đầu ván mới."""
        self.board = [['' for _ in range(self.width)] for _ in range(self.height)]

    def draw(self, screen):
        """Vẽ bàn cờ và các quân cờ X, O."""
        for row in range(self.height):
            for col in range(self.width):
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1) # Draw cell borders

                # Tính toán vị trí để vẽ ảnh (có padding)
                img_pos_x = col * self.cell_size + self.padding
                img_pos_y = row * self.cell_size + self.padding

                # Vẽ quân cờ nếu ô đã được đánh dấu
                player = self.board[row][col]
                if player == 'X':
                    screen.blit(self.x_img, (img_pos_x, img_pos_y))
                elif player == 'O':
                    screen.blit(self.o_img, (img_pos_x, img_pos_y))
