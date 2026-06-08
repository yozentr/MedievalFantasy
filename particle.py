import pygame
import utils
import animation

particles = []

class Dust:
    def __init__(self, x, y, xcamera, ycamera):
        self.timer = 8 * 12 
        self.x = x + 64
        self.y = y + 64
        self.anim = animation.Animation("images/Particle FX/Dust_01.png", 2, 8, 12, False)
    def render(self, screen, xcamera=0, ycamera=0, scale=1):
        screen_x, screen_y = utils.world_to_screen(self.x, self.y, xcamera, ycamera, scale)
        self.anim.render(screen, screen_x, screen_y, 'r', scale)
        self.timer -= 1
        self.anim.update()
        if self.timer == 0:
            particles.remove(self)
class Arrow:
    def __init__(self, x, y, xcamera, ycamera, targetx, targety):
        self.x = x
        self.y = y
        self.vx = (targetx - x) / 100
        self.vx = (targety - y) / 100
        self.anim = animation.Animation("images/Units/Blue Units/Archer/Arrow.png", 2, 1, 12, False)
    def render(self, screen):
        self.anim.render(screen, self.x, self.y, 'r', 1)
        self.timer -= 1
        self.anim.update()
        if self.timer == 0:
            particles.remove(self)
        self.x += self.vx
        self.y += self.vy
