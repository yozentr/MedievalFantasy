import animation
import pygame
import utils
import bar

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
        self.hp = 200
        self.bar = bar.Bar(200)
        self.dir = 'r'
        self.mission = None
        self.selectimg = utils.loadimg('images/UI Elements/UI Elements/Cursors/Cursor_04.png', 1)
        self.anims:dict[str, animation.Animation] = {}
        self.anims['attack'] = animation.Animation('images/Units/Blue Units/Warrior/Warrior_Attack1.png', 1, 4, 12, True)
        self.anims['idle'] = animation.Animation('images/Units/Blue Units/Warrior/Warrior_Idle.png', 1, 8, 6, True)
        self.anims['run'] = animation.Animation('images/Units/Blue Units/Warrior/Warrior_Run.png', 1, 6, 6, True)
    def render(self, screen, xcamera, ycamera, scale=1):
        screen_x, screen_y = utils.world_to_screen(self.x, self.y, xcamera, ycamera, scale)
        self.hitbox:pygame.Rect = self.anims[self.state].render(screen, screen_x, screen_y, self.dir, scale)
        hitbox_shrink = round(90 * scale)
        self.hitbox = self.hitbox.inflate(-hitbox_shrink, -hitbox_shrink)
        whit = self.gethitbox()
        #whit = whit.inflate(-95, -95)
        pygame.draw.rect(screen, 'red', utils.world_rect_to_screen(whit, xcamera, ycamera, scale), 2)
        if self.select == True:
            screen.blit(self.selectimg, [self.hitbox.centerx - self.selectimg.get_width() / 2, self.hitbox.centery - self.selectimg.get_height() / 2])
        self.bar.val = self.hp
        if self.hp != self.bar.maxval:
                self.bar.render(screen, self.x, self.y, xcamera, ycamera)
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
        
        if self.mission == 'attack' and self.get_distance_to_target()[0] < 10:
            self.state = 'attack'
            if self.anims['attack'].index == 3:
                self.target_obj.hp -= 3
                if self.target_obj.hp < 1:
                    self.mission = None
            if self.targetx > self.hitbox.centerx:
                self.dir = 'r'
            else:
                self.dir = 'l'
        elif self.mission == 'attack':
            self.targetx = self.target_obj.x
            self.targety = self.target_obj.y
            
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
                other_hitbox = i.gethitbox()
                if hitboxunit.colliderect(other_hitbox):
                    overlap = hitboxunit.clip(other_hitbox)
                    if overlap.width <= 0 or overlap.height <= 0:
                        continue

                    if overlap.width < overlap.height:
                        if hitboxunit.centerx < other_hitbox.centerx:
                            self.x -= overlap.width
                            self.collisionx(mlevel, 'l')
                        else:
                            self.x += overlap.width
                            self.collisionx(mlevel, 'r')
                    else:
                        if hitboxunit.centery < other_hitbox.centery:
                            self.y -= overlap.height
                            self.collisiony(mlevel, 'u')
                        else:
                            self.y += overlap.height
                            self.collisiony(mlevel, 'd')

                    hitboxunit = self.gethitbox()
class Pawn(Warrior):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.anims['idle'] = animation.Animation('images/Units/Blue Units/Pawn/Pawn_Idle.png', 1, 8, 6, True)
        self.anims['run'] = animation.Animation('images/Units/Blue Units/Pawn/Pawn_Run.png', 1, 6, 6, True)
        self.anims['interact_axe'] = animation.Animation('images/Units/Blue Units/Pawn/Pawn_Interact Axe.png', 1, 6, 6, True)
        self.anims['hold_wood'] = animation.Animation('images/Units/Blue Units/Pawn/Pawn_Idle Wood.png', 1, 8, 6, True)
        self.anims['interact_pickaxe'] = animation.Animation('images/Units/Blue Units/Pawn/Pawn_Interact Pickaxe.png', 1, 6, 6, True)
        self.mission = None
        self.target_obj = None
        self.hp = 100
        self.bar = bar.Bar(100)
    def render(self, screen, xcamera, ycamera, scale=1):
        return super().render(screen, xcamera, ycamera, scale)
    def update(self, click):
        super().update(click)
        if self.mission == 'felling tree' and self.get_distance_to_target()[0] < 10:
            self.state = 'interact_axe'
            if self.anims['interact_axe'].index == 3:
                self.target_obj.hp -= 5
                if self.target_obj.hp < 1:
                    self.mission = None
            if self.targetx > self.gethitbox().centerx:
                self.dir = 'r'
            else:
                self.dir = 'l'
        else:
            pass
        if self.mission == 'mining stone' and self.get_distance_to_target()[0] < 10:
            self.state = 'interact_pickaxe'
            if self.anims['interact_pickaxe'].index == 3:
                self.target_obj.hp -= 5
                if self.target_obj.hp < 1:
                    self.mission = None
            if self.targetx > self.gethitbox().centerx:
                self.dir = 'r'
            else:
                self.dir = 'l'
        else:
            pass
