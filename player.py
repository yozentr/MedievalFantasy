import animation
import pygame
import utils

class Warrior:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 'idle'
        self.select = False
        self.selectimg = utils.loadimg('images/UI Elements/UI Elements/Cursors/Cursor_04.png', 1)
        self.anims:dict[str, animation.Animation] = {}
        self.anims['attack1'] = animation.Animation('images/Units/Blue Units/Warrior/Warrior_Attack1.png', 1, 4, 6, True)
        self.anims['idle'] = animation.Animation('images/Units/Blue Units/Warrior/Warrior_Idle.png', 1, 8, 6, True)
    def render(self, screen, xcamera, ycamera, scale=1):
        screen_x = (self.x - xcamera) * scale
        screen_y = (self.y - ycamera) * scale
        self.hitbox:pygame.Rect = self.anims[self.state].render(screen, screen_x, screen_y, 'right', scale)
        hitbox_shrink = round(90 * scale)
        self.hitbox = self.hitbox.inflate(-hitbox_shrink, -hitbox_shrink)
        if self.select == True:
            screen.blit(self.selectimg, [self.hitbox.centerx - self.selectimg.get_width() / 2, self.hitbox.centery - self.selectimg.get_height() / 2])
    def update(self):
        self.anims[self.state].update()
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                if self.select == True:
                    self.select = False
                else:
                    self.select = True
