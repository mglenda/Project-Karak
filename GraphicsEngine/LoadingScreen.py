from GraphicsEngine.Screen import Screen
import os
import pygame


class LoadingScreen:
    def __init__(self, screen: Screen) -> None:
        self.screen = screen
        self.last_percent = None

    def draw(self, current: int, total: int, label: str):
        progress = 0 if total == 0 else current / total
        percent = int(progress * 100)
        if self.last_percent == percent and current not in (0, total):
            return
        self.last_percent = percent

        pygame.event.pump()
        surface = self.screen.get_surface()
        w = self.screen.get_w()
        h = self.screen.get_h()

        surface.fill((10, 10, 12))

        title_font = pygame.font.Font(None, 54)
        detail_font = pygame.font.Font(None, 28)
        title = title_font.render("Loading Karak", True, (235, 235, 235))
        detail = detail_font.render(f"{percent}%  {os.path.basename(label)}", True, (190, 190, 190))

        bar_w = w * 0.46
        bar_h = 18
        bar_x = (w - bar_w) / 2
        bar_y = h * 0.56

        surface.blit(title, ((w - title.get_width()) / 2, h * 0.42))
        pygame.draw.rect(surface, (55, 55, 60), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
        pygame.draw.rect(surface, (215, 180, 80), (bar_x, bar_y, bar_w * progress, bar_h), border_radius=4)
        surface.blit(detail, ((w - detail.get_width()) / 2, bar_y + 36))
        pygame.display.update()
