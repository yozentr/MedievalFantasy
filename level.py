import utils
import pygame
import pytmx
import player


class Level:
    ZOOM_FACTOR = 1.1
    MIN_ZOOM_LEVEL = -2
    MAX_ZOOM_LEVEL = 5

    def __init__(self):
        self.background = utils.loadimg('images/Maps/World.png', 1)
        self.backgroundorig = self.background
        self.scale = 1.0
        self.zoom_level = 0
        self.xcamera = 0.0
        self.ycamera = 0.0

    def render(self, screen):
        self.clamp_camera(screen.get_size())
        screen.blit(
            self.background,
            [-round(self.xcamera * self.scale), -round(self.ycamera * self.scale)],
        )

    def screen_to_world(self, x, y):
        return x / self.scale + self.xcamera, y / self.scale + self.ycamera

    def world_to_screen(self, x, y):
        return (x - self.xcamera) * self.scale, (y - self.ycamera) * self.scale

    def clamp_camera(self, viewport_size):
        max_x = max(0.0, self.backgroundorig.get_width() - viewport_size[0] / self.scale)
        max_y = max(0.0, self.backgroundorig.get_height() - viewport_size[1] / self.scale)
        self.xcamera = min(max(self.xcamera, 0.0), max_x)
        self.ycamera = min(max(self.ycamera, 0.0), max_y)

    def resize_everything(self, sizing, anchor_pos=None):
        zoom_delta = 1 if sizing == 1 else -1 if sizing == 0 else 0
        target_zoom_level = min(
            max(self.zoom_level + zoom_delta, self.MIN_ZOOM_LEVEL),
            self.MAX_ZOOM_LEVEL,
        )
        if target_zoom_level == self.zoom_level:
            return False

        if anchor_pos is None:
            anchor_pos = (0, 0)
        anchor_world_x, anchor_world_y = self.screen_to_world(*anchor_pos)
        self.zoom_level = target_zoom_level
        self.scale = self.ZOOM_FACTOR ** self.zoom_level
        width = max(1, round(self.backgroundorig.get_width() * self.scale))
        height = max(1, round(self.backgroundorig.get_height() * self.scale))
        self.background = pygame.transform.scale(self.backgroundorig, [width, height])
        self.xcamera = anchor_world_x - anchor_pos[0] / self.scale
        self.ycamera = anchor_world_y - anchor_pos[1] / self.scale
        return True

    def load(self, warriors):
        #print(1)
        data = pytmx.load_pygame('Tiled/World.tmx')
        #print(2)
        for x, y, gid in data.get_layer_by_name('Spawners'):
            if gid != 0:
                warrior = player.Warrior(x * 64, y * 64)
                warriors.append(warrior)
