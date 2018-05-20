import pygame
from fileplayer import Player
from platforms import Platform, BlockDie_1, BlockDie_2, BlockDie_3, Umnov, Autsave, End
from level import make_level
from music import music
from game_camera import Camera, camera_func
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

# Создание уровня.
level = make_level()

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
        x += 40
    y += 40
    x = 0

# Пишется отдельно из-за неудобных размеров изображения.
informatic = End(4510, 2430)
sprite_group.add(informatic)

# Создание таймера.
timer = pygame.time.Clock()

# Создание звукового сопровождения.
music()

# Переменная для выхода из игры.
done  = True

# Переменная для создания сохранялок.
d = 0

# Переменная для подсчета набранных очков.
score = 0

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

        # Считывание координат героя для перемещения в качестве разработчика.
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:  
                new_x = e.pos[0]
                new_y = e.pos[1]
                hack = True
        else:
            new_x = hero.rect.x
            new_y = hero.rect.y
            hack = False
    
    # Закрашивание экрана.
    screen.fill((10,120,10))

    # Генератор Умнова младшего.
    for umnov in die_blocks_4:
        umnov.update(platforms)

    # Обновление координат героя без сдвижения картинки.
    hero.update(left, up, right, platforms, hack, new_x, new_y, camera) 
    
    # Обнаружение заключительного игрового блока, прибавление очков за прохождение игры.
    p = hero.end(informatic, score, d, autsave_blocks, sprite_group)
    score = p[0]
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
        if e != informatic:
            screen.blit(e.image, camera.apply(e)) 
    screen.blit(informatic.image, camera.apply(informatic))
    # Прикрепление экрана к окну.
    window.blit(screen,(0,0))

    # Отрисовка всех объектов в соответствии с их координатами(сдвижение каринки).
    pygame.display.flip()

    # Установка количества кадров в единицу времени.
    timer.tick(50)
