import pygame

from pynethack.font import FONT
from pynethack.sprites import SPRITE_DICT
from roguengine import esper
from roguengine.component.door import DoorComponent, DoorState
from roguengine.component.dungeon import VWALL_TILE, HWALL_TILE, TLWALL_TILE, BLWALL_TILE, TRWALL_TILE, BRWALL_TILE, GROUND_TILE, CORRIDOR_TILE, \
    HDOOR_TILE, VDOOR_TILE
from roguengine.component.dungeon_resident import DungeonResidentComponent
from roguengine.component.label import LabelComponent
from roguengine.component.movable import MovableComponent
from roguengine.component.player import PlayerComponent
from roguengine.component.window import WindowComponent
from roguengine.event.dungeon_generation import DungeonGenerationEvent
from roguengine.processor.door import DoorProcessor
from roguengine.processor.dungeon import DungeonResident, DungeonResidents, DungeonGenerator, DungeonCreator, DungeonFiller, DungeonConfig
from roguengine.processor.input import InputProcessor
from roguengine.processor.move import MoveProcessor
from roguengine.processor.render import RenderProcessor
from roguengine.processor.ui import GenericUIDrawerProcessor, Font
from roguengine.processor.view import ViewProcessor


class GameWorld(esper.World):
    def __init__(self):
        super().__init__()
        self._is_running: bool = True

        window = WindowComponent((800, 800))
        self.create_entity(window)

        player_sprite = SPRITE_DICT["player"]
        player_resident = DungeonResident(
            [
                PlayerComponent(),
                DungeonResidentComponent(),
            ],
            1.,
            1,
            player_sprite
        )
        player_residents = DungeonResidents({1: 1}, [player_resident], 3)

        tile_sprites = {
            VWALL_TILE: SPRITE_DICT["vwall"],
            HWALL_TILE: SPRITE_DICT["hwall"],
            TLWALL_TILE: SPRITE_DICT["twall"],
            BLWALL_TILE: SPRITE_DICT["bwall"],
            TRWALL_TILE: SPRITE_DICT["twall"],
            BRWALL_TILE: SPRITE_DICT["bwall"],
            GROUND_TILE: SPRITE_DICT["ground"],
            CORRIDOR_TILE: SPRITE_DICT["ground"],
            HDOOR_TILE: SPRITE_DICT["door"],
            VDOOR_TILE: SPRITE_DICT["door"],
        }

        tile_invisible_sprites = {
            GROUND_TILE: SPRITE_DICT["invisible_ground"],
            VWALL_TILE: SPRITE_DICT["vwall"],
            HWALL_TILE: SPRITE_DICT["hwall"],
            TLWALL_TILE: SPRITE_DICT["twall"],
            BLWALL_TILE: SPRITE_DICT["bwall"],
            TRWALL_TILE: SPRITE_DICT["twall"],
            BRWALL_TILE: SPRITE_DICT["bwall"],
            CORRIDOR_TILE: SPRITE_DICT["invisible_ground"],
            HDOOR_TILE: SPRITE_DICT["door"],
            VDOOR_TILE: SPRITE_DICT["door"],
        }

        tile_components = {
            VWALL_TILE: [],
            HWALL_TILE: [],
            TLWALL_TILE: [],
            BLWALL_TILE: [],
            TRWALL_TILE: [],
            BRWALL_TILE: [],
            GROUND_TILE: [MovableComponent],
            CORRIDOR_TILE: [MovableComponent],
            HDOOR_TILE: [MovableComponent, DoorComponent],
            VDOOR_TILE: [MovableComponent, DoorComponent],
        }

        door_sprites = {
            (HDOOR_TILE, DoorState.OPEN): SPRITE_DICT["hdoor_open"],
            (VDOOR_TILE, DoorState.OPEN): SPRITE_DICT["vdoor_open"]
        }

        label = LabelComponent(0,788,"Dlvl", pygame.Color(254,254,254), pygame.Color(1,1,1))
        self.create_entity(label)

        self.add_processor(GenericUIDrawerProcessor(FONT))
        self.add_processor(DoorProcessor(door_sprites), 8)
        self.add_processor(ViewProcessor(), 7)
        self.add_processor(MoveProcessor(), 6)
        self.add_processor(DungeonGenerator(), 5)
        self.add_processor(DungeonCreator(tile_sprites, tile_invisible_sprites, tile_components), 4)
        self.add_processor(DungeonFiller([player_residents]), 3)
        self.add_processor(InputProcessor(), 2)
        self.add_processor(RenderProcessor(), 1)

        dungeon = DungeonConfig(4, 10, 8, 16, 50, 50)
        self.publish(DungeonGenerationEvent(dungeon))

    def is_running(self) -> bool:
        return self._is_running


def run():
    game_world = GameWorld()
    while game_world.is_running():
        game_world.process()


if __name__ == '__main__':
    import cProfile

    cProfile.run('run()', sort="cumtime")
