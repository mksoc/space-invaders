from enum import Enum
import random
from math import sqrt
from abc import ABC, abstractmethod
import pygame

width = 800
height = 600


def is_collision(item1, item2):
    # Calculate center coordinates
    x1 = item1.x + item1.IMAGE_SIDE_LEN / 2
    x2 = item2.x + item2.IMAGE_SIDE_LEN / 2
    y1 = item1.y + item1.IMAGE_SIDE_LEN / 2
    y2 = item2.y + item2.IMAGE_SIDE_LEN / 2
    
    distance = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
    if distance < max([item1.IMAGE_SIDE_LEN, item2.IMAGE_SIDE_LEN]) / 2:
        return True


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class BaseItem(ABC):
    STEP_X = 0
    STEP_Y = 0
    IMAGE_SIDE_LEN = 64

    def __init__(self, picture, window):
        self._img = pygame.image.load(picture)
        self._window = window
        self._x = 0
        self._y = 0
        self._speed_x = 0
        self._speed_y = 0

    # Coordinates getter/setter
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        """
        By default, limit the x coordinate to the windows boudaries.
        """
        if value <= 0:
            self._x = 0
        elif value >= width - self.IMAGE_SIDE_LEN:
            self._x = width - self.IMAGE_SIDE_LEN
        else:
            self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        """
        By default, limit the y coordinate to the windows boudaries.
        """
        if value <= 0:
            self._y = 0
        elif value >= height - self.IMAGE_SIDE_LEN:
            self._y = height - self.IMAGE_SIDE_LEN
        else:
            self._y = value

    # Movement methods
    @abstractmethod
    def move(self):
        pass

    def stop(self):
        self._speed_x = 0
        self._speed_y = 0

    def draw(self):
        self.x += self._speed_x
        self.y += self._speed_y
        self._window.blit(self._img, (self.x, self.y))


class Player(BaseItem):
    STEP_X = 5

    def __init__(self, picture, window):
        super().__init__(picture, window)
        self.x = (width - self.IMAGE_SIDE_LEN) / 2
        self.y = height - 100

    def move(self, direction):
        if direction == Direction.LEFT:
            self._speed_x = -self.STEP_X
        elif direction == Direction.RIGHT:
            self._speed_x = self.STEP_X


class Enemy(BaseItem):
    STEP_X = 3
    STEP_Y = 40

    def __init__(self, picture, window):
        super().__init__(picture, window)
        self.x = random.randint(0, width - self.IMAGE_SIDE_LEN / 2)
        self.y = random.randint(20, 150)
        self.move(Direction(random.randint(2, 3)))

    @BaseItem.x.setter
    def x(self, value):
        """
        Limit the x coordinate to the windows boudaries and change direction.
        """
        if value <= 0:
            self._x = 0
            self.move(Direction.DOWN)
            self.move(Direction.RIGHT)
        elif value >= width - self.IMAGE_SIDE_LEN:
            self._x = width - self.IMAGE_SIDE_LEN
            self.move(Direction.DOWN)
            self.move(Direction.LEFT)
        else:
            self._x = value

    def move(self, direction):
        if direction == Direction.LEFT:
            self._speed_x = -self.STEP_X
        elif direction == Direction.RIGHT:
            self._speed_x = self.STEP_X
        elif direction == Direction.DOWN:
            self.y += self.STEP_Y


class Bullet(BaseItem):
    STEP_Y = 10
    IMAGE_SIDE_LEN = 32

    def __init__(self, picture, window, player):
        super().__init__(picture, window)
        self._player = player
        self._firing = False

    @BaseItem.y.setter
    def y(self, value):
        """
        When bullet goes over the top, reset fire ready state.
        """
        if value <= 0:
            self.stop()
            self._firing = False
        else:
            self._y = value

    def move(self):
        self._speed_y = -self.STEP_Y

    # Draw on screen only when fired
    def draw(self):
        if self._firing:
            super().draw()

    # Set direction based on player position and fire
    def fire(self):
        if not self._firing:
            self._firing = True
            self.x = self._player.x + (self._player.IMAGE_SIDE_LEN - self.IMAGE_SIDE_LEN) / 2
            self.y = self._player.y - self.IMAGE_SIDE_LEN
            self.move()

    # Reset fired status when enemy is hit
    def hit(self):
        self._firing = False
