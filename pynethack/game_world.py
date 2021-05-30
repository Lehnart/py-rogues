from pynethack.sprites import SPRITE_DICT
from roguengine import esper
from roguengine.component.dungeon import Tile
from roguengine.component.dungeon_resident import DungeonResidentComponent
from roguengine.component.movable import MovableComponent
from roguengine.component.player import PlayerComponent
from roguengine.component.window import WindowComponent
from roguengine.event.dungeon_generation import DungeonGenerationEvent
from roguengine.processor.dungeon import DungeonResident, DungeonResidents, DungeonGenerator, DungeonCreator, DungeonFiller, DungeonConfig
from roguengine.processor.input import InputProcessor
from roguengine.processor.move import MoveProcessor
from roguengine.processor.render import RenderProcessor
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
            Tile.WALL: SPRITE_DICT["wall"],
            Tile.GROUND: SPRITE_DICT["ground"],
            Tile.HDOOR: SPRITE_DICT["door"],
            Tile.VDOOR: SPRITE_DICT["door"],
            Tile.CORRIDOR: SPRITE_DICT["corridor"]
        }

        tile_components = {
            Tile.WALL: [],
            Tile.GROUND: [MovableComponent()],
            Tile.HDOOR: [MovableComponent()],
            Tile.VDOOR: [MovableComponent()],
            Tile.CORRIDOR: [MovableComponent()],
        }

        self.add_processor(ViewProcessor(), 7)
        self.add_processor(MoveProcessor(), 6)
        self.add_processor(DungeonGenerator(), 5)
        self.add_processor(DungeonCreator(tile_sprites, tile_components), 4)
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
