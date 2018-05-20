import pygame.time
from pygame import Surface
from pygame.sprite import Sprite, collide_rect
from pygame.image import load

# Игровые константы.
MOVE_SPEED = 0.6
GRAVITY = 0.4
JUMP_POWER = 12
LIMIT_SPEED = 40

class Player(Sprite):
    def __init__(self,x,y):
        Sprite.__init__(self)
        self.image = load('ball1.png')

        # Снятие прямоугольника с картинки героя.
        self.rect = self.image.get_rect()

        # Координаты и скорость этого прямоугольника. 
        self.rect.x = x  
        self.rect.y = y
        self.yvel = 0
        self.xvel = 0

        # Атрибут, показывающий наличие земли под ногами.
        self.onGround = False

    # Метод класса, отвечающий за смерть героя.
    def get_die(self, die_blocks,d):
        for enemy in die_blocks:
            # Проверка пересечения блока героя и монстров и отправление героя к ближайшей сохранялке при данном пересечении.
            if collide_rect(self, enemy):
                if d == 0:
                    self.rect.x = 80
                    self.rect.y = 80
                    self.yvel = 0
                    self.xvel = 0
                if d == 1:
                    self.rect.x = 2520
                    self.rect.y = 160
                    self.yvel = 0
                    self.xvel = 0      
                if d == 2:
                    self.rect.x = 80
                    self.rect.y = 1400
                    self.yvel = 0
                    self.xvel = 0
                if d == 3:
                    self.rect.x = 2840
                    self.rect.y = 1400
                    self.yvel = 0
                    self.xvel = 0
    
    # Метод класса, отвечающий за обновление координат героя.
    def update(self, left, up, right, platforms):
        if left:

            # Изменение self.xvel для более быстрого набора скорости.
            if self.xvel == 0:
                 self.xvel = -5

            # Основное изменение скорости.
            self.xvel -=  MOVE_SPEED

            # Создание лимитирующей скорости (иначе при большом разгоне герой может вылететь за пределы уровня).
            if abs(self.xvel) > LIMIT_SPEED:
                self.xvel +=  MOVE_SPEED
            # Ослабление движения по инерции. 
            if self.xvel > 15: 
                self.xvel = 15 
 
        # Все аналогично "if left".         
        if right:
            if self.xvel == 0:
                 self.xvel = 5
            self.xvel += MOVE_SPEED
            if abs(self.xvel) > LIMIT_SPEED:
                self.xvel -=  MOVE_SPEED 
            if self.xvel < -15: 
                self.xvel = -15

        # Контролируемое ликвидирование инерции.   
        if not(left or right):
            self.xvel = 0

        # Выполнение прыжка.
        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER

        # Включение влияния гравитации.
        if not self.onGround:
            self.yvel += GRAVITY   
        self.onGround = False

        # Прибавление скорости к координатам, проверка пересечения с платформами (во избежание неправильной динамики производить для отдельно каждой координаты)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

    # Метод класса, отвечающий за взатимодействие героя с платформами.
    def collide(self, xvel, yvel, platforms):
        for pl in platforms:
            # Действия при пересечении героя и платформы.
            if collide_rect(self,pl):

                # Проверка пересечения с платформой справа и возвращение героя к ее левому краю при пересечении.
                if xvel > 0:
                    self.rect.right = pl.rect.left

                # Проверка пересечения с платформой слева и возвращение героя к ее правому краю при пересечении.
                if xvel < 0:
                    self.rect.left = pl.rect.right

                # Проверка пересечения с платформой снизу. Создание отметки, что герой на земле, если это так. Возвращение героя к верхнему краю платформы при пересечении.
                if yvel > 0:
                    self.rect.bottom = pl.rect.top
                    self.onGround = True
                    self.yvel = 0

                # Проверка пересечения с платформой сверху. Возвращение героя к нижнему краю платформы, если жто так.
                if yvel < 0:
                    self.rect.top = pl.rect.bottom
                    self.yvel = 0

    # Метод класса, отвечающий за сохранение.
    def autsave(self, d, autsave_blocks, sprite_group):  
        for i in range(len(autsave_blocks)):
            if collide_rect(self, autsave_blocks[i]):

                # Данная сохранялка переcтает отрисовываться, а место сохранения героя становится соответствующим значению "i + 1".
                sprite_group.remove(autsave_blocks[i])
                return (i + 1)

        # Иначе место сохранения героя остается прежним.
        return d

    # Метод класса, отвечающий за пересечение с финальной платформой.
    def end(self, end_level, score, d, autsave_blocks, sprite_group):

        # Изменения места сохранения на начальное. Увеличение количества набранных очков.
        if collide_rect(self, end_level):
            score += 1
            d = 0

            # Добавление всех исчезнувших сохранялок на уровень снова.
            for aut in autsave_blocks:
                if aut not in sprite_group:
                    sprite_group.add(aut)

            # Возвращение положение героя к начальному. Изменение надписи наверху с целью изменить количество набранных очков.
            self.rect.x = 80
            self.rect.y = 80
            self.yvel = 0
            self.xvel = 0
            tmp = 'Super Mario. Score = ' + str(i) 
            pygame.display.set_caption(tmp)
        return [score,d]    
            
            
                


