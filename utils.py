import pygame

_image_cache = {}
_spritesheet_cache = {}
_scaled_image_cache = {}


def _display_ready():
    return pygame.display.get_init() and pygame.display.get_surface() is not None


def _cache_scale(scale):
    return round(float(scale), 4)


def _scaled_size(image, scale):
    return (
        max(1, round(image.get_width() * scale)),
        max(1, round(image.get_height() * scale)),
    )


def _convert_for_display(image):
    if not _display_ready():
        return image
    try:
        return image.convert_alpha()
    except pygame.error:
        return image


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
    scale_key = _cache_scale(scale)
    if scale_key == 1:
        return image
    cache_key = (id(image), scale_key)
    scaled = _scaled_image_cache.get(cache_key)
    if scaled is None:
        scaled = pygame.transform.scale(image, _scaled_size(image, scale_key))
        _scaled_image_cache[cache_key] = scaled
    return scaled


def transform_image(image, scale=1, flip_x=False):
    scale_key = _cache_scale(scale)
    if scale_key == 1 and not flip_x:
        return image

    cache_key = (id(image), scale_key, flip_x)
    transformed = _scaled_image_cache.get(cache_key)
    if transformed is None:
        transformed = scale_image(image, scale_key)
        if flip_x:
            transformed = pygame.transform.flip(transformed, True, False)
        _scaled_image_cache[cache_key] = transformed
    return transformed

def loadimg(path, scale):
    cache_key = (path, _cache_scale(scale), _display_ready())
    cached = _image_cache.get(cache_key)
    if cached is not None:
        return cached

    img = pygame.image.load(path)
    if scale != 1:
        img = pygame.transform.scale(img, _scaled_size(img, scale))
    img = _convert_for_display(img)
    _image_cache[cache_key] = img
    return img
def loadimages(path, scale, countimg):
    cache_key = (path, _cache_scale(scale), countimg, _display_ready())
    cached = _spritesheet_cache.get(cache_key)
    if cached is not None:
        return cached

    spritesheet = loadimg(path, scale)
    images = []
    w = spritesheet.get_width() // countimg
    h = spritesheet.get_height()
    for i in range(0, countimg):
        image = spritesheet.subsurface(i * w, 0, w, h)
        images.append(image)
    _spritesheet_cache[cache_key] = images
    return images
def loadimagesgrid(path, scale, countimgX, countimgY):
    spritesheet = loadimg(path, scale)
    images = []
    w = spritesheet.get_width() // countimgX
    h = spritesheet.get_height() // countimgY
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
