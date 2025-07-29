import pygame
import os
from GameLogic import GameLogic
from EnterNameDialog import get_player_names

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

if __name__ == '__main__':
    pygame.init()

    # Screen dimensions
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Cờ Caro")

    # --- Màn hình nhập tên ---
    player1_name, player2_name = get_player_names(screen)

    # Board dimensions
    cell_size = 40
    board_width = screen_width // cell_size
    board_height = screen_height // cell_size
    board = GameBoard(board_width, board_height, cell_size)

    # Khởi tạo logic game
    WIN_LENGTH = 5
    game_logic = GameLogic(board_width, board_height, WIN_LENGTH)

    # Các biến trạng thái game
    current_player = 'X'
    game_over = False
    winner = None
    player_names = {'X': player1_name, 'O': player2_name}

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Chỉ xử lý click chuột khi game chưa kết thúc
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // cell_size
                clicked_col = mouseX // cell_size

                # Nếu ô hợp lệ và còn trống, đánh dấu và đổi lượt
                if board.mark_square(clicked_row, clicked_col, current_player):
                    # Kiểm tra thắng
                    if game_logic.check_win(board.board, current_player, clicked_row, clicked_col):
                        winner = current_player
                        game_over = True
                    # Kiểm tra hòa
                    elif game_logic.is_board_full(board.board):
                        winner = "Draw"
                        game_over = True
                    else:
                        # Đổi lượt chơi
                        current_player = 'O' if current_player == 'X' else 'X'

        screen.fill((255, 255, 255))  # Fill background white
        board.draw(screen)

        # Hiển thị thông báo khi game kết thúc
        if game_over:
            font = pygame.font.SysFont("Times New Roman", 74, bold=True)
            if winner == "Draw":
                text = font.render("Hòa!", True, (255, 0, 0))
            else:
                winner_name = player_names.get(winner, "Unknown")
                text = font.render(f"{winner_name} thắng!", True, (255, 0, 0))
            
            text_rect = text.get_rect(center=(screen_width/2, screen_height/2))
            screen.blit(text, text_rect)

        pygame.display.flip()

    pygame.quit()
