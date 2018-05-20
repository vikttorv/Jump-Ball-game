from pygame.image import load
from pygame.sprite import Sprite, collide_rect

# Класс обычной платформы.
class Platform(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = load('images/Blok.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Класс ловушки "огонь", находящейся внизу.
class BlockDie_1(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = load('images/Fire.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Класс ловушки "монстр слева", находящейся с левой части блока.
class BlockDie_2(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = load('images/Axe_1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Класс ловушки "монстр справа", находящейся с правой части блока.
class BlockDie_3(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = load('images/Axe_2.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Класс монстра "Умнов Младший".
class Umnov(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = load('images/Umnov.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xvel = 5

    # Метод класса отвечающий за поворот монстра при соприкосновении с платформой.
    def collide(self,platforms):
        for pl in platforms:
            if collide_rect(self,pl):
                self.xvel = - self.xvel
                break

    # Обновление координат монстра.
    def update(self, platforms):
        self.rect.x += self.xvel
        self.collide(platforms)

# Класс сохранялки.
class Autsave(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = load('images/Autsave.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Класс заключительного блока.
class End(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = load('images/Main_boss.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

            
