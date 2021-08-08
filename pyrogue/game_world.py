from typing import Optional

import pygame

from pyrogue.font import FONT
from roguengine import rogue_esper
from roguengine.component.ai import AIComponent, State
from roguengine.dungeon.components import *

from roguengine.component.movable import MovableComponent
from roguengine.component.player import PlayerComponent
from roguengine.component.window.window import WindowComponent
from roguengine.dungeon.events import DungeonGenerationEvent
from roguengine.dungeon.processors import DungeonResident, DungeonResidents, DungeonGenerator, DungeonCreator, DungeonFiller, DungeonConfig
from roguengine.fight.components import FighterComponent, WeaponSlotComponent, ArmorSlotComponent, Type, WeaponComponent, ArmorComponent
from roguengine.fight.processors import FightProcessor
from roguengine.gold.components import GoldBagComponent, GoldComponent
from roguengine.gold.processors import GoldProcessor
from roguengine.input.components import InputListenerComponent
from roguengine.input.processors import InputProcessor
from roguengine.processor.ai import AIProcessor

from roguengine.processor.move import MoveProcessor
from roguengine.processor.render import RenderProcessor
from roguengine.processor.view import RoomViewProcessor
from roguengine.processor.wear import WearWeaponProcessor, WearArmorProcessor
from roguengine.processor.window.logger import LoggerProcessor
from roguengine.processor.window.time import TimeProcessor
from roguengine.ui.components import DynamicLabelComponent
from roguengine.ui.processors import UIProcessor

SPRITE_SHEET: pygame.Surface = pygame.image.load("res/sprites.bmp")


class GameWorld(rogue_esper.RogueWorld):
    def __init__(self):
        super().__init__()
        self._is_running: bool = True

        window = WindowComponent((800, 840))
        self.create_entity(window)

        player_sprite = pygame.transform.scale2x(get_sprite(56, 200, 8, 8, pygame.Color(155, 71, 102)))
        player_resident = DungeonResident(
            [
                PlayerComponent(1),
                FighterComponent(16, 5, 12),
                DungeonResidentComponent(),
                GoldBagComponent(0),
                FighterComponent(10, 5, 15, Type.HUMAN),
                WeaponSlotComponent(),
                ArmorSlotComponent(),
                InputListenerComponent(),
            ],
            1.,
            1,
            player_sprite
        )
        player_residents = DungeonResidents({1: 1}, [player_resident], 3)

        kobold_sprite = pygame.transform.scale2x(get_sprite(8, 184, 8, 8, pygame.Color(71, 102, 155)))
        kobold_resident = DungeonResident(
            [DungeonResidentComponent(), FighterComponent(10, 5, 15), AIComponent(State.PASSIVE)],
            0.3,
            100,
            kobold_sprite
        )

        zombie_sprite = pygame.transform.scale2x(get_sprite(40, 184, 8, 8, pygame.Color(71, 155, 102)))
        zombie_resident = DungeonResident(
            [DungeonResidentComponent(), FighterComponent(10, 5, 15), AIComponent(State.GUARDING)],
            0.3,
            100,
            zombie_sprite
        )

        gargoyle_sprite = pygame.transform.scale2x(get_sprite(8, 200, 8, 8, pygame.Color(155, 155, 155)))
        gargoyle_resident = DungeonResident(
            [DungeonResidentComponent(), FighterComponent(10, 5, 15), AIComponent(State.GUARDING)],
            0.3,
            100,
            gargoyle_sprite
        )
        monster_residents = DungeonResidents(
            {0: 0.2, 1: 0.5, 2: 0.2, 3: 0.1},
            [kobold_resident, zombie_resident, gargoyle_resident],
            3
        )

        gold_sprite = pygame.transform.scale2x(get_sprite(344, 40, 8, 8, pygame.Color(172, 172, 0)))
        gold_resident = DungeonResident([DungeonResidentComponent(), GoldComponent(0, 100)], 0.3, 100, gold_sprite)

        dagger_sprite = pygame.transform.scale2x(get_sprite(8, 72, 8, 8, pygame.Color(128, 128, 128)))
        dagger_component = WeaponComponent(1)
        dagger_resident = DungeonResident([DungeonResidentComponent(), dagger_component], 0.3, 1, dagger_sprite)

        sblade_sprite = pygame.transform.scale2x(get_sprite(24, 72, 8, 8, pygame.Color(128, 128, 128)))
        sblade_component = WeaponComponent(2)
        sblade_resident = DungeonResident([DungeonResidentComponent(), sblade_component], 0.2, 1, sblade_sprite)

        rapier_sprite = pygame.transform.scale2x(get_sprite(40, 72, 8, 8, pygame.Color(128, 128, 128)))
        rapier_component = WeaponComponent(3)
        rapier_resident = DungeonResident([DungeonResidentComponent(), rapier_component], 0.05, 1, rapier_sprite)

        sword_sprite = pygame.transform.scale2x(get_sprite(88, 72, 8, 8, pygame.Color(128, 128, 128)))
        sword_component = WeaponComponent(4)
        sword_resident = DungeonResident([DungeonResidentComponent(), sword_component], 0.025, 1, sword_sprite)

        shirt_sprite = pygame.transform.scale2x(get_sprite(168, 56, 8, 8, pygame.Color(128, 128, 128)))
        shirt_component = ArmorComponent(1)
        shirt_resident = DungeonResident([DungeonResidentComponent(), shirt_component], 0.3, 1, shirt_sprite)

        leather_sprite = pygame.transform.scale2x(get_sprite(184, 56, 8, 8, pygame.Color(128, 128, 128)))
        leather_component = ArmorComponent(2)
        leather_resident = DungeonResident([DungeonResidentComponent(), leather_component], 0.3, 1, leather_sprite)

        chain_sprite = pygame.transform.scale2x(get_sprite(200, 56, 8, 8, pygame.Color(128, 128, 128)))
        chain_component = ArmorComponent(3)
        chain_resident = DungeonResident([DungeonResidentComponent(), chain_component], 0.3, 1, chain_sprite)

        item_residents = DungeonResidents(
            {0: 0.4, 1: 0.3, 2: 0.2, 3: 0.1},
            [gold_resident, dagger_resident, sblade_resident, rapier_resident, sword_resident, shirt_resident, leather_resident, chain_resident],
            2
        )

        wall_sprite = pygame.transform.scale2x(get_sprite(32 * 8, 2 * 8, 8, 8, pygame.Color(80, 80, 100)))
        ground_sprite = pygame.transform.scale2x(get_sprite(11 * 8, 2 * 8, 8, 8, pygame.Color(0, 192, 32)))
        hdoor_sprite = pygame.transform.scale2x(get_sprite(46 * 8, 2 * 8, 8, 8, pygame.Color(135, 113, 69)))
        vdoor_sprite = pygame.transform.scale2x(get_sprite(45 * 8, 2 * 8, 8, 8, pygame.Color(135, 113, 69)))
        corridor_sprite = pygame.transform.scale2x(get_sprite(41 * 8, 2 * 8, 8, 8, pygame.Color(140, 140, 140)))

        tile_sprites = {
            VWALL_TILE: wall_sprite,
            HWALL_TILE: wall_sprite,
            TLWALL_TILE: wall_sprite,
            BLWALL_TILE: wall_sprite,
            TRWALL_TILE: wall_sprite,
            BRWALL_TILE: wall_sprite,
            GROUND_TILE: ground_sprite,
            CORRIDOR_TILE: corridor_sprite,
            HDOOR_TILE: hdoor_sprite,
            VDOOR_TILE: vdoor_sprite,
        }

        tile_invisible_sprites = {
            VWALL_TILE: wall_sprite,
            HWALL_TILE: wall_sprite,
            TLWALL_TILE: wall_sprite,
            BLWALL_TILE: wall_sprite,
            TRWALL_TILE: wall_sprite,
            BRWALL_TILE: wall_sprite,
            GROUND_TILE: ground_sprite,
            CORRIDOR_TILE: corridor_sprite,
            HDOOR_TILE: hdoor_sprite,
            VDOOR_TILE: vdoor_sprite,
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
            HDOOR_TILE: [MovableComponent],
            VDOOR_TILE: [MovableComponent],
        }

        self.create_ui()

        self.add_processor(UIProcessor(FONT), 14)
        self.add_processor(AIProcessor(), 13)
        self.add_processor(GoldProcessor(), 12)
        self.add_processor(FightProcessor(), 11)
        self.add_processor(LoggerProcessor(16, 0, FONT, 3, pygame.Color(128, 128, 128), pygame.Color(128, 128, 128)), 10)
        self.add_processor(TimeProcessor(720, 824, FONT), 9)
        self.add_processor(RoomViewProcessor(), 7)
        self.add_processor(WearArmorProcessor(), 6)
        self.add_processor(WearWeaponProcessor(), 6)
        self.add_processor(MoveProcessor(), 6)
        self.add_processor(DungeonGenerator(), 5)
        self.add_processor(DungeonCreator(tile_sprites, tile_invisible_sprites, tile_components, 0, 48), 4)
        self.add_processor(DungeonFiller([player_residents, monster_residents, item_residents], 0, 48), 3)
        self.add_processor(InputProcessor(), 2)
        self.add_processor(RenderProcessor(), 1)

        dungeon = DungeonConfig(5, 25, 5, 10, 50, 47)
        self.publish(DungeonGenerationEvent(dungeon))

        self.get_processor(LoggerProcessor).put("Welcome to the dungeon!")

    def is_running(self) -> bool:
        return self._is_running

    def create_ui(self):
        label = DynamicLabelComponent(16, 800, get_player_state, pygame.Color(128, 128, 0), pygame.Color(1, 1, 1))
        self.create_entity(label)


def get_player(world: rogue_esper.RogueWorld) -> Optional[int]:
    players = world.get_components(PlayerComponent)
    if not players:
        return None

    player, [_] = players[0]
    return player


def get_player_state(world: rogue_esper.RogueWorld) -> str:
    player_ent = get_player(world)

    if not player_ent:
        return ""

    ui_str = "Level:1 "

    player_component = world.component_for_entity(player_ent, PlayerComponent)
    goldbag_component = world.component_for_entity(player_ent, GoldBagComponent)

    if world.has_component(player_ent, FighterComponent):
        fighter_component = world.component_for_entity(player_ent, FighterComponent)
        hp = fighter_component.hp()
        hp_max = fighter_component.hp_max()
        atk = fighter_component.attack()
        arm = fighter_component.defense()
        exp = player_component.exp()

        ui_str += "HP:{}/{} Str:{} Gold:{} Armor:{} Exp:{}/{}".format(hp, hp_max, atk, goldbag_component.amount(), arm, player_component.level(), exp)

    return ui_str


def get_sprite(x: int, y: int, w: int, h: int, c: pygame.Color):
    sprite = SPRITE_SHEET.subsurface(pygame.Rect(x, y, w, h))
    sprite: pygame.Surface = sprite.convert()
    oc = sprite.map_rgb(pygame.Color(239, 239, 239))
    c = sprite.map_rgb(c)
    pixel_array = pygame.PixelArray(sprite)
    pixel_array.replace(oc, c)
    sprite = pixel_array.surface
    return sprite


def run():
    game_world = GameWorld()
    while game_world.is_running():
        game_world.process()


if __name__ == '__main__':
    import cProfile

    cProfile.run('run()', sort="cumtime")
