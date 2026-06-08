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
import particle
import buildings
Font30 = pygame.font.Font("font BikiniBottom-Regular.otf", 30)

pygame.init()
def selectslot_all():
    for i in units:
        i.select = True
def unselectslot():
    for i in units:
        i.select = False
def selectslot_pawn():
    for i in units:
        if isinstance(i, player.Pawn):
            i.select = True
def selectslot_warrior():
    for i in units:
        if isinstance(i, player.Warrior) and not isinstance(i, player.Pawn) and not isinstance(i, player.Archer):
            i.select = True
def selectslot_archer():
    for i in units:
        if isinstance(i, player.Archer):
            i.select = True
def selectslot():
    global secondmenu
    if secondmenu == None:
        if menu.x < screen.get_width() / 2:
            secondmenu = rightclick.Menu(menu.x + 200, menu.y, ['Unselect','All', 'Warriors', 'Pawns', 'Archers'])
        else:
            secondmenu = rightclick.Menu(menu.x - 200, menu.y, ['Unselect','All', 'Warriors', 'Pawns', 'Archers'])
        secondmenu.button[0].slot = unselectslot
        secondmenu.button[1].slot = selectslot_all
        secondmenu.button[2].slot = selectslot_warrior
        secondmenu.button[3].slot = selectslot_pawn
        secondmenu.button[4].slot = selectslot_archer
    
    else:
        secondmenu = None
def buildslot():
    global buildmode
    if buildmode == True:
        buildmode = False
    else:
        buildmode = True
    
    

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
buildmode = False
buildcost = [
    {'Wood Resource': 6, 'Stone Resource': 1},
    {'Wood Resource': 2, 'Stone Resource': 6},
    {'Wood Resource': 4, 'Stone Resource': 13},
    {'Wood Resource': 3, 'Stone Resource': 0},
    {'Wood Resource': 8, 'Stone Resource': 1},
    {'Wood Resource': 0, 'Stone Resource': 3}
]
buildingsimg = [
    utils.loadimg("images\Buildings\Blue Buildings\Archery.png", 1),
    utils.loadimg("images\Buildings\Blue Buildings\Barracks.png", 1),
    utils.loadimg("images\Buildings\Blue Buildings\Castle.png", 1),
    utils.loadimg("images\Buildings\Blue Buildings\House2.png", 1),
    utils.loadimg("images\Buildings\Blue Buildings\Monastery.png", 1),
    utils.loadimg("images\Buildings\Blue Buildings\Tower.png", 1)
]
buildingsindex = 3

pygame.mouse.set_visible(False)

mlevel.load(units, enemies, buildings.buildings)
def clicknowhere():
    world_mpos = mlevel.screen_to_world(*mpos)
    for group in (units, enemies):
        for i in group:
            hitbox = i.gethitbox()
            if hitbox.collidepoint(world_mpos):
                return False
    return True

def get_interaction_target(obj):
    if hasattr(obj, 'get_interaction_hitbox'):
        return obj.get_interaction_hitbox().center
    return obj.get_hitbox().center

def felling_tree_mission(coords, tree):
    for i in units:
        if i.select == True and isinstance(i, player.Pawn):
            i.mission = 'felling tree'
            i.targetx = coords[0]
            i.targety = coords[1]
            i.target_obj = tree
            i.mustmove = True
def mining_stone_mission(coords, stone):
    for i in units:
        if i.select == True and isinstance(i, player.Pawn):
            i.mission = 'mining stone'
            i.targetx = coords[0]
            i.targety = coords[1]
            i.target_obj = stone
            i.mustmove = True
def attack_mission(enemy):
    for i in units:
        if i.select == True and isinstance(i, player.Warrior):
            i.set_attack_target(enemy)
            

while True:
    fps.tick(60)
    f = fps.get_fps()
    screen.fill('black')
    events = pygame.event.get()
    mpos = pygame.mouse.get_pos()
    click = False
    c = 0
    for i in events:
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                quit()
            if i.key == pygame.K_UP:
                if buildingsindex == len(buildingsimg) - 1:
                    buildingsindex = 0
                else:
                    buildingsindex += 1
            if i.key == pygame.K_DOWN:
                if buildingsindex == 0:
                    buildingsindex = len(buildingsimg) - 1
                else:
                    buildingsindex -= 1
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
                targetx, targety = mlevel.screen_to_world(*mpos)
                for j in units:
                    if j.select == True:
                        j.targetx = targetx
                        j.targety = targety
                        j.mustmove = True
                        j.mission = None
        if i.type == pygame.MOUSEBUTTONDOWN and i.button == 3:
            if menu == None:
                menu = rightclick.Menu(mpos[0], mpos[1], ['Select', 'Build'])
                menu.button[0].slot = selectslot
                menu.button[1].slot = buildslot
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
    if buildmode == True:
        mlevel.background = mlevel.background_net
        buildingsimg[buildingsindex].set_alpha(200)
        if buildcost[buildingsindex]['Wood Resource'] <= inventory.inv['Wood Resource'] and buildcost[buildingsindex]['Stone Resource'] <= inventory.inv['Stone Resource']:

            screen.blit(buildingsimg[buildingsindex], ((mpos[0] + mlevel.xcamera) // buildings.gridsize * buildings.gridsize - mlevel.xcamera, (mpos[1] + mlevel.ycamera) // buildings.gridsize * buildings.gridsize - mlevel.ycamera))
        else:
            #Сделать красным цветом постройку
            buildingsimg[buildingsindex].fill('red', special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(buildingsimg[buildingsindex], ((mpos[0] + mlevel.xcamera) // buildings.gridsize * buildings.gridsize - mlevel.xcamera, (mpos[1] + mlevel.ycamera) // buildings.gridsize * buildings.gridsize - mlevel.ycamera))
        mlevel.background = mlevel.backgroundorig
    for i in units:
        i.render(screen, mlevel.xcamera, mlevel.ycamera, mlevel.scale)
        if c != 0:
            i.update(False, units, mlevel, enemies)
        else:
            i.update(click, units, mlevel, enemies)
        if i.mustmove == True:
            i.moving(mlevel, units + enemies)
    for i in enemies:
        i.render(screen, mlevel.xcamera, mlevel.ycamera, mlevel.scale)
        i.update(units, mlevel, enemies)
        i.moving(mlevel, units + enemies)
    hover_state = None
    world_mpos = mlevel.screen_to_world(*mpos)
    for i in decorations.trees:
        i.render(screen, mlevel.xcamera, mlevel.ycamera, mlevel.scale)
        if i.get_hitbox().collidepoint(world_mpos) and i.dead == False:
            hover_state = 'tree'
            current_cursor = cursor_axe
            if click == True:
                felling_tree_mission(get_interaction_target(i), i)
    for i in decorations.stumps:
        i.render(screen, mlevel.xcamera, mlevel.ycamera, mlevel.scale)
    for i in decorations.stones:
        i.render(screen, mlevel.xcamera, mlevel.ycamera, mlevel.scale)
        if i.get_hitbox().collidepoint(world_mpos):
            hover_state = 'stone' 
            current_cursor = cursor_pickaxe
            if click == True:
                mining_stone_mission(get_interaction_target(i), i)
    for i in enemies:
        if i.gethitbox().collidepoint(world_mpos):
            hover_state = 'attack'
            current_cursor = cursor_sword
            if click == True:
                attack_mission(i)
    for i in buildings.buildings:
        i.render(screen, mlevel.xcamera, mlevel.ycamera, mlevel.scale)
    for i in particle.particles:
        i.render(screen, mlevel.xcamera, mlevel.ycamera, mlevel.scale)
    inventory.render(screen)
    if menu != None:
        menu.render(screen, click)
    if secondmenu != None:
        secondmenu.render(screen, click)
    if hover_state == None:
        current_cursor = cursor_arrow

    screen.blit(current_cursor, mpos)
    fpsimg = Font30.render(str(fps), True, 'white')
    screen.blit(fpsimg, (20, 20))

    pygame.display.update()
