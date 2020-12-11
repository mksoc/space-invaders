from enum import Enum
import random
from abc import ABC, abstractmethod
import pygame

width = 800
height = 600


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class BaseItem(ABC):
    MAX_SPEED_X = 0
    MAX_SPEED_Y = 0
    IMAGE_SIDE_LEN = 64

    def __init__(self, picture, window):
        self._img = pygame.image.load(picture)
        self._window = window
        self.x = 0
        self.y = 0
        self._speed_x = 0
        self._speed_y = 0

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

    x = property(lambda self: self._x, x)

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

    y = property(lambda self: self._y, y)

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
    MAX_SPEED_X = 5

    def __init__(self, picture, window):
        super().__init__(picture, window)
        self.x = (width / 2) - 32
        self.y = height - 100

    def move(self, direction):
        if direction == Direction.LEFT:
            self._speed_x = -self.MAX_SPEED_X
        elif direction == Direction.RIGHT:
            self._speed_x = self.MAX_SPEED_X
