from typing import Optional

import pygame
from pygame import Color

from pynethack.font import FONT
from pynethack.sprites import SPRITE_DICT
from roguengine import rogue_esper
from roguengine.systems.ai.components import AIComponent, State
from roguengine.systems.ai.processors import AIProcessor
from roguengine.systems.callable.components import KeyCallableComponent
from roguengine.systems.callable.events import KeyPressedEvent
from roguengine.systems.callable.processors import KeyCallableProcessor

from roguengine.systems.dungeon.components import VWALL_TILE, HWALL_TILE, TLWALL_TILE, BLWALL_TILE, TRWALL_TILE, BRWALL_TILE, GROUND_TILE, \
    CORRIDOR_TILE, \
    HDOOR_TILE, VDOOR_TILE, VOID_TILE, DungeonResidentComponent, DoorComponent, DoorState, MovableComponent
from roguengine.systems.dungeon.events import DungeonGenerationEvent
from roguengine.systems.dungeon.processors import DungeonGenerator, DungeonResident, DungeonResidents, DoorProcessor, DungeonCreator, DungeonFiller, \
    DungeonConfig, MoveProcessor
from roguengine.systems.fight.components import FighterComponent, Type, CharacterStatComponent
from roguengine.systems.fight.processors import FightProcessor
from roguengine.systems.gold.components import GoldBagComponent
from roguengine.systems.input.components import InputListenerComponent
from roguengine.systems.input.processors import InputProcessor
from roguengine.systems.log.events import LogEvent
from roguengine.systems.log.processors import LoggerProcessor
from roguengine.systems.look.processors import LookProcessor
from roguengine.systems.player.components import PlayerComponent

from roguengine.systems.render.components import WindowComponent
from roguengine.systems.render.processors import RenderProcessor
from roguengine.systems.text_form.components import TextFormComponent
from roguengine.systems.text_form.processors import TextFormProcessor
from roguengine.systems.turn_count.components import TurnCountComponent
from roguengine.systems.turn_count.processors import TurnCounterProcessor
from roguengine.systems.ui.components import LabelComponent, BlinkingComponent, DynamicLabelComponent, GaugeComponent
from roguengine.systems.ui.processors import BlinkProcessor, UIProcessor
from roguengine.systems.view.components import OpaqueComponent
from roguengine.systems.view.processors import FOVViewProcessor


class GameWorld(rogue_esper.RogueWorld):
    def __init__(self):
        super().__init__()
        self._is_running: bool = True

        window = WindowComponent((800, 800))
        self.create_entity(window)

        lc2 = LabelComponent(358, 384, "PYNETHACK", pygame.Color(255, 0, 0), pygame.Color(0, 0, 0))
        self.create_entity(lc2)

        lc = LabelComponent(350, 400, "PRESS ENTER", pygame.Color(255, 0, 0), pygame.Color(0, 0, 0))
        bc = BlinkingComponent(0.250)
        kc = KeyCallableComponent(KeyPressedEvent("\u000D"), self._enter_name)
        self.create_entity(lc, bc, kc)

        self.add_processor(AIProcessor(), 17)
        self.add_processor(FightProcessor(), 16)
        self.add_processor(TextFormProcessor(), 15)
        self.add_processor(KeyCallableProcessor(), 14)
        self.add_processor(BlinkProcessor(), 13)
        self.add_processor(LookProcessor(640, 0, 160, 800, FONT), 12)
        self.add_processor(LoggerProcessor(0, 0, FONT, 3, pygame.Color(255, 255, 255), pygame.Color(128, 128, 128)), 11)
        self.add_processor(TurnCounterProcessor(), 10)
        self.add_processor(UIProcessor(FONT), 9)
        self.add_processor(FOVViewProcessor(), 7)
        self.add_processor(MoveProcessor(), 6)
        self.add_processor(DungeonGenerator(), 5)
        self.add_processor(InputProcessor(), 2)
        self.add_processor(RenderProcessor(), 1)

    def _enter_name(self):

        for e, _ in self.get_component(LabelComponent):
            self.delete_entity(e, True)

        lc = LabelComponent(358, 384, "Enter your name : ", pygame.Color(128, 128, 128), pygame.Color(0, 0, 0))
        kc = KeyCallableComponent(KeyPressedEvent("\u000D"), self._create_game)
        self.create_entity(lc, kc)

        tfc = TextFormComponent()
        dlc = DynamicLabelComponent(358, 400, get_text_form, pygame.Color(128, 128, 128), pygame.Color(0, 0, 0))
        self.create_entity(tfc, dlc)

    def _create_game(self):

        e, t = self.get_component(TextFormComponent)[0]
        player_name = t.get()

        for e, _ in self.get_component(LabelComponent):
            self.delete_entity(e)
        for e, _ in self.get_component(DynamicLabelComponent):
            self.delete_entity(e)

        player_sprite = SPRITE_DICT["player"]
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

        spider_sprite = SPRITE_DICT["spider"]
        spider_resident = DungeonResident(
            [DungeonResidentComponent(), FighterComponent(20, 10, 15), AIComponent(State.PASSIVE)],
            0.5,
            100,
            spider_sprite
        )
        monster_residents = DungeonResidents(
            {0: 0.2, 1: 0.5, 2: 0.2},
            [spider_resident],
            3
        )

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
            VOID_TILE: SPRITE_DICT["void"]
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
            VOID_TILE: SPRITE_DICT["void"]
        }

        tile_components = {
            VWALL_TILE: [OpaqueComponent],
            HWALL_TILE: [OpaqueComponent],
            TLWALL_TILE: [OpaqueComponent],
            BLWALL_TILE: [OpaqueComponent],
            TRWALL_TILE: [OpaqueComponent],
            BRWALL_TILE: [OpaqueComponent],
            GROUND_TILE: [MovableComponent],
            CORRIDOR_TILE: [MovableComponent],
            HDOOR_TILE: [MovableComponent, DoorComponent, OpaqueComponent],
            VDOOR_TILE: [MovableComponent, DoorComponent, OpaqueComponent],
            VOID_TILE: [OpaqueComponent]
        }

        door_sprites = {
            (HDOOR_TILE, DoorState.OPEN): SPRITE_DICT["hdoor_open"],
            (VDOOR_TILE, DoorState.OPEN): SPRITE_DICT["vdoor_open"]
        }

        self.create_ui(player_name)

        self.add_processor(DoorProcessor(door_sprites), 8)
        self.add_processor(DungeonCreator(tile_sprites, tile_invisible_sprites, tile_components, 0, 48), 4)
        self.add_processor(DungeonFiller([player_residents, monster_residents], 0, 48), 3)

        dungeon = DungeonConfig(4, 10, 8, 16, 40, 45)
        self.publish(DungeonGenerationEvent(dungeon))

        self.publish(LogEvent("[Odin has chosen you to recover the Amulet of Yendor for Him.]"))
        self.publish(LogEvent("Welcome to pynethack! you are a neutral human."))

    def is_running(self) -> bool:
        return self._is_running

    def create_ui(self, player_name: str):
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
            player_name
        )
        self.add_component(ui_ent, gauge)


def get_text_form(world: rogue_esper.RogueWorld) -> str:
    for e, tfc in world.get_component(TextFormComponent):
        return tfc.get()


def get_player(world: rogue_esper.RogueWorld) -> Optional[int]:
    players = world.get_components(PlayerComponent)
    if not players:
        return None

    player, [_] = players[0]
    return player


def get_player_stats(world: rogue_esper.RogueWorld) -> str:
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


def get_player_state(world: rogue_esper.RogueWorld) -> str:
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


def get_player_hp(world: rogue_esper.RogueWorld) -> float:
    player_ent = get_player(world)

    if not player_ent:
        return 0.

    if world.has_component(player_ent, FighterComponent):
        fighter_component = world.component_for_entity(player_ent, FighterComponent)
        hp = fighter_component.hp()

        return hp
    return 0.


def get_player_hp_max(world: rogue_esper.RogueWorld) -> float:
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
