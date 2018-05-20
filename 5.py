import pygame
from fileplayer import Player
from pygame import mixer
from platforms import Platform, BlockDie_1, BlockDie_2, BlockDie_3, Umnov, Autsave, End

# Создание окна.
SIZE = (1300,700)
window = pygame.display.set_mode(SIZE)

# Подпись на окне вверху.
pygame.display.set_caption('Super Mario. Score = 0')

# Создание экрана.
screen = pygame.Surface(SIZE)

# Создание героя.
hero = Player(55,55)
left =  False
right = False
up = False

# Функция для создания камеры.
class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func =  camera_func
        # Создание атрибута класса камера - прямоугольника всего уровня.
        self.state = pygame.Rect(0, 0, width, height)
    # Прикрипление всех объектов уровня обратно к нему после смещения.
    def apply(self, target):
        return target.rect.move(self.state.topleft)
    # Обновление координат камеры для отслеживания местоположения героя.
    def update(self, target):
        self.state = self.camera_func(self.state, target.rect) 

# Функция для фокусировки камеры на герое.
def camera_func(camera, target_rect):
    # Нахождение координат камеры в с.о. героя по координатам героя в с.о. камеры.
    l = -target_rect.x + SIZE[0]/2
    t = -target_rect.y + SIZE[1]/2
    # Геометрические размеры камеры.
    w,h = camera.width,camera.height
    # Предотвращение выхода окна камеры за пределы уровня.
    l = min(0,l)
    l = max(-(camera.width - SIZE[0]), l)
    t = max(-(camera.height - SIZE[1]), t)
    t = min(0,t)
    # Возвращение прямоугольника с обновленными координатами.
    return pygame.Rect(l, t, w, h) 

# Создание уровня.
level = [
'---------------------------------------------------------------------------------------------------------------------',
'-                                                     ->                                                            -',
'-              Y                                      ->                   <--------------------------------------- -',
'-                                                     --  --------------------                                    - -',
'-    x     x   x   x   x        x                     -                                                           - -',
'------------------------------------------            - -        O                                                - -',
'->                                                    -                             -     -   -  -                - -',
'->                                                    -   -    -            -   -                    -            - -',
'->                                                    -             -   -                               -         - -',
'->               xxx        x                         -                                                    -      - -',
'-       <----------------------------------------------            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx        - -',
'--                                                    -            ---------------------------------------    -   - -',
'---                                                   -                                                           - -',
'----                                                  -                                                     -     - -',
'-----                                                 -                                             -  -----      - -',
'------                                                -                               -        --                 - -',
'-------                                               -            -   -     -     --    ---                      - -',
'--------            Y                        Y        -      -                                                    - -',
'---------    x     x        x       x    x    x                 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx- -',
'------------------------------------------------------------------------------------------------------------------- -',
'-        Y                Y                      Y                        Y                         Y               -',
'-                                                                                                                   -',
'- ----- ----  --------- --------- ------- -------- ------ --------   ----------------------  ---------------------- -',
'- -------------------------------------------------------------------------------------------------------------------',
'-                                                                                                                   -',
'-                                                            ------------------------------------------------------ -',
'-                                                                     -             -                             - -',
'-                                                           -         -     -       ->  ---      Y                - -',
'-                                                                     -    ---      ->  <- -                      - -',
'-                                                         -           -     -       ->  <-  -                     - -',
'- O                                                                   - -   -  -    ->  <-   -            Y       - -',
'-                                                      -              -     -       ->  <-     -                  - -',
'-                                                   -                 -   - -    -  ->  <-      -                 - -',
'-                                              -                      -     -       ->  <-        -               - -',
'-                           -    -    -  -                            --    - -     ->  <-          -             - -',
'-                    -                                                -     -       ->  <-           -            - -',
'-              -                                                      - O   -     - ->  <-            -           - -',
'-           -                                                         -   - --      ->  <-             -          - -',
'-        -                                                            -     -       ->  <-                        - -',
'-      -                                                              -     -   -   ->  <-              -    Y    - -',
'-     -                                                               --    -       ->  <-                -       - -',
'-                                                                     -     -  -    ->  <-                 -      - -',
'-    -                                                                -  -  -       ->  <-                        - -',
'-----------------------------------------------------------------------     -     - ->  <-                  -     - -',
'-----------------------------------------------------------------------     -       ->  <-                        - -',
'------------------------------------------------------------------------    - -     ->  <-        Y           -   - -',
'-----------------------------------------------------------------------  -  -       ->  <-                        - -',
'-----------------------------------------------------------------------     -    -  ->  <-                -       - -',
'-----------------------------------------------------------------------     -       ->  <-                        - -',
'------------------------------------------------------------------------    - -   - ->  <-                  --    - -',
'-----------------------------------------------------------------------     -       ->  <-         Y              - -',
'-----------------------------------------------------------------------    --       ->  <-                        - -',
'-----------------------------------------------------------------------     -   -   ->  <-             --         - -',
'-----------------------------------------------------------------------     -       ->  <-                        - -',
'-                                                                           - -     ->  <-                 --     - -',
'-                           --             Y                                -       ->  <-                        - -',
'-     -         --->                      -                                 -       ->  <-                  --    - -',
'-         --          --     -      -->       --     --    --               -   --- ->  <-                     -  - -',
'-           ->                 ---                                          -       ->  <-                          -',
'-        x   xx  x x x x x x x      x x x  x x x x x  x x x   x-x x---x---xx-           <-xxxxxxxxxxxxxxxxxxxxx------',
'--- -----------------------------------------------------------------------------------------------------------------',
'- Y                                                                                                                 -',
'-                                                                                                                 I -',
'---------------------------------------------------------------------------------------------------------------------'
 ]

# Сооздание множества всех игровых объектов класса Sprite и списков для различных подклассов класса  Sprite.
sprite_group = pygame.sprite.Group()
sprite_group.add(hero)
platforms = []
die_blocks_1 = []
die_blocks_2 = []
die_blocks_3 = []
die_blocks_4 = []
autsave_blocks = []

# Нахождение геометрических размеров уровня и создание камеры.
total_level_weight = len(level[0]) * 40
total_level_height = len(level) * 40
camera = Camera(camera_func, total_level_weight, total_level_height)

# Считывание с уровня всех обЪектов типа Sprite, добавление их во множество sprite_group и соответсвующие списки для подклассов.
x = 0
y = 0
for row in level:
    for col in row:
        if col == '-':
            pl = Platform(x, y)
            sprite_group.add(pl)
            platforms.append(pl)
        elif col == 'x':
            pl = BlockDie_1(x, y)
            sprite_group.add(pl)
            die_blocks_1.append(pl)
        elif col == '<':
            pl = BlockDie_2(x, y)
            sprite_group.add(pl)
            die_blocks_2.append(pl)
        elif col == '>':
            pl = BlockDie_3(x, y)
            sprite_group.add(pl)
            die_blocks_3.append(pl)
        elif col == 'Y':
            pl = Umnov(x, y)
            sprite_group.add(pl)
            die_blocks_4.append(pl)
        elif col == 'O':
            pl = Autsave(x, y)
            sprite_group.add(pl)
            autsave_blocks.append(pl)
        elif col == 'I':
            informatic = End(x, y)
            sprite_group.add(informatic)
        x += 40
    y += 40
    x = 0

# Создание звукового сопровождения.
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
sound = pygame.mixer.Sound('Angel.ogx')
sound.play(-1)

# Созданеи таймера.
timer = pygame.time.Clock()

# Переменная для выхода из игры.
done  = True

# Переменная для создания сохранялок.
d = 0

# Переменная для подсчета набранных очков.
i = 0

# Всеобъемлющий цикл.
while done:
    # Считывание и выпонение запросов пользователя.
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:
                left = True
            if e.key == pygame.K_d:
                right = True
            if e.key == pygame.K_w:
                up = True
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_a:
                left = False
            if e.key == pygame.K_d:
                right = False
            if e.key == pygame.K_w:
                up = False

    # Закрашивание экрана.
    screen.fill((10,120,10))

    # Генератор Умнова младшего.
    for umnov in die_blocks_4:
        umnov.update(platforms)

    # Обновление координат героя без сдвижения картинки.
    hero.update(left, up, right, platforms) 
    
    # Обнаружение заключительного игрового блока, прибавление очков за прохождение игры.
    p = hero.end(informatic, i, d, autsave_blocks, sprite_group)
    i = p[0]
    d = p[1]
    
    # Взаимодействие героя с сохранялками.
    d = hero.autsave(d, autsave_blocks, sprite_group)
    
    # Взаимодействие героя с монстрами.
    hero.get_die(die_blocks_1,d)
    hero.get_die(die_blocks_2,d)
    hero.get_die(die_blocks_3,d)  
    hero.get_die(die_blocks_4,d)

    # Передвижение камеры за героем без сдвижение картинки
    camera.update(hero) 

    # Прикрепление всех объектов к сместившемуся экрану без сдвижения картинки.
    for e in sprite_group:
        screen.blit(e.image, camera.apply(e)) 

    # Прикрепление экрана к окну.
    window.blit(screen,(0,0))

    # Отрисовка всех объектов в соответствии с их координатами(сдвижение каринки).
    pygame.display.flip()

    # Установка количества кадров в единицу времени.
    timer.tick(50)
