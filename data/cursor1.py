import os, pygame, random
 
 
def load_image(name, colorkey=None, ):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)  
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image 
pygame.init()
size = width, height = 400, 300
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("сursor.png")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
sprite.rect.x = 0
sprite.rect.y = 0
pygame.mouse.set_visible(False)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            pos_x, pos_y = event.pos
            sprite.rect.topleft = pos_x, pos_y
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)        
    pygame.display.flip()
pygame.quit()
