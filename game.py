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
warriors = []
mlevel.load(warriors)
while True:
    fps.tick(60)
    screen.fill('black')
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
        if i.type == pygame.MOUSEBUTTONUP and i.button == 2:
            moving = False
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
    for i in warriors:
        i.render(screen, mlevel.xcamera, mlevel.ycamera, mlevel.scale)
        i.update()

    pygame.display.update()
