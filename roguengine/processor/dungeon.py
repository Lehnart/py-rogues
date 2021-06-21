import bisect
import random
from copy import deepcopy
from queue import Queue
from typing import List, Dict, Tuple

import pygame

from roguengine.component.dungeon import DungeonComponent, Room, Tile, VoidTile, VOID_TILE, TLWALL_TILE, BLWALL_TILE, TRWALL_TILE, BRWALL_TILE, \
    HWALL_TILE, VWALL_TILE, GROUND_TILE, WallTile, VDOOR_TILE, HDOOR_TILE, CORRIDOR_TILE
from roguengine.component.position import PositionComponent
from roguengine.component.sprite import VisibleSpriteComponent, InvisibleSpriteComponent
from roguengine.esper import Processor
from roguengine.event.dungeon_creation import DungeonCreationEvent
from roguengine.event.dungeon_filling import DungeonFillingEvent
from roguengine.event.dungeon_generation import DungeonGenerationEvent


class DungeonConfig:

    def __init__(self,
                 room_size_min: int,
                 room_size_max: int,
                 room_count_min: int,
                 room_count_max: int,
                 width: int,
                 height: int,
                 ):
        super().__init__()

        self.room_size_min = room_size_min
        self.room_size_max = room_size_max
        self.room_count_min = room_count_min
        self.room_count_max = room_count_max
        self.width = width
        self.height = height



class DungeonResident:

    def __init__(self, components: List[object], probability: float, n_max_per_dungeon: int, sprite: pygame.Surface):
        self._components = components
        self._probability = probability
        self._n_max_per_dungeon = n_max_per_dungeon
        self._sprite = sprite
        self._number_created = 0

    def components(self) -> List[object]:
        return self._components

    def probability(self) -> float:
        return self._probability

    def n_max_per_dungeon(self) -> int:
        return self._n_max_per_dungeon

    def sprite(self) -> pygame.Surface:
        return self._sprite

    def created(self):
        self._number_created += 1

    def can_create(self) -> bool:
        return self._number_created < self._n_max_per_dungeon

    def reset(self):
        self._number_created = 0


class DungeonResidents:

    def __init__(self, number_proba_per_room: Dict[int, float], residents: List[DungeonResident], sprite_layer: int):
        self._number_proba_per_room = number_proba_per_room
        self._residents = residents
        self._sprite_layer = sprite_layer

    def residents(self) -> List[DungeonResident]:
        return self._residents

    def number_proba_per_room(self) -> Dict[int, float]:
        return self._number_proba_per_room

    def sprite_layer(self) -> int:
        return self._sprite_layer


class DungeonCreator(Processor):

    def __init__(self,
                 tile_sprites: Dict[Tile, pygame.Surface],
                 tile_invisible_sprites: Dict[Tile, pygame.Surface],
                 tile_components: Dict[Tile, list],
                 px0: int = 0,
                 py0: int = 0
                 ):

        super().__init__()

        self._tile_sprites = tile_sprites
        self._tile_invisible_sprites = tile_invisible_sprites
        self._tile_components = tile_components
        self.px0 = px0
        self.py0 = py0

    def process(self):
        msgs = self.world.receive(DungeonCreationEvent)
        for msg in msgs:
            dungeon = msg.dungeon

            for x in range(len(dungeon.grid())):
                for y in range(len(dungeon.grid()[x])):
                    if dungeon.grid()[x][y] not in self._tile_sprites:
                        continue
                    tile = dungeon.grid()[x][y]
                    tile_sprite = self._tile_sprites[tile]
                    sprite = VisibleSpriteComponent(
                        (x * tile_sprite.get_width()) + self.px0,
                        (y * tile_sprite.get_height()) + self.py0,
                        tile_sprite
                    )
                    pos = PositionComponent(x, y)

                    if self._tile_invisible_sprites and tile in self._tile_invisible_sprites:
                        invisible_sprite = InvisibleSpriteComponent(
                            (x * tile_sprite.get_width()) + self.px0,
                            (y * tile_sprite.get_height()) + self.py0,
                            self._tile_invisible_sprites[tile]
                        )
                        components = [*[c() for c in self._tile_components[tile]], sprite, invisible_sprite, pos]
                    else:
                        components = [*[c() for c in self._tile_components[tile]], sprite, pos]

                    self.world.create_entity(*components)


class DungeonGenerator(Processor):

    def __init__(self):
        super().__init__()
        self._last_config = None

    def process(self):

        msgs = self.world.receive(DungeonGenerationEvent)
        for msg in msgs:
            dungeon = msg.dungeon

            if dungeon is None:
                dungeon = self._last_config
            self._last_config = dungeon

            for ent, _ in self.world.get_component(PositionComponent):
                self.world.delete_entity(ent, True)

            grid, rooms = self._generate_rooms(dungeon)
            self._connect_rooms(grid, rooms)

            dungeon = self.world.get_component(DungeonComponent)
            new_dungeon_component = DungeonComponent(grid, rooms)
            if dungeon:
                dungeon_entity, dungeon_component = dungeon[0]
                self.world.remove_component(dungeon_entity, DungeonComponent)
            else:
                dungeon_entity = self.world.create_entity()

            self.world.add_component(dungeon_entity, new_dungeon_component)
            self.world.publish(DungeonCreationEvent(new_dungeon_component))
            self.world.publish(DungeonFillingEvent(new_dungeon_component))

    def _generate_rooms(self, dungeon: DungeonConfig) -> Tuple[List[List[Tile]], List[Room]]:

        grid = [[VOID_TILE for _ in range(dungeon.height)] for _ in range(dungeon.width)]
        n_room = random.randint(dungeon.room_count_min, dungeon.room_count_max)
        return grid, [self._generate_room(dungeon, grid) for _ in range(n_room)]

    def _generate_room(self, dungeon: DungeonConfig, grid: List[List[Tile]]) -> Room:

        while True:

            w, h = random.randint(dungeon.room_size_min, dungeon.room_size_max), random.randint(dungeon.room_size_min, dungeon.room_size_max)
            x_max, y_max = dungeon.width - w - 1, dungeon.height - h - 1
            x0, y0 = random.randint(1, x_max), random.randint(1, y_max)

            is_empty = True
            for y in range(y0, y0 + h):

                if not is_empty:
                    break

                for x in range(x0, x0 + w):
                    if grid[x][y] != VOID_TILE:
                        is_empty = False
                        break

            if not is_empty:
                continue

            for x in range(x0, x0 + w):
                if x == x0:
                    grid[x][y0] = TLWALL_TILE
                    grid[x][y0 + h - 1] = BLWALL_TILE

                elif x == x0 + w - 1:
                    grid[x][y0] = TRWALL_TILE
                    grid[x][y0 + h - 1] = BRWALL_TILE

                else:
                    grid[x][y0] = HWALL_TILE
                    grid[x][y0 + h - 1] = HWALL_TILE

            for y in range(y0, y0 + h):
                if y == y0 or y == y0 + h - 1:
                    continue

                else:
                    grid[x0][y] = VWALL_TILE
                    grid[x0 + w - 1][y] = VWALL_TILE

            for x in range(x0 + 1, x0 + w - 1):
                for y in range(y0 + 1, y0 + h - 1):
                    grid[x][y] = GROUND_TILE

            return Room(x0, y0, w, h)

    def _connect_rooms(self, grid: List[List[Tile]], rooms):
        connected_rooms = []
        not_connected_rooms = list(rooms)
        while len(not_connected_rooms) != 0:

            if len(connected_rooms) == 0:
                room_index = random.randint(0, len(not_connected_rooms) - 1)
                connected_rooms.append(not_connected_rooms.pop(room_index))
                continue

            connected_room = random.choice(connected_rooms)
            room_distances = [(index, r, connected_room.distance_to(r)) for index, r in enumerate(not_connected_rooms)]
            room_distances.sort(key=lambda l: l[2])
            not_connected_room_index, not_connected_room, _ = room_distances[0]

            if self._connect_two_rooms(grid, connected_room, not_connected_room):
                connected_rooms.append(not_connected_room)
                not_connected_rooms.pop(not_connected_room_index)

    def _connect_two_rooms(self, grid: List[List[Tile]], room1: Room, room2: Room) -> bool:
        x1, y1 = room1.rand_in_room()
        x2, y2 = room2.rand_in_room()

        x_min, y_min = min(x1, x2), min(y1, y2)
        x_max, y_max = max(x1, x2), max(y1, y2)

        wall_count = 0
        for i in range(x_min, x_max + 1):
            if isinstance(grid[i][y1], WallTile):
                wall_count += 1
        for i in range(y_min, y_max + 1):
            if isinstance(grid[x2][i], WallTile):
                wall_count += 1
        if wall_count != 2:
            return False

        for i in range(x_min, x_max + 1):
            if grid[i][y1] == HWALL_TILE:
                grid[i][y1] = VDOOR_TILE
            elif grid[i][y1] == VWALL_TILE:
                grid[i][y1] = HDOOR_TILE
            elif isinstance(grid[i][y1], VoidTile):
                grid[i][y1] = CORRIDOR_TILE

        for i in range(y_min, y_max + 1):

            if grid[x2][i] == VWALL_TILE:
                grid[x2][i] = HDOOR_TILE
            elif grid[x2][i] == HWALL_TILE:
                grid[x2][i] = VDOOR_TILE
            elif isinstance(grid[x2][i], VoidTile):
                grid[x2][i] = CORRIDOR_TILE

        return True


class DungeonFiller(Processor):

    def __init__(self, dungeon_residents: List[DungeonResidents], px0 : int = 0, py0 : int = 0):

        super().__init__()
        self._dungeon_residents = dungeon_residents
        self.px0 = px0
        self.py0 = py0

    def process(self):
        for msg in self.world.receive(DungeonFillingEvent):
            dungeon: DungeonComponent = msg.dungeon
            rooms = dungeon.rooms()
            for room in rooms:
                self._generate_residents_in_room(room)

            for residents in self._dungeon_residents:
                for resident in residents.residents():
                    resident.reset()

    def _generate_residents_in_room(self, room):
        for dungeon_residents in self._dungeon_residents:
            residents = [r for r in dungeon_residents.residents() if r.can_create()]
            if not residents:
                continue
            probas = dungeon_residents.number_proba_per_room()

            proba_list = [0.]
            number_list = [None]
            for k in probas:
                pp = proba_list[-1]
                proba_list.append(probas[k] + pp)
                number_list.append(k)

            rand = random.random() * proba_list[-1]
            index = bisect.bisect_left(proba_list, rand)
            number_in_this_room = number_list[index]

            for _ in range(number_in_this_room):
                residents = [r for r in dungeon_residents.residents() if r.can_create()]
                proba_list = [0.]
                for i in range(len(residents)):
                    pp = proba_list[-1]
                    proba_list.append(residents[i].probability() + pp)

                rand = random.random() * proba_list[-1]
                index = bisect.bisect_left(proba_list, rand)
                resident = residents[index - 1]

                while True:
                    rx, ry = room.rand_in_room()
                    if room.is_occupied(rx, ry):
                        continue

                    resident_sprite = resident.sprite()
                    sprite = VisibleSpriteComponent(
                        (rx * resident_sprite.get_width()) + self.px0,
                        (ry * resident_sprite.get_height()) + self.py0,
                        resident_sprite,
                        dungeon_residents.sprite_layer()
                    )
                    pos = PositionComponent(rx, ry)
                    components = [*deepcopy(resident.components()), sprite, pos]
                    self.world.create_entity(*components)
                    resident.created()
                    room.set_occupied(rx, ry)
                    break
