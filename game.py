import pygame
import animation
import level
import pytmx

pygame.init()
info = pygame.display.Info()
screen = pygame.display.set_mode([info.current_w, info.current_h])
fps = pygame.time.Clock()
mlevel = level.Level()
lastcamx = mlevel.xcamera
lastcamy = mlevel.ycamera
moving = False
countwheel = 0
warriors = []
mlevel.load(warriors)
while True:
    fps.tick(60)
    screen.fill('black')
    mlevel.render(screen)
    events = pygame.event.get()
    mpos = pygame.mouse.get_pos()
    for i in events:
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                quit()
        if i.type == pygame.MOUSEBUTTONDOWN and i.button == 2:
            lastcamx = mpos[0]
            lastcamy = mpos[1]
            moving = True
        if i.type == pygame.MOUSEBUTTONUP:
            moving = False
        if i.type == pygame.MOUSEWHEEL:
            if i.y > 0 and countwheel <= 4:
                mlevel.resize_everything(1)
                countwheel += 1
            elif countwheel >= -1 and i.y < 0 : 
                mlevel.resize_everything(0)
                countwheel -= 1
    if moving == True:
        dx = mpos[0] - lastcamx
        dy = mpos[1] - lastcamy
        mlevel.xcamera -= dx
        mlevel.ycamera -= dy
        lastcamx = mpos[0]
        lastcamy = mpos[1]
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a]:
        mlevel.xcamera -= 10
    if pressed[pygame.K_d]:
        mlevel.xcamera += 10
    if pressed[pygame.K_s]:
        mlevel.ycamera += 10
    if pressed[pygame.K_w]:
        mlevel.ycamera -= 10
    for i in warriors:
        i.render(screen, mlevel.xcamera, mlevel.ycamera)
        i.update()

    pygame.display.update()

