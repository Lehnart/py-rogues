import math
import random
from enum import Enum
from typing import Tuple, List

import pygame


class Tile(Enum):
    VOID = 0,
    WALL = 1,
    GROUND = 2,
    HDOOR = 3,
    VDOOR = 4,
    CORRIDOR = 5,


class Room:

    def __init__(self, x0: int, y0: int, w: int, h: int):
        self.x0 = x0
        self.y0 = y0
        self.w = w
        self.h = h
        self._is_occupied = [[False for _ in range(self.h)] for _ in range(self.w)]

    def is_in(self, x: int, y: int) -> bool:
        if self.x0 <= x < self.x0 + self.w and self.y0 <= y < self.y0 + self.h:
            return True
        return False

    def center(self) -> Tuple[int, int]:
        return (2 * self.x0 + self.w) // 2, (2 * self.y0 + self.h) // 2

    def distance_to(self, room) -> float:
        x1, y1 = self.center()
        x2, y2 = room.center()
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def is_occupied(self, x, y) -> bool:
        x -= self.x0
        y -= self.y0
        return self._is_occupied[x][y]

    def set_occupied(self, x, y):
        x -= self.x0
        y -= self.y0
        self._is_occupied[x][y] = True

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x0, self.y0, self.w, self.h)

    def _rand_x_in_room(self) -> int:
        return random.randint(self.x0 + 1, self.x0 + self.w - 2)

    def _rand_y_in_room(self) -> int:
        return random.randint(self.y0 + 1, self.y0 + self.h - 2)

    def rand_in_room(self) -> Tuple[int, int]:
        return self._rand_x_in_room(), self._rand_y_in_room()

    def rand_door(self) -> Tuple[int, Tuple[int, int]]:
        r = random.choice([0, 1, 2, 3])  # 0 is top, 1 is right, 2 is bottom, 3 is left
        if r == 0:
            return 0, (random.randint(self.x0 + 1, self.x0 + self.w - 2), self.y0)
        if r == 1:
            return 1, (self.x0 + self.w - 1, random.randint(self.y0 + 1, self.y0 + self.h - 2))
        if r == 2:
            return 2, (random.randint(self.x0 + 1, self.x0 + self.w - 2), self.y0 + self.h - 1)
        if r == 3:
            return 3, (self.x0, random.randint(self.y0 + 1, self.y0 + self.h - 2))


class DungeonComponent:

    def __init__(self, grid: List[List[Tile]], rooms: List[Room]):
        self._grid = grid
        self._rooms = rooms
        self._level = 1

    def grid(self) -> List[List[Tile]]:
        return self._grid

    def rooms(self) -> List[Room]:
        return self._rooms

    def level(self) -> int:
        return self._level
