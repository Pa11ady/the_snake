from random import randint

import pygame

# Инициализация PyGame
pygame.init()

# Константы для размеров
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета фона - черный
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет яблока - красный
APPLE_COLOR = (255, 0, 0)

# Цвет змени - зелёный
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки
SPEED = 5

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR,
                 position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Заготовка метода для отрисовки объекта на игровом поле."""
        raise NotImplementedError


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.is_reset = False

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод обновляет позицию, размеры змейки и проверяет столкновения."""
        head = self.get_head_position()
        head = (
            (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
        )
        # Если змейка столкнулась, то начинаем игру сначала
        if head in self.positions:
            self.reset()
            return

        self.positions.insert(0, head)
        # Если змея не стала больше, то удаляем хвост и запоминаем его
        if self.length < len(self.positions):
            self.last = self.positions.pop()

    def draw(self, surface):
        """Метод для рисования змейки на экране."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)

        # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, (93, 216, 228), head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод  возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод  сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions.clear()
        self.positions.append(self.position)
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.is_reset = True


class Apple(GameObject):
    """Класс Яблоко."""

    def __init__(self):
        super().__init__(APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Метод устанавливает случайное положение яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - GRID_SIZE) * GRID_SIZE,
            randint(0, GRID_HEIGHT - GRID_SIZE) * GRID_SIZE
        )

    def draw(self, surface):
        """Метод отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (93, 216, 228), rect, 1)


def handle_keys(game_object):
    """Функция для обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция приложения."""
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Сброc игры когда змея столкнусь (событие в методе move)
        if snake.is_reset:
            apple.randomize_position()
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.is_reset = False

        # Змея съела яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()


if __name__ == '__main__':
    main()
