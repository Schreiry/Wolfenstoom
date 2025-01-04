import pygame as pg
import sys
from settings import *  # Настройки игры (размер экрана, FPS и т. д.)
from map import *  # Карта игры
from player import *  # Игрок
from raycasting import *  # Система рэйкастинга (визуализация 3D)
from object_renderer import *  # Отображение объектов
from sprite_object import *  # Работа с объектами-спрайтами
from object_handler import *  # Обработчик объектов
from weapon import Weapon  # Исправлено: импортируем класс Weapon
from sound import *  # Работа со звуком
from pathfinding import *  # Алгоритм поиска пути


class Game:
    def __init__(self):
        """
        Инициализация игры.
        Настраивает параметры экрана, событий и запускает новую игру.
        """
        pg.init()
        pg.mouse.set_visible(False)  # Скрыть курсор мыши
        self.screen = pg.display.set_mode(RES)  # Создать окно с заданным разрешением
        pg.event.set_grab(True)  # Зафиксировать курсор внутри окна
        self.clock = pg.time.Clock()  # Контроль FPS
        self.delta_time = 1  # Временной дельта-костыль
        self.global_trigger = False  # Флаг для глобальных событий
        self.global_event = pg.USEREVENT + 0  # Определение глобального пользовательского события
        pg.time.set_timer(self.global_event, 40)  # Таймер глобального события
        self.new_game()  # Запуск новой игры

    def new_game(self):
        """
        Настройка новой игры. 
        Инициализирует карту, игрока, объекты, оружие и другие компоненты.
        """
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)  # Создаем экземпляр класса Weapon
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)  # Запуск фоновой музыки (бесконечный цикл)

    def update(self):
        """
        Обновление состояния игры. 
        Вызывается на каждом кадре.
        """
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()  # Обновление экрана
        self.delta_time = self.clock.tick(FPS)  # Контроль времени кадра
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')  # Отображение FPS в заголовке окна

    def draw(self):
        """
        Рисует все элементы игры на экране.
        """
        self.object_renderer.draw()
        self.weapon.draw()
        # Для отладки можно включить отрисовку карты и игрока:
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        """
        Обрабатывает все события в игре (выход, нажатия клавиш и т. д.).
        """
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        """
        Основной цикл игры. 
        Управляет событиями, обновлениями и отрисовкой.
        """
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
