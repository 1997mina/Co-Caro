class PieceDragHandler:
    def __init__(self, x_img, o_img, initial_x_center, initial_o_center, drop_target1, drop_target2):
        self.x_img = x_img
        self.o_img = o_img
        self.initial_x_center = initial_x_center
        self.initial_o_center = initial_o_center
        self.drop_target1 = drop_target1
        self.drop_target2 = drop_target2

        self.x_drag_rect = x_img.get_rect(center=initial_x_center)
        self.o_drag_rect = o_img.get_rect(center=initial_o_center)

        self.dragging = False
        self.dragged_piece = None  # 'X' or 'O'
        self.offset_x, self.offset_y = 0, 0

        self.player1_piece = None
        self.player2_piece = None

    def handle_mouse_down(self, event_pos):
        if self.x_drag_rect.collidepoint(event_pos) and not self.dragging and not ('X' in [self.player1_piece, self.player2_piece]):
            self.dragging = True
            self.dragged_piece = 'X'
            self.offset_x, self.offset_y = event_pos[0] - self.x_drag_rect.x, event_pos[1] - self.x_drag_rect.y
        elif self.o_drag_rect.collidepoint(event_pos) and not self.dragging and not ('O' in [self.player1_piece, self.player2_piece]):
            self.dragging = True
            self.dragged_piece = 'O'
            self.offset_x, self.offset_y = event_pos[0] - self.o_drag_rect.x, event_pos[1] - self.o_drag_rect.y

    def handle_mouse_motion(self, event_pos):
        if self.dragging:
            if self.dragged_piece == 'X':
                self.x_drag_rect.x = event_pos[0] - self.offset_x
                self.x_drag_rect.y = event_pos[1] - self.offset_y
            elif self.dragged_piece == 'O':
                self.o_drag_rect.x = event_pos[0] - self.offset_x
                self.o_drag_rect.y = event_pos[1] - self.offset_y

    def handle_mouse_up(self, event_pos):
        if self.dragging:
            if self.drop_target1.collidepoint(event_pos):
                if self.dragged_piece == 'X':
                    self.player1_piece = 'X'
                    self.player2_piece = 'O' if self.player2_piece != 'O' else None
                elif self.dragged_piece == 'O':
                    self.player1_piece = 'O'
                    self.player2_piece = 'X' if self.player2_piece != 'X' else None
            elif self.drop_target2.collidepoint(event_pos):
                if self.dragged_piece == 'X':
                    self.player2_piece = 'X'
                    self.player1_piece = 'O' if self.player1_piece != 'O' else None
                elif self.dragged_piece == 'O':
                    self.player2_piece = 'O'
                    self.player1_piece = 'X' if self.player1_piece != 'X' else None
            else: # Reset position if not dropped on a valid target
                if self.dragged_piece == 'X':
                    self.x_drag_rect.center = self.initial_x_center
                elif self.dragged_piece == 'O':
                    self.o_drag_rect.center = self.initial_o_center
            self.dragging = False
            self.dragged_piece = None