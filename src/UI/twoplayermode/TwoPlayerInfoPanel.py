from ui.general.InfoPanel import InfoPanel

class TwoPlayerInfoPanel(InfoPanel):
    """
    Lớp này chịu trách nhiệm vẽ bảng thông tin người chơi ở bên cạnh màn hình.
    """
    def __init__(self, rect, player_names, x_img, o_img):
        super().__init__(rect, player_names, x_img, o_img)
        # Xác định các nút sẽ được hiển thị trong chế độ này (không có nút Gợi ý)
        self.buttons_to_layout = [self.pause_button, self.quit_button]

    def draw(self, screen, current_player, remaining_times, time_mode, paused):
        # Gọi phương thức draw của lớp cha, nó sẽ tự động vẽ các nút trong buttons_to_layout
        super().draw(screen, current_player, remaining_times, time_mode, paused)