import pygame
import animation
import level
import pytmx
import decorations
import utils
import player
import random
import inventory
import rightclick

pygame.init()
def selectslot_all():
    for i in units:
        i.select = True
def unselectslot():
    for i in units:
        i.select = False
def selectslot_pawn():
    for i in units:
        if isinstance(i) == player.Pawn:
            i.select = True
def selectslot_warrior():
    for i in units:
        if isinstance(i) == player.Warrior:
            i.select = True
def selectslot():
    global secondmenu
    if secondmenu == None:
        if menu.x < screen.get_width() / 2:
            secondmenu = rightclick.Menu(menu.x + 155, menu.y, ['Unselect','All', 'Warriors', 'Pawns'])
        else:
            secondmenu = rightclick.Menu(menu.x - 155, menu.y, ['Unselect','All', 'Warriors', 'Pawns'])
        secondmenu.button[0].slot = unselectslot
        secondmenu.button[1].slot = selectslot_all
        secondmenu.button[2].slot = selectslot_pawn
        secondmenu.button[3].slot = selectslot_warrior
    else:
        secondmenu = None

info = pygame.display.Info()

screen = pygame.display.set_mode([info.current_w, info.current_h])
fps = pygame.time.Clock()
mlevel = level.Level()
lastcamx = mlevel.xcamera
lastcamy = mlevel.ycamera
moving = False
units = []
enemies = []
decorations.loadtrees()
cursor_arrow = utils.loadimg('images/UI Elements/UI Elements/Cursors/Cursor_01.png', 1)
cursor_axe = utils.loadimg('images/Terrain/Resources/Tools/Tool_02.png', 1)
cursor_hand = utils.loadimg('images/UI Elements/UI Elements/Cursors/Cursor_02.png', 1)
cursor_pickaxe = utils.loadimg('images/Terrain/Resources/Tools/Tool_04.png', 1)
cursor_sword = utils.loadimg('images/Terrain/Resources/Tools/Tool_03.png', 1)
current_cursor = cursor_arrow
hover_state = None
menu = None
secondmenu = None

pygame.mouse.set_visible(False)

mlevel.load(units, enemies)
allunits = units + enemies
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
def mining_stone_mission(coords, stone):
    for i in units:
        if i.select == True and isinstance(i, player.Pawn):
            i.mission = 'mining stone'
            i.targetx = coords[0]
            i.targety = coords[1]
            i.target_obj = stone
def attack_mission(enemy):
    for i in units:
        if i.select == True and isinstance(i, player.Warrior):
            i.mission = 'attack'
            i.target_obj = enemy
            

while True:
    fps.tick(60)
    screen.fill('black')
    events = pygame.event.get()
    mpos = pygame.mouse.get_pos()
    click = False
    c = 0
    for i in events:
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                quit()
        if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:
            lastcamx = mpos[0]
            lastcamy = mpos[1]
            click = True
            moving = True
            if menu != None:
                if menu != None and menu.get_hitbox().collidepoint(mpos):
                    c += 1
                if secondmenu != None and secondmenu.get_hitbox().collidepoint(mpos):
                    c += 1
                if c == 0:
                    menu = None
                    secondmenu = None
            if clicknowhere() == True and c == 0:
                for j in units:
                    if j.select == True:
                        j.targetx = pygame.mouse.get_pos()[0] + mlevel.xcamera
                        j.targety = pygame.mouse.get_pos()[1] + mlevel.ycamera
                        j.mustmove = True
        if i.type == pygame.MOUSEBUTTONDOWN and i.button == 3:
            if menu == None:
                menu = rightclick.Menu(mpos[0], mpos[1], ['Select', 'Build'])
                menu.button[0].slot = selectslot
            else:
                menu = None
                secondmenu = None
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
        menu = None
        secondmenu = None
        mlevel.xcamera -= camera_step
    if pressed[pygame.K_d]:
        menu = None
        secondmenu = None
        mlevel.xcamera += camera_step
    if pressed[pygame.K_s]:
        menu = None
        secondmenu = None
        mlevel.ycamera += camera_step
    if pressed[pygame.K_w]:
        menu = None
        secondmenu = None
        mlevel.ycamera -= camera_step
    mlevel.render(screen)
    for i in units:
        i.render(screen, mlevel.xcamera, mlevel.ycamera, mlevel.scale)
        if c != 0:
            i.update(False)
        else:
            i.update(click)
        if i.mustmove == True:
            i.moving(mlevel, allunits)
    for i in enemies:
        i.render(screen, mlevel.xcamera, mlevel.ycamera, mlevel.scale)
        i.update()
        i.moving(mlevel, allunits)
    hover_state = None
    for i in decorations.trees:
        i.render(screen, mlevel.xcamera, mlevel.ycamera, mlevel.scale)
        if i.get_hitbox().move(-mlevel.xcamera, -mlevel.ycamera).collidepoint(mpos) and i.dead == False:
            hover_state = 'tree'
            current_cursor = cursor_axe
            if click == True:
                felling_tree_mission(i.get_hitbox().move(random.choice([-50, 50]), -40).midbottom, i)
    for i in decorations.stumps:
        i.render(screen, mlevel.xcamera, mlevel.ycamera, mlevel.scale)
    for i in decorations.stones:
        i.render(screen, mlevel.xcamera, mlevel.ycamera)
        if i.get_hitbox().move(-mlevel.xcamera, -mlevel.ycamera).collidepoint(mpos):
            hover_state = 'stone' 
            current_cursor = cursor_pickaxe
            if click == True:
                mining_stone_mission(i.get_hitbox().move(random.choice([-50, 50]), -40).midbottom, i)
    for i in enemies:
        if i.gethitbox().move(-mlevel.xcamera, -mlevel.ycamera).collidepoint(mpos):
            hover_state = 'attack'
            current_cursor = cursor_sword
            if click == True:
                attack_mission(i)
    inventory.render(screen)
    if menu != None:
        menu.render(screen, click)
    if secondmenu != None:
        secondmenu.render(screen, click)
    if hover_state == None:
        current_cursor = cursor_arrow

    screen.blit(current_cursor, mpos)
    pygame.display.update()
