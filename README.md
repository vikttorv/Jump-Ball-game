# Darky
import pygame
from fileplayer import Player
from platforms import Platform
from pygame import mixer
SIZE = (1300,700)
window = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Super Mario')
screen = pygame.Surface(SIZE)
# Герой
hero = Player(55,55)
left =  False
right = False
up = False

#камера
class Camera:
    def __init__(self,camera_func,width,height):
        self.camera_func =  camera_func
        self.state = pygame.Rect(0,0,width,height)
    def apply(self, target):
        return target.rect.move(self.state.topleft)
    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def camera_func(camera, target_rect):
    l = -target_rect.x + SIZE[0]/2
    t = -target_rect.y + SIZE[1]/2
    w,h = camera.width,camera.height
    l = min(0,l)
    l = max(-(camera.width - SIZE[0]), l)
    t = max(-(camera.height - SIZE[1]), t)
    t = min(0,t)
    return pygame.Rect(l,t,w,h)

# Уровень
level = [
'---------------------------------------------------------------------------------------------------------------------',
'-                                                                                                                   -',
'-                                                                                                                   -',
'-       -                                                     ------------                                          -',
'-                                                                                                                   -',
'------                                                                                                              -',
'-          -      -                                                                              -                  -',
'-                                                                                                                   -',
'-                                                                  -                                                -',
'-          --                                         -                                                             -',
'-                                                                                                                   -',
'-                 -      -                                                    -                                     -',
'-                                                                                                                   -',
'-                                                                                                                   -',
'-                                                                                                                   -',
'-         --                                 -----                                                                  -',
'-                      -                                                                          -                 -',
'-                                                                                                                   -',
'-                                                                    -                                              -',
'-                                             -                                    -                                -',
'-                                                                                                                   -',
'-                   -                                                                                               -',
'-                                                                                                            -      -',
'-                                                               -                                                   -',
'-                                                                                                                   -',
'-           -                                                                                                       -',
'-                                  ---                                                            ----              -',
'-                                                                                                                   -',
'-                                         -    -                --                                                  -',
'-              -                          -    -                                                                    -',
'-                                         -    -                                                                    -',
'-                                                                                                                   -',
'-                                    -             -                                                                -',
'-        -                            -           -                                                                 -',
'-                                      -----------                                                                  -',
'-                                                                                            ---                    -',
'-                                                                                                                   -',
'-                                                                                                                   -',
'-                      ---                                                                                          -',
'-                                             --                                                                    -',
'-                                                                                                                   -',
'-                                                               ---                                                 -',
'-                                      ---                                                            ---           -',
'-                           -                                                                                       -',
'-           -                                  --                                                                   -',
'-                                                                                                                   -',
'-                                                                                                                   -',
'-                                                   --                                                              -',
'-               -                                                                  ----             ---             -',
'-                         ---                    -                                                                  -',
'-                                                                                                                   -',
'-                                           --                     --                                               -',
'-                                                                                                                   -',
'-                                                                                                                   -',
'-                                   ---                                                        ---                  -',
'-               ---                                                                                                 -',
'-                           --                           ---                                                        -',
'-     -                                                                                                             -',
'-                                                                           ---                                     -',
'-           -                  ---                                                                                  -',
'-                                                                                                         ---       -',
'-                                                                                                                   -',
'-                                                                                                                   -',
'---------------------------------------------------------------------------------------------------------------------']

sprite_group = pygame.sprite.Group()
sprite_group.add(hero)
platforms = []
total_level_weight = len(level[0]) * 40
total_level_height = len(level) * 40
camera = Camera(camera_func, total_level_weight, total_level_height)

# Платформа
x = 0
y = 0
for row in level:
    for col in row:
        if col == '-':
            pl = Platform(x,y)
            sprite_group.add(pl)
            platforms.append(pl)
        x += 40
    y += 40
    x = 0
pygame.mixer.pre_init(44100,-16,1,512)
pygame.mixer.init()
sound = pygame.mixer.Sound('Angel.ogx')
sound.play(-1)
# Таймер
timer = pygame.time.Clock()

# Большая туша цикла
done  = True
while done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                left = True
            if e.key == pygame.K_RIGHT:
                right = True
            if e.key == pygame.K_UP:
                up = True
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT:
                left = False
            if e.key == pygame.K_RIGHT:
                right = False
            if e.key == pygame.K_UP:
                up = False
    screen.fill((10,120,10))
    hero.update(left,up,right,platforms)
    camera.update(hero)
    for e in sprite_group:
        screen.blit(e.image, camera.apply(e))
    window.blit(screen,(0,0))
    pygame.display.flip()
    timer.tick(60)
