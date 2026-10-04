import sys
from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

START_POSITION = (
    SCREEN_WIDTH // 2,
    SCREEN_HEIGHT // 2,
)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

TURNS = {
    pg.K_UP: (UP, DOWN),
    pg.K_DOWN: (DOWN, UP),
    pg.K_LEFT: (LEFT, RIGHT),
    pg.K_RIGHT: (RIGHT, LEFT),
}

BLACK = (0, 0, 0)
LIGHT_BLUE = (93, 216, 228)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(
        self,
        position=START_POSITION,
        body_color=None,
    ):
        """Инициализировать базовые свойства игрового объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовать игровой объект."""
        pass

    def draw_cell(self,
        position,
        color=None,
        border_color=LIGHT_BLUE,
    ):
        """Отрисовать клетку в указанной позиции."""
        if color is None:
            color = self.body_color

        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, border_color, rect, 1)

class Apple(GameObject):
    """Представить яблоко на игровом поле."""

    def __init__(self, body_color=RED):
        """Создать яблоко в случайной клетке игрового поля."""
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self, occupied_positions=()):
        """Задать яблоку случайную позицию на игровом поле."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )

            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовать яблоко на игровом поле."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Представить змейку и управлять её движением."""

    def __init__(self, body_color=GREEN):
        """Создать змейку с одной головой в центре поля."""
        super().__init__(body_color=body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновить направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Переместить змейку на одну клетку игрового поля."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        new_head = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)

        self.last = (
            self.positions.pop()
            if len(self.positions) > self.length
            else None
        )

    def draw(self):
        """Отрисовать голову змейки и стереть её хвост."""
        if self.last is not None:
            self.draw_cell(self.last, BLACK, BLACK)

        self.draw_cell(self.get_head_position())

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбросить змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обработать нажатия клавиш управления змейкой."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type != pg.KEYDOWN:
            continue

        if event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()

        if event.key in TURNS:
            new_direction, opposite = TURNS[event.key]

            if game_object.direction != opposite:
                game_object.next_direction = new_direction



def main():
    """Запустить основной игровой цикл."""
    pg.init()

    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    screen.fill(BLACK)
    snake.draw()
    apple.draw()
    pg.display.update()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
            snake.draw()
            apple.draw()
            pg.display.update()


        elif snake.get_head_position() in snake.positions[4:]:

            snake.reset()

            if apple.position in snake.positions:
                apple.randomize_position(snake.positions)

            screen.fill(BLACK)

            snake.draw()

            apple.draw()

            pg.display.update()

            continue

        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
