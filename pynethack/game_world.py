from typing import Optional

import pygame
from pygame import Color

from pynethack.font import FONT
from pynethack.sprites import SPRITE_DICT
from roguengine import esper
from roguengine.component.character_stats import CharacterStatComponent
from roguengine.component.door import DoorComponent, DoorState
from roguengine.component.dungeon import VWALL_TILE, HWALL_TILE, TLWALL_TILE, BLWALL_TILE, TRWALL_TILE, BRWALL_TILE, GROUND_TILE, CORRIDOR_TILE, \
    HDOOR_TILE, VDOOR_TILE
from roguengine.component.dungeon_resident import DungeonResidentComponent
from roguengine.component.dynamic_label import DynamicLabelComponent
from roguengine.component.fighter import FighterComponent
from roguengine.component.gauge import GaugeComponent
from roguengine.component.goldbag import GoldBagComponent
from roguengine.component.movable import MovableComponent
from roguengine.component.player import PlayerComponent
from roguengine.component.turn_count import TurnCountComponent
from roguengine.component.window import WindowComponent
from roguengine.event.dungeon_generation import DungeonGenerationEvent
from roguengine.processor.door import DoorProcessor
from roguengine.processor.dungeon import DungeonResident, DungeonResidents, DungeonGenerator, DungeonCreator, DungeonFiller, DungeonConfig
from roguengine.processor.input import InputProcessor
from roguengine.processor.move import MoveProcessor
from roguengine.processor.render import RenderProcessor
from roguengine.processor.turn_counter import TurnCounterProcessor
from roguengine.processor.ui import GenericUIDrawerProcessor
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
                GoldBagComponent(),
                FighterComponent(5, 6, 60),
                CharacterStatComponent(10, 10, 10, 10, 10, 10)
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

        self.create_ui()

        self.add_processor(TurnCounterProcessor(), 10)
        self.add_processor(GenericUIDrawerProcessor(FONT), 9)
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

    def create_ui(self):
        label = DynamicLabelComponent(0, 788, get_player_state, pygame.Color(254, 254, 254), pygame.Color(1, 1, 1))
        ui_ent = self.create_entity(label)
        self.add_component(ui_ent, TurnCountComponent())

        label = DynamicLabelComponent(248, 776, get_player_stats, pygame.Color(254, 254, 254), pygame.Color(1, 1, 1))
        ui_ent = self.create_entity(label)

        gauge = GaugeComponent(
            0,
            776,
            240,
            12,
            pygame.Color(1, 1, 1),
            [(0.2, Color(254, 0, 0)), (0.4, Color(254, 170, 70)), (0.6, Color(247, 247, 69)), (0.8, Color(37, 186, 52)), (1., Color(254, 254, 254))],
            get_player_hp,
            get_player_hp_max,
            "setoh"
        )
        self.add_component(ui_ent, gauge)




def get_player(world: esper.World) -> Optional[int]:
    players = world.get_components(PlayerComponent)
    if not players:
        return None

    player, [_] = players[0]
    return player


def get_player_stats(world: esper.World) -> str:
    player_ent = get_player(world)

    if not player_ent:
        return ""

    stat_component = world.component_for_entity(player_ent, CharacterStatComponent)
    ui_str = "St:{} Dx:{} Co:{} In:{} Wi:{} Ch:{}".format(
        stat_component.strength(),
        stat_component.dexterity(),
        stat_component.constitution(),
        stat_component.intelligence(),
        stat_component.wisdom(),
        stat_component.charism()
    )
    return ui_str


def get_player_state(world: esper.World) -> str:
    player_ent = get_player(world)

    if not player_ent:
        return ""

    ui_str = "Dlvl:"

    player_component = world.component_for_entity(player_ent, PlayerComponent)
    ui_str += str(player_component.level()) + "   "

    if world.has_component(player_ent, GoldBagComponent):
        goldbag_component = world.component_for_entity(player_ent, GoldBagComponent)
        ui_str += "$:" + str(goldbag_component.amount()) + " "

    if world.has_component(player_ent, FighterComponent):
        fighter_component = world.component_for_entity(player_ent, FighterComponent)
        hp = fighter_component.hp()
        hp_max = fighter_component.hp_max()
        atk = fighter_component.attack()
        arm = fighter_component.defense()
        exp = player_component.exp()

        t: TurnCountComponent = world.get_component(TurnCountComponent)[0][1]

        ui_str += "HP:{}({}) Pw:{}({}) AC:{} Xp:{} T:{}".format(hp, hp_max, atk, atk, arm, exp, t.get_turn())

    return ui_str


def get_player_hp(world: esper.World) -> float:
    player_ent = get_player(world)

    if not player_ent:
        return 0.

    if world.has_component(player_ent, FighterComponent):
        fighter_component = world.component_for_entity(player_ent, FighterComponent)
        hp = fighter_component.hp()

        return hp
    return 0.


def get_player_hp_max(world: esper.World) -> float:
    player_ent = get_player(world)

    if not player_ent:
        return 0.

    if world.has_component(player_ent, FighterComponent):
        fighter_component = world.component_for_entity(player_ent, FighterComponent)
        hp_max = fighter_component.hp_max()

        return hp_max
    return 0.


def run():
    game_world = GameWorld()
    while game_world.is_running():
        game_world.process()


if __name__ == '__main__':
    import cProfile

    cProfile.run('run()', sort="cumtime")
