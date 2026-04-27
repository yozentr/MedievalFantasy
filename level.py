import utils
import pygame
import pytmx
import player
import math


class Level:
    ZOOM_FACTOR = 1.1
    MIN_ZOOM_LEVEL = -2
    MAX_ZOOM_LEVEL = 5

    def __init__(self):
        self.backgroundorig = utils.loadimg('images/Maps/World.png', 1).convert_alpha()
        self.background = self.backgroundorig
        self.scale = 1.0
        self.zoom_level = 0
        self.xcamera = 3000
        self.ycamera = 3000
        self.load_borders()

    def load_borders(self):
        map = pytmx.load_pygame('Tiled/World.tmx') 
        self.borders = {}
        for i in map.get_layer_by_name('Borders'):
            if i[2] != 0:
                x = i[0] * 64 * self.scale
                y = i[1] * 64 * self.scale
                self.borders[(x, y)] = None



    def render(self, screen):
        viewport_size = screen.get_size()
        self.clamp_camera(viewport_size)

        map_width = self.backgroundorig.get_width()
        map_height = self.backgroundorig.get_height()
        visible_width = min(map_width, max(1, math.ceil(viewport_size[0] / self.scale) + 2))
        visible_height = min(map_height, max(1, math.ceil(viewport_size[1] / self.scale) + 2))
        source_x = min(max(int(self.xcamera), 0), max(0, map_width - visible_width))
        source_y = min(max(int(self.ycamera), 0), max(0, map_height - visible_height))
        offset_x = -round((self.xcamera - source_x) * self.scale)
        offset_y = -round((self.ycamera - source_y) * self.scale)
        visible_rect = pygame.Rect(source_x, source_y, visible_width, visible_height)
        visible_part = self.backgroundorig.subsurface(visible_rect)

        if self.scale == 1:
            screen.blit(visible_part, [offset_x, offset_y])
            for i in self.borders:
                pygame.draw.rect(screen, 'red', (i[0] - self.xcamera * self.scale, i[1] - self.ycamera * self.scale, 64 * self.scale, 64 * self.scale))
            return
            

        scaled_size = [
            max(1, round(visible_width * self.scale)),
            max(1, round(visible_height * self.scale)),
        ]
        scaled_visible_part = pygame.transform.scale(visible_part, scaled_size)
        screen.blit(scaled_visible_part, [offset_x, offset_y])
        


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
        self.xcamera = anchor_world_x - anchor_pos[0] / self.scale
        self.ycamera = anchor_world_y - anchor_pos[1] / self.scale
        return True

    def load(self, warriors):
        #print(1)
        data = pytmx.load_pygame('Tiled/World.tmx')
        #print(2)
        for x, y, gid in data.get_layer_by_name('Warrior'):
            if gid != 0:
                warrior = player.Warrior(x * 64, (y - 2) * 64)
                warriors.append(warrior)
        for x, y, gid in data.get_layer_by_name('Pawn'):
            if gid != 0:
                pawn = player.Pawn(x * 64, (y - 2) * 64)
                warriors.append(pawn)