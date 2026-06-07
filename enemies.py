import pygame
import animation
import utils
import bar
import particle
import constans

class EnemyWarrior:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 'idle'
        self.speed = 4
        self.dir = 'r'
        self.hp = 200
        self.bar = bar.Bar(200)
        self.anims:dict[str, animation.Animation] = {}
        self.anims['attack1'] = animation.Animation('images/Units/Red Units/Warrior/Warrior_Attack1.png', 1, 4, 12, True)
        self.anims['idle'] = animation.Animation('images/Units/Red Units/Warrior/Warrior_Idle.png', 1, 8, 6, True)
        self.anims['run'] = animation.Animation('images/Units/Red Units/Warrior/Warrior_Run.png', 1, 6, 6, True)
    def render(self, screen, xcamera, ycamera, scale):
        screen_x = (self.x - xcamera) * scale
        screen_y = (self.y - ycamera) * scale
        self.hitbox:pygame.Rect = self.anims[self.state].render(screen, screen_x, screen_y, self.dir, scale)
        hitbox_shrink = round(90 * scale)
        self.hitbox = self.hitbox.inflate(-hitbox_shrink, -hitbox_shrink)
        whit = self.gethitbox()
        #whit = whit.inflate(-95, -95)
        if constans.DEBUG_DRAW:
            pygame.draw.rect(screen, 'red', utils.world_rect_to_screen(whit, xcamera, ycamera, scale), 2)
        self.bar.val = self.hp
        if self.hp != self.bar.maxval:
                self.bar.render(screen, self.x, self.y, xcamera, ycamera)

    def update(self, units, mlevel, enemies):
        self.anims[self.state].update()
        self.search_for_aim(units, mlevel)
        if self.anims['attack1'].index == 3 and self.target_obj != None:
                self.target_obj.hp -= 3
                if self.target_obj.hp < 1:
                    self.target_obj = None
                    self.nearest = None
                    self.state = 'idle'
        if self.hp < 1:
            dust = particle.Dust(self.x, self.y, mlevel.xcamera, mlevel.ycamera)
            particle.particles.append(dust)
            enemies.remove(self)
    def gethitbox(self):
        return pygame.rect.Rect([self.x, self.y], self.anims[self.state].what_size_of_img()).inflate(-140, -140)
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
    def moving(self, mlevel, units):
        self.collision_units(units, mlevel)
    def collisionx(self, mlevel, dir):
        self.hitbox = self.gethitbox()
        for hit in mlevel.iter_border_rects_near(self.hitbox):
            if hit.colliderect(self.hitbox):
                self.mustmove = False
                if dir == 'r':
                    self.hitbox.right = hit.left
                if dir == 'l':
                    self.hitbox.left = hit.right
        self.x = self.hitbox.x - 70

    def collisiony(self, mlevel, dir):
        self.hitbox = self.gethitbox()
        for hit in mlevel.iter_border_rects_near(self.hitbox):
            if hit.colliderect(self.hitbox):
                self.mustmove = False
                if dir == 'u':
                    self.hitbox.top = hit.bottom
                if dir == 'd':
                    self.hitbox.bottom = hit.top
        self.y = self.hitbox.y - 70
    def search_for_aim(self, units, mlevel):
        nearest = None
        mindist_sq = None
        for i in units:
            dist_sq = self.get_distance_to_target_sq(i)
            if nearest == None:
                nearest = i
                mindist_sq = dist_sq
            if dist_sq < mindist_sq:
                nearest = i
                mindist_sq = dist_sq
        if mindist_sq == None or mindist_sq > 500 * 500:
            return
        if mindist_sq < 500 * 500 and mindist_sq > 100 * 100:
            self.state = 'run'
            if nearest.x > self.x:
                self.x += 1
                self.dir = 'r'
                self.collisionx(mlevel, self.dir)
            if nearest.x < self.x:
                self.x -= 1
                self.dir = 'l' 
                self.collisionx(mlevel, self.dir)
            if nearest.y > self.y:
                self.y += 1
                self.collisiony(mlevel, self.dir)
            else:
                self.y -= 1
                self.collisiony(mlevel, self.dir)
        else:
            self.state = 'idle'
            self.target_obj = nearest
            if mindist_sq < 100 * 100:
                self.state = 'attack1'
    def get_distance_to_target(self, target):
        return self.get_distance_to_target_sq(target)**.5

    def get_distance_to_target_sq(self, target):
        x = self.x
        y = self.y
        dx = target.x - x
        dy = target.y - y
        return dx * dx + dy * dy
