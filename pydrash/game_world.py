import pygame

from pydrash.font import FONT
from pydrash.sprites import SPRITE_DICT, UI_FRAME_SPRITE, TILE_MAP_SPRITE, RESIDENT_MAP_SPRITE
from roguengine import rogue_esper
from roguengine.systems.ai.processors import AIProcessor
from roguengine.systems.callable.processors import KeyCallableProcessor
from roguengine.systems.dungeon.components import VWALL_TILE, HWALL_TILE, TLWALL_TILE, BLWALL_TILE, TRWALL_TILE, BRWALL_TILE, GROUND_TILE, \
    CORRIDOR_TILE, \
    HDOOR_TILE, VDOOR_TILE, VOID_TILE, DungeonResidentComponent, MovableComponent, BlockComponent, FOREST_TILE, GRASS_TILE, WATER_TILE
from roguengine.systems.dungeon.events import MapCreationEvent
from roguengine.systems.dungeon.processors import DungeonResident, DungeonResidents, MoveProcessor, MapCreatorProcessor
from roguengine.systems.fight.components import FighterComponent, Type, CharacterStatComponent
from roguengine.systems.fight.processors import FightProcessor
from roguengine.systems.gold.components import GoldBagComponent
from roguengine.systems.input.components import InputListenerComponent
from roguengine.systems.input.processors import InputProcessor
from roguengine.systems.log.events import LogEvent
from roguengine.systems.log.processors import LoggerProcessor
from roguengine.systems.look.processors import LookProcessor
from roguengine.systems.player.components import PlayerComponent
from roguengine.systems.player.tools import get_player_entity
from roguengine.systems.render.components import WindowComponent
from roguengine.systems.render.processors import CenteredViewRenderProcessor
from roguengine.systems.text_form.processors import TextFormProcessor
from roguengine.systems.turn_count.processors import TurnCounterProcessor
from roguengine.systems.ui.components import UISpriteComponent, DynamicLabelComponent
from roguengine.systems.ui.processors import BlinkProcessor, UIProcessor
from roguengine.systems.view.components import OpaqueComponent
from roguengine.systems.view.processors import FOVViewProcessor


class GameWorld(rogue_esper.RogueWorld):
    def __init__(self):
        super().__init__()
        self._is_running: bool = True

        window = WindowComponent((800, 800))
        self.create_entity(window)

        player_sprite = SPRITE_DICT["player"]
        player_comps = [
            PlayerComponent(),
            DungeonResidentComponent(),
            GoldBagComponent(),
            InputListenerComponent(),
            FighterComponent(20, 15, 60, Type.HUMAN),
            CharacterStatComponent(10, 10, 10, 10, 10, 10)
        ]
        player_resident = DungeonResident(
            [
                PlayerComponent(),
                DungeonResidentComponent(),
                GoldBagComponent(),
                InputListenerComponent(),
                FighterComponent(20, 15, 60, Type.HUMAN),
                CharacterStatComponent(10, 10, 10, 10, 10, 10)
            ],
            1.,
            1,
            player_sprite
        )
        player_residents = DungeonResidents({1: 1}, [player_resident], 3)

        tile_sprites = {
            VWALL_TILE: SPRITE_DICT["wall"],
            HWALL_TILE: SPRITE_DICT["wall"],
            TLWALL_TILE: SPRITE_DICT["wall"],
            BLWALL_TILE: SPRITE_DICT["wall"],
            TRWALL_TILE: SPRITE_DICT["wall"],
            BRWALL_TILE: SPRITE_DICT["wall"],
            GROUND_TILE: SPRITE_DICT["ground"],
            CORRIDOR_TILE: SPRITE_DICT["corridor"],
            HDOOR_TILE: SPRITE_DICT["corridor"],
            VDOOR_TILE: SPRITE_DICT["corridor"],
            VOID_TILE: SPRITE_DICT["void"],
            FOREST_TILE: SPRITE_DICT["forest"],
            GRASS_TILE: SPRITE_DICT["grass"],
            WATER_TILE: SPRITE_DICT["water"]
        }

        tile_invisible_sprites = {
            VWALL_TILE: SPRITE_DICT["wall"],
            HWALL_TILE: SPRITE_DICT["wall"],
            TLWALL_TILE: SPRITE_DICT["wall"],
            BLWALL_TILE: SPRITE_DICT["wall"],
            TRWALL_TILE: SPRITE_DICT["wall"],
            BRWALL_TILE: SPRITE_DICT["wall"],
            GROUND_TILE: SPRITE_DICT["ground"],
            CORRIDOR_TILE: SPRITE_DICT["corridor"],
            HDOOR_TILE: SPRITE_DICT["corridor"],
            VDOOR_TILE: SPRITE_DICT["corridor"],
            VOID_TILE: SPRITE_DICT["void"],
            FOREST_TILE: SPRITE_DICT["forest"],
            GRASS_TILE: SPRITE_DICT["grass"],
            WATER_TILE: SPRITE_DICT["water"]
        }

        tile_components = {
            VWALL_TILE: [OpaqueComponent, BlockComponent],
            HWALL_TILE: [OpaqueComponent, BlockComponent],
            TLWALL_TILE: [OpaqueComponent, BlockComponent],
            BLWALL_TILE: [OpaqueComponent, BlockComponent],
            TRWALL_TILE: [OpaqueComponent, BlockComponent],
            BRWALL_TILE: [OpaqueComponent, BlockComponent],
            GROUND_TILE: [MovableComponent],
            CORRIDOR_TILE: [MovableComponent],
            HDOOR_TILE: [MovableComponent],
            VDOOR_TILE: [MovableComponent],
            VOID_TILE: [OpaqueComponent],
            FOREST_TILE: [BlockComponent, OpaqueComponent],
            GRASS_TILE: [MovableComponent],
            WATER_TILE: [BlockComponent],
        }

        tile_dict = {
            (0, 85, 28): FOREST_TILE,
            (0, 127, 14): GRASS_TILE,
            (127, 51, 0): CORRIDOR_TILE,
            (28, 27, 84): WATER_TILE,
            (64, 64, 64): VWALL_TILE,
            (128, 128, 128): GROUND_TILE
        }

        self.create_entity(UISpriteComponent(UI_FRAME_SPRITE))

        self.add_processor(
            MapCreatorProcessor(
                TILE_MAP_SPRITE, tile_dict, tile_components, tile_sprites,
                RESIDENT_MAP_SPRITE, {(255, 0, 0): "player"}, {"player": player_sprite}, {"player": player_comps},
                tile_invisible_sprites
            ), 17
        )
        self.add_processor(AIProcessor(), 17)
        self.add_processor(FightProcessor(), 16)
        self.add_processor(TextFormProcessor(), 15)
        self.add_processor(KeyCallableProcessor(), 14)
        self.add_processor(BlinkProcessor(), 13)
        self.add_processor(LookProcessor(640, 0, 160, 800, FONT), 12)
        self.add_processor(LoggerProcessor(16, 738, FONT, 4, pygame.Color(255, 255, 255), pygame.Color(128, 128, 128)), 11)
        self.add_processor(TurnCounterProcessor(), 10)
        self.add_processor(UIProcessor(FONT), 9)
        self.add_processor(FOVViewProcessor(), 7)
        self.add_processor(MoveProcessor(), 6)
        self.add_processor(InputProcessor(), 2)
        self.add_processor(CenteredViewRenderProcessor(16, 16, 608, 720), 1)

        self.publish(MapCreationEvent())
        self.publish(LogEvent("Welcome to the dungeon of Drash!"))

        label = DynamicLabelComponent(650, 32, get_player_state, pygame.Color(254, 254, 254), pygame.Color(1, 1, 1))
        self.create_entity(label)

    def is_running(self) -> bool:
        return self._is_running


def get_player_state(world: rogue_esper.RogueWorld) -> str:
    player_ent = get_player_entity(world)

    if not player_ent:
        return ""

    ui_str = "lvl:"

    player_component = world.component_for_entity(player_ent, PlayerComponent)
    ui_str += str(player_component.level()) + "   \n"

    if world.has_component(player_ent, GoldBagComponent):
        goldbag_component = world.component_for_entity(player_ent, GoldBagComponent)
        ui_str += "$:" + str(goldbag_component.amount()) + " \n"

    if world.has_component(player_ent, FighterComponent):
        fighter_component = world.component_for_entity(player_ent, FighterComponent)
        hp = fighter_component.hp()
        hp_max = fighter_component.hp_max()
        atk = fighter_component.attack()
        arm = fighter_component.defense()
        exp = player_component.exp()

        ui_str += "HP:{}({})\nPw:{}({})\nAC:{}\nXp:{} ".format(hp, hp_max, atk, atk, arm, exp)

    return ui_str


def run():
    game_world = GameWorld()
    while game_world.is_running():
        game_world.process()


if __name__ == '__main__':
    import cProfile

    cProfile.run('run()', sort="cumtime")
