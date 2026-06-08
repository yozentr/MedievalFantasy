import pygame
import utils
import bar

gridsize = 64
buildings = []
houseimg = utils.loadimg('images/Buildings/Blue Buildings/House2.png', 1)

class House:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 500
        self.bar = bar.Bar(500)
    def render(self, screen, xcamera, ycamera, scale=1):
        self.bar.val = self.hp
        screen_x, screen_y = utils.world_to_screen(self.x, self.y, xcamera, ycamera, scale)
        screen.blit(utils.scale_image(houseimg, scale), (round(screen_x), round(screen_y)))
        if self.hp < self.bar.maxval:
            self.bar.render(screen, self.x, self.y, xcamera, ycamera, scale)
