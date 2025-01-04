from settings import *
import pygame as pg
import math



class Player:
    """
    Класс игрока, управляющий его состоянием, передвижением и взаимодействием с игрой.
    """

    def __init__(self, game):
        """
        Инициализация игрока: позиция, угол обзора, здоровье и параметры управления.
        """
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recovery_delay = 590  # Задержка восстановления здоровья
        self.time_prev = pg.time.get_ticks()
        self.diag_move_corr = 1.4 / math.sqrt(2)  # Коррекция скорости при движении по диагонали
    
    def recover_health(self):
        """
        Автоматическое восстановление здоровья игрока с учетом задержки.
        """
        if self._can_recover_health() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def gain_health_on_kill(self):
        """
        Увеличивает здоровье игрока при убийстве врага на случайное значение (3-11).
        """
        health_bonus = 7  # Случайное количество восстанавливаемого здоровья
        self.health = min(self.health + health_bonus, PLAYER_MAX_HEALTH)

    def _can_recover_health(self):
        """
        Проверяет, прошло ли достаточно времени для восстановления здоровья.
        """
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def check_game_over(self):
        """
        Проверка на завершение игры: здоровье игрока не должно опускаться ниже 1.
        """
        if self.health < 1:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def get_damage(self, damage):
        """
        Уменьшает здоровье игрока при получении урона.
        """
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()
        self.check_game_over()

    def single_fire_event(self, event):
        """
        Обрабатывает одиночный выстрел игрока.
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True

    def movement(self):
        """
        Обрабатывает передвижение игрока, включая учет стен и диагонального движения.
        """
        sin_a, cos_a = math.sin(self.angle), math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin, speed_cos = speed * sin_a, speed * cos_a

        keys = pg.key.get_pressed()
        num_key_pressed = -1

        if keys[pg.K_w]:
            num_key_pressed += 1
            dx, dy = dx + speed_cos, dy + speed_sin
        if keys[pg.K_s]:
            num_key_pressed += 1
            dx, dy = dx - speed_cos, dy - speed_sin
        if keys[pg.K_a]:
            num_key_pressed += 1
            dx, dy = dx + speed_sin, dy - speed_cos
        if keys[pg.K_d]:
            num_key_pressed += 1
            dx, dy = dx - speed_sin, dy + speed_cos

        if num_key_pressed:
            dx, dy = dx * self.diag_move_corr, dy * self.diag_move_corr

        self._handle_wall_collision(dx, dy)

    def _handle_wall_collision(self, dx, dy):
        """
        Обрабатывает столкновения игрока со стенами.
        """
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self._can_move(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self._can_move(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def _can_move(self, x, y):
        """
        Проверяет, свободна ли клетка для движения игрока.
        """
        return (x, y) not in self.game.map.world_map

    def draw(self):
        """
        Рисует игрока и направление его взгляда (для отладки).
        """
        pg.draw.line(
            self.game.screen, 'yellow',
            (self.x * 100, self.y * 100),
            (self.x * 100 + WIDTH * math.cos(self.angle), self.y * 100 + WIDTH * math.sin(self.angle)),
            2
        )
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        """
        Управляет поворотом игрока с помощью мыши.
        """
        mx, _ = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        """
        Основной цикл обновления игрока: движение, контроль мыши, восстановление здоровья.
        """
        self.movement()
        self.mouse_control()
        self.recover_health()

    @property
    def pos(self):
        """
        Возвращает текущую позицию игрока.
        """
        return self.x, self.y

    @property
    def map_pos(self):
        """
        Возвращает текущую позицию игрока на карте.
        """
        return int(self.x), int(self.y)


from settings import *
import pygame as pg
import math


class Player:
    """
    Класс игрока, управляющий его состоянием, передвижением и взаимодействием с игрой.
    """

    def __init__(self, game):
        """
        Инициализация игрока: позиция, угол обзора, здоровье и параметры управления.
        """
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recovery_delay = 700  # Задержка восстановления здоровья
        self.time_prev = pg.time.get_ticks()
        self.diag_move_corr = 1 / math.sqrt(2)  # Коррекция скорости при движении по диагонали

    def recover_health(self):
        """
        Автоматическое восстановление здоровья игрока с учетом задержки.
        """
        if self._can_recover_health() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def gain_health_on_kill(self):
        """
        Увеличивает здоровье игрока при убийстве врага на случайное значение (3-11).
        """
        health_bonus = 10  # Случайное количество восстанавливаемого здоровья
        self.health = min(self.health + health_bonus, PLAYER_MAX_HEALTH)

    def _can_recover_health(self):
        """
        Проверяет, прошло ли достаточно времени для восстановления здоровья.
        """
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def check_game_over(self):
        """
        Проверка на завершение игры: здоровье игрока не должно опускаться ниже 1.
        """
        if self.health < 1:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def get_damage(self, damage):
        """
        Уменьшает здоровье игрока при получении урона.
        """
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()
        self.check_game_over()

    def single_fire_event(self, event):
        """
        Обрабатывает одиночный выстрел игрока.
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True

    def movement(self):
        """
        Обрабатывает передвижение игрока, включая учет стен и диагонального движения.
        """
        sin_a, cos_a = math.sin(self.angle), math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin, speed_cos = speed * sin_a, speed * cos_a

        keys = pg.key.get_pressed()
        num_key_pressed = -1

        if keys[pg.K_w]:
            num_key_pressed += 1
            dx, dy = dx + speed_cos, dy + speed_sin
        if keys[pg.K_s]:
            num_key_pressed += 1
            dx, dy = dx - speed_cos, dy - speed_sin
        if keys[pg.K_a]:
            num_key_pressed += 1
            dx, dy = dx + speed_sin, dy - speed_cos
        if keys[pg.K_d]:
            num_key_pressed += 1
            dx, dy = dx - speed_sin, dy + speed_cos

        if num_key_pressed:
            dx, dy = dx * self.diag_move_corr, dy * self.diag_move_corr

        self._handle_wall_collision(dx, dy)

    def _handle_wall_collision(self, dx, dy):
        """
        Обрабатывает столкновения игрока со стенами.
        """
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self._can_move(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self._can_move(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def _can_move(self, x, y):
        """
        Проверяет, свободна ли клетка для движения игрока.
        """
        return (x, y) not in self.game.map.world_map

    def draw(self):
        """
        Рисует игрока и направление его взгляда (для отладки).
        """
        pg.draw.line(
            self.game.screen, 'yellow',
            (self.x * 100, self.y * 100),
            (self.x * 100 + WIDTH * math.cos(self.angle), self.y * 100 + WIDTH * math.sin(self.angle)),
            2
        )
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        """
        Управляет поворотом игрока с помощью мыши.
        """
        mx, _ = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        """
        Основной цикл обновления игрока: движение, контроль мыши, восстановление здоровья.
        """
        self.movement()
        self.mouse_control()
        self.recover_health()

    @property
    def pos(self):
        """
        Возвращает текущую позицию игрока.
        """
        return self.x, self.y

    @property
    def map_pos(self):
        """
        Возвращает текущую позицию игрока на карте.
        """
        return int(self.x), int(self.y)
