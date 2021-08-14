import math
import random
from enum import Enum
from typing import Tuple, List

import pygame


class DoorState(Enum):
    CLOSED = 0,
    OPEN = 1,
    BROKEN = 2


class DoorComponent:

    def __init__(self, state: DoorState = DoorState.CLOSED):
        self._state = state

    def is_closed(self):
        return self._state == DoorState.CLOSED

    def open(self):
        self._state = DoorState.OPEN


class TileType(Enum):
    VOID = 0,
    WALL = 1,
    GROUND = 2,
    DOOR = 3


class WallType(Enum):
    HORIZONTAL_WALL = 0,
    VERTICAL_WALL = 1,
    TOP_LEFT_CORNER_WALL = 2,
    TOP_RIGHT_CORNER_WALL = 3,
    BOTTOM_LEFT_CORNER_WALL = 4,
    BOTTOM_RIGHT_CORNER_WALL = 5,
    FOREST = 6,
    WATER = 7


class DoorType(Enum):
    HDOOR = 0,
    VDOOR = 1


class GroundType(Enum):
    GROUND = 0,
    CORRIDOR = 1,
    GRASS = 2


class VoidType(Enum):
    VOID = 0


class Tile:
    def __init__(self):
        pass


class VoidTile(Tile):
    def __init__(self, void_type: VoidType = VoidType.VOID):
        super().__init__()
        self.void_type = void_type


class WallTile(Tile):
    def __init__(self, wall_type: WallType):
        super().__init__()
        self.wall_type = wall_type


class GroundTile(Tile):
    def __init__(self, ground_type: GroundType):
        super().__init__()
        self.ground_type = ground_type


class DoorTile(Tile):
    def __init__(self, door_type: DoorType):
        super().__init__()
        self.door_type = door_type


VOID_TILE = VoidTile()

VWALL_TILE = WallTile(WallType.VERTICAL_WALL)
HWALL_TILE = WallTile(WallType.HORIZONTAL_WALL)
TLWALL_TILE = WallTile(WallType.TOP_LEFT_CORNER_WALL)
BLWALL_TILE = WallTile(WallType.BOTTOM_LEFT_CORNER_WALL)
TRWALL_TILE = WallTile(WallType.TOP_RIGHT_CORNER_WALL)
BRWALL_TILE = WallTile(WallType.BOTTOM_RIGHT_CORNER_WALL)
FOREST_TILE = WallTile(WallType.FOREST)
WATER_TILE = WallTile(WallType.WATER)

GROUND_TILE = GroundTile(GroundType.GROUND)
CORRIDOR_TILE = GroundTile(GroundType.CORRIDOR)
GRASS_TILE = GroundTile(GroundType.GRASS)

HDOOR_TILE = DoorTile(DoorType.HDOOR)
VDOOR_TILE = DoorTile(DoorType.VDOOR)


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

    def width(self) -> int:
        return len(self._grid)

    def height(self) -> int:
        return len(self._grid[0])

    def grid(self) -> List[List[Tile]]:
        return self._grid

    def tile(self, x: int, y: int) -> Tile:
        return self._grid[x][y]

    def rooms(self) -> List[Room]:
        return self._rooms

    def level(self) -> int:
        return self._level


class DungeonResidentComponent:

    def __init__(self):
        pass


class PositionComponent:

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def xy(self) -> Tuple[int, int]:
        return self._x, self._y

    def move(self, dx: int, dy: int):
        self._x += dx
        self._y += dy


class MovableComponent:

    def __init__(self):
        pass


class BlockComponent:

    def __init__(self):
        pass
