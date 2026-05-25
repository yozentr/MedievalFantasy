import pygame

def world_to_screen(x, y, xcamera, ycamera, scale=1):
    return (x - xcamera) * scale, (y - ycamera) * scale

def world_rect_to_screen(rect, xcamera, ycamera, scale=1):
    x, y = world_to_screen(rect.x, rect.y, xcamera, ycamera, scale)
    return pygame.Rect(
        round(x),
        round(y),
        max(1, round(rect.width * scale)),
        max(1, round(rect.height * scale)),
    )

def scale_image(image, scale):
    if scale == 1:
        return image
    return pygame.transform.scale(image, [
        max(1, round(image.get_width() * scale)),
        max(1, round(image.get_height() * scale)),
    ])

def loadimg(path, scale):
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, [img.get_width() * scale, img.get_height() * scale])
    return img
def loadimages(path, scale, countimg):
    spritesheet = loadimg(path, scale)
    images = []
    w = spritesheet.get_width() / countimg
    for i in range(0, countimg):
        image = spritesheet.subsurface(i * w, 0, w, spritesheet.get_height())
        images.append(image)
    return images
def loadimagesgrid(path, scale, countimgX, countimgY):
    spritesheet = loadimg(path, scale)
    images = []
    w = spritesheet.get_width() / countimgX
    h = spritesheet.get_height() / countimgY
    for i in range(0, countimgX):
        for j in range(0, countimgY):
            image = spritesheet.subsurface(i * w, j * h, w, h)
            images.append(image)
    return images
def glueimagesgrid(path, scale, countimgX, countimgY):
    sprites = loadimagesgrid(path, scale, countimgX, countimgY)
    sprites2 = []
    for i in sprites:
        sprites2.append(i.subsurface(i.get_bounding_rect()))
    w = sprites[0].get_width() * countimgX
    h = sprites[1].get_height() * countimgY
    surface = pygame.Surface((w, h))
    x = 0
    y = 0
    for i in range(0, countimgX):
        for j in range(0, countimgY):
            img = sprites2[i * countimgY + j]
            surface.blit(img, (x, y))
            y += img.get_height()
        y = 0
        x += img.get_width()
    return surface.subsurface(surface.get_bounding_rect())
