from sprite_object import *
from npc import *
from random import choices, randrange


class ObjectHandler:
    """
    Класс для управления объектами и NPC в игре. 
    Занимается добавлением, обновлением и контролем игровых объектов.
    """

    def __init__(self, game):
        """
        Инициализация обработчика объектов.
        Устанавливает игровые параметры, добавляет NPC и статические спрайты.
        """
        self.game = game
        self.sprite_list = []  # Список всех спрайтов
        self.npc_list = []  # Список всех NPC
        self.npc_positions = {}  # Позиции всех NPC на карте

        # Пути к ресурсам
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'

        # Конфигурация NPC
        self.enemies = 20  # Количество врагов
        self.npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC]  # Типы NPC
        self.weights = [70, 20, 10]  # Вероятности появления типов NPC
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}  # Запрещенная зона спавна

        # Спавн NPC
        self.spawn_npc()

        # Добавление статических спрайтов
        self._initialize_sprites()

        # Добавление NPC на карту
        self._initialize_npc()

    def spawn_npc(self):
        """
        Генерация NPC с учетом типов, вероятностей и ограничений спавна.
        """
        for _ in range(self.enemies):
            npc_class = choices(self.npc_types, self.weights)[0]
            pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)

            # Убедиться, что позиция не занята или находится в запрещенной зоне
            while pos in self.game.map.world_map or pos in self.restricted_area:
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)

            # Добавить NPC
            self.add_npc(npc_class(self.game, pos=(x + 0.5, y + 0.5)))

    def _initialize_sprites(self):
        """
        Добавляет статические и анимированные спрайты в игру.
        """
        sprite_positions = [
            (1.5, 1.5), (1.5, 7.5), (5.5, 3.25), (5.5, 4.75),
            (7.5, 2.5), (7.5, 5.5), (14.5, 1.5), (14.5, 4.5),
            (14.5, 24.5), (14.5, 30.5), (1.5, 30.5), (1.5, 24.5)
        ]

        # Добавление обычных спрайтов
        for pos in sprite_positions:
            self.add_sprite(AnimatedSprite(self.game, pos=pos))

        # Добавление анимированных красных огней
        red_light_positions = [
            (14.5, 5.5), (14.5, 7.5), (12.5, 7.5),
            (9.5, 7.5), (14.5, 12.5), (9.5, 20.5),
            (10.5, 20.5), (3.5, 14.5), (3.5, 18.5)
        ]

        for pos in red_light_positions:
            self.add_sprite(AnimatedSprite(self.game, path=self.anim_sprite_path + 'red_light/0.png', pos=pos))

    def _initialize_npc(self):
        """
        Добавляет NPC вручную на определенные позиции.
        """
        manual_npc_positions = [
            (SoldierNPC, (11.0, 19.0)), (SoldierNPC, (11.5, 4.5)),
            (SoldierNPC, (13.5, 6.5)), (SoldierNPC, (2.0, 20.0)),
            (SoldierNPC, (4.0, 29.0)), (CacoDemonNPC, (5.5, 14.5)),
            (CacoDemonNPC, (5.5, 16.5)), (CyberDemonNPC, (14.5, 25.5))
        ]

        for npc_class, pos in manual_npc_positions:
            self.add_npc(npc_class(self.game, pos=pos))

    def check_win(self):
        """
        Проверяет, уничтожены ли все NPC.
        Если да, завершает текущую игру и запускает новую.
        """
        if not self.npc_positions:
            self.game.object_renderer.win()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def update(self):
        """
        Обновляет состояния всех объектов и NPC в игре.
        Также проверяет условие победы.
        """
        # Обновление позиций NPC
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}

        # Обновление всех спрайтов и NPC
        for sprite in self.sprite_list:
            sprite.update()

        for npc in self.npc_list:
            npc.update()

        # Проверка победы
        self.check_win()

    def add_npc(self, npc):
        """
        Добавляет NPC в список.
        """
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        """
        Добавляет спрайт в список.
        """
        self.sprite_list.append(sprite)
