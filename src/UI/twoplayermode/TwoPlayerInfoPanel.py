from ui.general.InfoPanel import InfoPanel

class TwoPlayerInfoPanel(InfoPanel):
    """
    Lớp này chịu trách nhiệm vẽ bảng thông tin người chơi ở bên cạnh màn hình.
    """
    def __init__(self, rect, player_names, x_img, o_img):
        super().__init__(rect, player_names, x_img, o_img)

    def draw(self, screen, current_player, remaining_times, time_mode, paused):
        # Gọi phương thức draw của lớp cha
        super().draw(screen, current_player, remaining_times, time_mode, paused)