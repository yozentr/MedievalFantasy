import pygame
import animation
import level
import pytmx
import decorations
import utils
import player
import random

pygame.init()
info = pygame.display.Info()
screen = pygame.display.set_mode([info.current_w, info.current_h])
fps = pygame.time.Clock()
mlevel = level.Level()
lastcamx = mlevel.xcamera
lastcamy = mlevel.ycamera
moving = False
units = []
decorations.loadtrees()
cursor_arrow = utils.loadimg('images/UI Elements/UI Elements/Cursors/Cursor_01.png', 1)
cursor_axe = utils.loadimg('images/UI Elements/UI Elements/Icons/Icon_02.png', 0.7)
current_cursor = cursor_arrow
hover_state = None

pygame.mouse.set_visible(False)


mlevel.load(units)
def clicknowhere():
    for i in units:
        hitbox = i.gethitbox()
        if hitbox.collidepoint(mpos[0] + mlevel.xcamera, mpos[1] + mlevel.ycamera):
            return False
    return True
def felling_tree_mission(coords, tree):
    for i in units:
        if i.select == True and isinstance(i, player.Pawn):
            i.mission = 'felling tree'
            i.targetx = coords[0]
            i.targety = coords[1]
            i.target_obj = tree
while True:
    fps.tick(60)
    screen.fill('black')
    events = pygame.event.get()
    mpos = pygame.mouse.get_pos()
    click = False
    

    for i in events:
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                quit()
        if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:
            lastcamx = mpos[0]
            lastcamy = mpos[1]
            click = True
            moving = True
            if clicknowhere() == True:
                for j in units:
                    if j.select == True:
                        j.targetx = pygame.mouse.get_pos()[0] + mlevel.xcamera
                        j.targety = pygame.mouse.get_pos()[1] + mlevel.ycamera
                        j.mustmove = True
        if i.type == pygame.MOUSEBUTTONUP and i.button == 1:
            moving = False
            click = False
        if i.type == pygame.MOUSEWHEEL:
            if i.y > 0:
                mlevel.resize_everything(1, mpos)
            elif i.y < 0:
                mlevel.resize_everything(0, mpos)
    if moving == True:
        dx = mpos[0] - lastcamx
        dy = mpos[1] - lastcamy
        mlevel.xcamera -= dx / mlevel.scale
        mlevel.ycamera -= dy / mlevel.scale
        lastcamx = mpos[0]
        lastcamy = mpos[1]
    pressed = pygame.key.get_pressed()
    camera_step = 10 / mlevel.scale
    if pressed[pygame.K_a]:
        mlevel.xcamera -= camera_step
    if pressed[pygame.K_d]:
        mlevel.xcamera += camera_step
    if pressed[pygame.K_s]:
        mlevel.ycamera += camera_step
    if pressed[pygame.K_w]:
        mlevel.ycamera -= camera_step
    mlevel.render(screen)
    for i in units:
        i.render(screen, mlevel.xcamera, mlevel.ycamera, mlevel.scale)
        i.update(click)
        if i.mustmove == True:
            i.moving(mlevel, units)
    hover_state = None
    for i in decorations.trees:
        i.render(screen, mlevel.xcamera, mlevel.ycamera, mlevel.scale)
        if i.get_hitbox().move(-mlevel.xcamera, -mlevel.ycamera).collidepoint(mpos):
            hover_state = 'tree'
            current_cursor = cursor_axe
            if click == True:
                felling_tree_mission(i.get_hitbox().move(random.choice([-50, 50]), -40).midbottom, i)
    if hover_state == None:
        current_cursor = cursor_arrow

    screen.blit(current_cursor, mpos)
    pygame.display.update()
