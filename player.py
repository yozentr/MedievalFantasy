import animation
import pygame
import utils
import bar
import particle
import constans

class Warrior:
    AUTO_TARGET_DISTANCE = 500

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 'idle'
        self.select = False
        self.speed = 4
        self.targetx = 100
        self.targety = 100
        self.mustmove = False
        self.damage = 3
        self.hp = 200
        self.bar = bar.Bar(200)
        self.dir = 'r'
        self.mission = None
        self.target_obj = None
        self.attackdistance = 100
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
        if constans.DEBUG_DRAW:
            pygame.draw.rect(screen, 'red', utils.world_rect_to_screen(whit, xcamera, ycamera, scale), 2)
        if self.select == True:
            screen.blit(self.selectimg, [self.hitbox.centerx - self.selectimg.get_width() / 2, self.hitbox.centery - self.selectimg.get_height() / 2])
        self.bar.val = self.hp
        if self.hp != self.bar.maxval:
            self.bar.render(screen, self.x, self.y, xcamera, ycamera, scale)
    def update(self, click, units, mlevel, enemies=None):
        self.anims[self.state].update()
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if click == True:
                if self.select == True:
                    self.select = False
                else:
                    self.select = True
        if self.mission == 'attack':
            self.update_attack(enemies or [])
        elif self.mustmove == True:
            self.state = 'run'
        else:
            self.state = 'idle'
        if self.hp < 1:
            dust = particle.Dust(self.x, self.y, mlevel.xcamera, mlevel.ycamera)
            particle.particles.append(dust)
            units.remove(self)
    def update_attack(self, enemies):
        if self.target_obj is None or self.target_obj.hp < 1:
            if not self.acquire_nearest_enemy(enemies):
                self.state = 'idle'
                return

        self.targetx = self.target_obj.x
        self.targety = self.target_obj.y
        if not self.needstop():
            self.state = 'run'
            self.mustmove = True
            return

        self.state = 'attack'
        self.mustmove = False
        if self.anims['attack'].index == 3:
            self.target_obj.hp -= self.damage
            if self.target_obj.hp < 1:
                self.acquire_nearest_enemy(enemies)
        if self.target_obj is not None:
            if self.gethitbox().centerx < self.target_obj.gethitbox().centerx:
                self.dir = 'r'
            else:
                self.dir = 'l'
    def set_attack_target(self, enemy):
        if enemy is not None and enemy is not self.target_obj:
            self.anims['attack'].reset()
        self.target_obj = enemy
        if enemy is None:
            self.mission = None
            self.mustmove = False
            return False

        self.mission = 'attack'
        self.targetx = enemy.x
        self.targety = enemy.y
        self.mustmove = not self.needstop()
        return True
    def acquire_nearest_enemy(self, enemies):
        nearest = None
        nearest_distance_sq = self.AUTO_TARGET_DISTANCE * self.AUTO_TARGET_DISTANCE
        center = self.gethitbox().center
        for enemy in enemies:
            if enemy.hp < 1:
                continue
            enemy_center = enemy.gethitbox().center
            dx = enemy_center[0] - center[0]
            dy = enemy_center[1] - center[1]
            distance_sq = dx * dx + dy * dy
            if distance_sq <= nearest_distance_sq:
                nearest = enemy
                nearest_distance_sq = distance_sq
        return self.set_attack_target(nearest)
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
    def needstop(self):
        if self.gethitbox().inflate(self.attackdistance, self.attackdistance).colliderect(self.target_obj.gethitbox()):
            return True
        else:
            return False
    def gethitbox(self):
        return pygame.rect.Rect([self.x, self.y], self.anims[self.state].what_size_of_img()).inflate(-140, -140)
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
    RESOURCE_INTERACTION_DISTANCE = 12

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
    def update(self, click, units, mlevel, enemies=None):
        super().update(click, units, mlevel, enemies)
        self.interact_with_resource('felling tree', 'interact_axe')
        self.interact_with_resource('mining stone', 'interact_pickaxe')
    def interact_with_resource(self, mission, anim_name):
        if self.mission != mission:
            return
        if self.target_obj is None or self.target_obj.hp < 1:
            self.mission = None
            self.mustmove = False
            return
        target_hitbox = self.get_target_interaction_hitbox()
        if target_hitbox is None:
            return
        if self.distance_to_rect(target_hitbox) > self.RESOURCE_INTERACTION_DISTANCE:
            return

        self.mustmove = False
        self.state = anim_name
        if self.anims[anim_name].index == 3:
            self.target_obj.hp -= 5
            if self.target_obj.hp < 1:
                self.mission = None
        if target_hitbox.centerx > self.gethitbox().centerx:
            self.dir = 'r'
        else:
            self.dir = 'l'

    def get_target_interaction_hitbox(self):
        if self.target_obj is None:
            return None
        if hasattr(self.target_obj, 'get_interaction_hitbox'):
            return self.target_obj.get_interaction_hitbox()
        if hasattr(self.target_obj, 'get_hitbox'):
            return self.target_obj.get_hitbox()
        return None

    def distance_to_rect(self, rect):
        hitbox = self.gethitbox()
        dx = max(rect.left - hitbox.right, hitbox.left - rect.right, 0)
        dy = max(rect.top - hitbox.bottom, hitbox.top - rect.bottom, 0)
        return (dx * dx + dy * dy)**.5
class Archer(Warrior):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.anims['attack'] = animation.Animation('images/Units/Blue Units/Archer/Archer_Shoot.png', 1, 8, 4, True)
        self.anims['idle'] = animation.Animation('images/Units/Blue Units/Archer/Archer_Idle.png', 1, 6, 6, True)
        self.anims['run'] = animation.Animation('images/Units/Blue Units/Archer/Archer_Run.png', 1, 4, 6, True)
        self.attackdistance = 450
        self.hp = 150
        self.bar = bar.Bar(150)
        self.damage = 5
