import pygame
SIZE = (1300,700)
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
