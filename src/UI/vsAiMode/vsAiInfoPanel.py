import pygame

from utils.ResourcePath import resource_path
from ui.general.InfoPanel import InfoPanel

class vsAiInfoPanel(InfoPanel):
    """
    Lớp này chịu trách nhiệm vẽ bảng thông tin người chơi ở bên cạnh màn hình.
    """
    def __init__(self, rect, player_names, x_img, o_img):
        self.rect = rect
        self.player_names = player_names
        
        # Tạo phiên bản ảnh nhỏ hơn cho panel
        super().__init__(rect, player_names, x_img, o_img)
        
        # Tải và thay đổi kích thước ảnh đại diện người chơi
        player_icon_size = 100
        self.ai_icon_img = pygame.image.load(resource_path('img/Computer.png')).convert_alpha() # Ảnh đại diện cho máy
        self.ai_icon_img = pygame.transform.smoothscale(self.ai_icon_img, (player_icon_size, player_icon_size))
        
    def _get_player_icon(self, player_name):
        return self.ai_icon_img if player_name == "Máy tính" else self.player_icon_img

    def _draw_player_avatar(self, screen, player_name, player_area, y_cursor):
        """Ghi đè phương thức vẽ avatar để sử dụng icon AI nếu tên là 'Máy tính'."""
        icon_to_draw = self._get_player_icon(player_name)
        player_icon_rect = icon_to_draw.get_rect(centerx=player_area.centerx, top=y_cursor)
        screen.blit(icon_to_draw, player_icon_rect)
        return player_icon_rect.bottom