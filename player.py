import animation
import pygame
import utils

class Warrior:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 'idle'
        self.select = False
        self.speed = 4
        self.targetx = 100
        self.targety = 100
        self.mustmove = False
        self.dir = 'r'
        self.selectimg = utils.loadimg('images/UI Elements/UI Elements/Cursors/Cursor_04.png', 1)
        self.anims:dict[str, animation.Animation] = {}
        self.anims['attack1'] = animation.Animation('images/Units/Blue Units/Warrior/Warrior_Attack1.png', 1, 4, 6, True)
        self.anims['idle'] = animation.Animation('images/Units/Blue Units/Warrior/Warrior_Idle.png', 1, 8, 6, True)
        self.anims['run'] = animation.Animation('images/Units/Blue Units/Warrior/Warrior_Run.png', 1, 6, 6, True)
    def render(self, screen, xcamera, ycamera, scale=1):
        screen_x = (self.x - xcamera) * scale
        screen_y = (self.y - ycamera) * scale
        self.hitbox:pygame.Rect = self.anims[self.state].render(screen, screen_x, screen_y, self.dir, scale)
        hitbox_shrink = round(90 * scale)
        self.hitbox = self.hitbox.inflate(-hitbox_shrink, -hitbox_shrink)
        whit = self.gethitbox()
        #whit = whit.inflate(-95, -95)
        pygame.draw.rect(screen, 'red', [whit.x - xcamera * scale, whit.y - ycamera * scale, whit.width, whit.height], 2)
        if self.select == True:
            screen.blit(self.selectimg, [self.hitbox.centerx - self.selectimg.get_width() / 2, self.hitbox.centery - self.selectimg.get_height() / 2])
    def update(self, click):
        self.anims[self.state].update()
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if click == True:
                if self.select == True:
                    self.select = False
                else:
                    self.select = True
        if self.mustmove == True:
            self.state = 'run'
        else:
            self.state = 'idle'
    def moving(self, mlevel, units):
        distance, dx, dy, size = self.get_distance_to_target()
        if abs(distance) < 1:
            self.mustmove = False
            return
        speed = min(self.speed, distance / 5)
        self.x += dx * speed / distance
        if dx > 0:
            self.collisionx(mlevel, 'r')
            self.dir = 'r'
        else:
            self.collisionx(mlevel, 'l')
            self.dir = 'l'
        self.y += dy * speed / distance
        if dy > 0:
            self.collisiony(mlevel, 'd')
        else:
            self.collisiony(mlevel, 'u')
        self.collision_units(units, mlevel)
        if abs(self.targetx - self.x - size[0] / 2) < 10 and abs(self.targety - self.y - size[1] / 2) < 10:
            self.mustmove = False
    def get_distance_to_target(self):
        size = self.anims[self.state].what_size_of_img()
        x = self.x + size[0] / 2
        y = self.y + size[1] / 2
        dx = self.targetx - x
        dy = self.targety - y
        return (dx * dx + dy * dy)**.5, dx, dy, size
    def gethitbox(self):
        return pygame.rect.Rect([self.x, self.y], self.anims[self.state].what_size_of_img()).inflate(-140, -140)
    def collisionx(self, mlevel, dir):
        self.hitbox = self.gethitbox()
        for i in mlevel.borders:
            hit = pygame.rect.Rect(i[0], i[1], 64, 64)
            if hit.colliderect(self.hitbox):
                self.mustmove = False
                if dir == 'r':
                    self.hitbox.right = hit.left
                if dir == 'l':
                    self.hitbox.left = hit.right
        self.x = self.hitbox.x - 70

    def collisiony(self, mlevel, dir):
        self.hitbox = self.gethitbox()
        for i in mlevel.borders:
            hit = pygame.rect.Rect(i[0], i[1], 64, 64)
            if hit.colliderect(self.hitbox):
                self.mustmove = False
                if dir == 'u':
                    self.hitbox.top = hit.bottom
                if dir == 'd':
                    self.hitbox.bottom = hit.top
        self.y = self.hitbox.y - 70
    def collision_units(self, units, mlevel):
        hitboxunit = self.gethitbox()
        for i in units:
            if i != self:
                if hitboxunit.colliderect(i.gethitbox()):
                    #self.mustmove = False
                    dx = self.x - i.x
                    dy = self.y - i.y
                    distance = (dx * dx + dy * dy)**.5
                    if abs(distance) < 1:
                        return
                    self.x += dx / distance * 5
                    self.y += dy / distance * 5
                    if dx > 0:
                        self.collisionx(mlevel, 'r')
                    else:
                        self.collisionx(mlevel, 'l')
                    if dy > 0:
                        self.collisiony(mlevel, 'd')
                    else:
                        self.collisiony(mlevel, 'u')
class Pawn(Warrior):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.anims['idle'] = animation.Animation('images/Units/Blue Units/Pawn/Pawn_Idle.png', 1, 8, 6, True)
        self.anims['run'] = animation.Animation('images/Units/Blue Units/Pawn/Pawn_Run.png', 1, 6, 6, True)
        self.anims['interact_axe'] = animation.Animation('images/Units/Blue Units/Pawn/Pawn_Interact Axe.png', 1, 6, 6, True)
        self.mission = None
        self.target_obj = None
    def render(self, screen, xcamera, ycamera, scale=1):
        return super().render(screen, xcamera, ycamera, scale)
    def update(self, click):
        super().update(click)
        if self.mission == 'felling tree' and self.get_distance_to_target()[0] < 10:
            self.state = 'interact_axe'
            if self.anims['interact_axe'].index == 3:
                self.target_obj.hp -= 0.1
            if self.targetx > self.hitbox.centerx:
                self.dir = 'r'
            else:
                self.dir = 'l'
        else:
            pass

