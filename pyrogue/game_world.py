import pygame

from roguengine import esper
from roguengine.component.ai import AIComponent, State
from roguengine.component.armor import ArmorComponent
from roguengine.component.armor_slot import ArmorSlotComponent
from roguengine.component.dungeon import VWALL_TILE, HWALL_TILE, TLWALL_TILE, BLWALL_TILE, TRWALL_TILE, BRWALL_TILE, GROUND_TILE, CORRIDOR_TILE, \
    HDOOR_TILE, VDOOR_TILE
from roguengine.component.dungeon_resident import DungeonResidentComponent
from roguengine.component.fighter import FighterComponent, Type
from roguengine.component.gold import GoldComponent
from roguengine.component.goldbag import GoldBagComponent
from roguengine.component.movable import MovableComponent
from roguengine.component.player import PlayerComponent
from roguengine.component.weapon import WeaponComponent
from roguengine.component.weapon_slot import WeaponSlotComponent
from roguengine.component.window import WindowComponent
from roguengine.event.dungeon_generation import DungeonGenerationEvent
from roguengine.processor.ai import AIProcessor
from roguengine.processor.dungeon import DungeonGenerator, DungeonConfig, DungeonCreator, \
    DungeonFiller, DungeonResidents, \
    DungeonResident
from roguengine.processor.fight import FightProcessor
from roguengine.processor.gold import GoldProcessor
from roguengine.processor.input import InputProcessor
from roguengine.processor.logger import LoggerProcessor
from roguengine.processor.move import MoveProcessor
from roguengine.processor.render import RenderProcessor
from roguengine.processor.time import TimeProcessor
from roguengine.processor.ui import UIProcessor
from roguengine.processor.view import ViewProcessor
from roguengine.processor.wear import WearWeaponProcessor, WearArmorProcessor

SPRITE_SHEET: pygame.Surface = pygame.image.load("res/sprites.bmp")


class GameWorld(esper.World):
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

        yellow_char_sprites = get_char_sprites(pygame.Color(128, 128, 0))
        grey_char_sprites = get_char_sprites(pygame.Color(128, 128, 128))

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
            GROUND_TILE: [MovableComponent()],
            CORRIDOR_TILE: [MovableComponent()],
            HDOOR_TILE: [MovableComponent()],
            VDOOR_TILE: [MovableComponent()],
        }

        self.add_processor(AIProcessor(), 13)
        self.add_processor(GoldProcessor(), 12)
        self.add_processor(FightProcessor(), 11)
        self.add_processor(LoggerProcessor(16, 0, grey_char_sprites, 3), 10)
        self.add_processor(TimeProcessor(720, 820, grey_char_sprites), 9)
        self.add_processor(UIProcessor(16, 800, yellow_char_sprites), 8)
        self.add_processor(ViewProcessor(), 7)
        self.add_processor(WearArmorProcessor(), 6)
        self.add_processor(WearWeaponProcessor(), 6)
        self.add_processor(MoveProcessor(), 6)
        self.add_processor(DungeonGenerator(), 5)
        self.add_processor(DungeonCreator(tile_sprites, tile_invisible_sprites, tile_components), 4)
        self.add_processor(DungeonFiller([player_residents, monster_residents, item_residents]), 3)
        self.add_processor(InputProcessor(), 2)
        self.add_processor(RenderProcessor(), 1)

        dungeon = DungeonConfig(5, 25, 5, 10, 50, 50)
        self.publish(DungeonGenerationEvent(dungeon))

        self.get_processor(LoggerProcessor).put("Welcome to the dungeon!")

    def is_running(self) -> bool:
        return self._is_running


def get_sprite(x: int, y: int, w: int, h: int, c: pygame.Color):
    sprite = SPRITE_SHEET.subsurface(pygame.Rect(x, y, w, h))
    sprite: pygame.Surface = sprite.convert()
    oc = sprite.map_rgb(pygame.Color(239, 239, 239))
    c = sprite.map_rgb(c)
    pixel_array = pygame.PixelArray(sprite)
    pixel_array.replace(oc, c)
    sprite = pixel_array.surface
    return sprite


def get_char_sprites(color: pygame.Color):
    return {
        'a': pygame.transform.scale2x(get_sprite(27 * 8, 7, 8, 8, color)),
        'b': pygame.transform.scale2x(get_sprite(28 * 8, 7, 8, 8, color)),
        'c': pygame.transform.scale2x(get_sprite(29 * 8, 7, 8, 8, color)),
        'd': pygame.transform.scale2x(get_sprite(30 * 8, 7, 8, 8, color)),
        'e': pygame.transform.scale2x(get_sprite(31 * 8, 7, 8, 8, color)),
        'f': pygame.transform.scale2x(get_sprite(32 * 8, 7, 8, 8, color)),
        'g': pygame.transform.scale2x(get_sprite(33 * 8, 7, 8, 8, color)),
        'h': pygame.transform.scale2x(get_sprite(34 * 8, 7, 8, 8, color)),
        'i': pygame.transform.scale2x(get_sprite(35 * 8, 7, 8, 8, color)),
        'j': pygame.transform.scale2x(get_sprite(36 * 8, 7, 8, 8, color)),
        'k': pygame.transform.scale2x(get_sprite(37 * 8, 7, 8, 8, color)),
        'l': pygame.transform.scale2x(get_sprite(38 * 8, 7, 8, 8, color)),
        'm': pygame.transform.scale2x(get_sprite(39 * 8, 7, 8, 8, color)),
        'n': pygame.transform.scale2x(get_sprite(40 * 8, 7, 8, 8, color)),
        'o': pygame.transform.scale2x(get_sprite(41 * 8, 7, 8, 8, color)),
        'p': pygame.transform.scale2x(get_sprite(42 * 8, 7, 8, 8, color)),
        'q': pygame.transform.scale2x(get_sprite(43 * 8, 7, 8, 8, color)),
        'r': pygame.transform.scale2x(get_sprite(44 * 8, 7, 8, 8, color)),
        's': pygame.transform.scale2x(get_sprite(45 * 8, 7, 8, 8, color)),
        't': pygame.transform.scale2x(get_sprite(46 * 8, 7, 8, 8, color)),
        'u': pygame.transform.scale2x(get_sprite(47 * 8, 7, 8, 8, color)),
        'v': pygame.transform.scale2x(get_sprite(48 * 8, 7, 8, 8, color)),
        'w': pygame.transform.scale2x(get_sprite(49 * 8, 7, 8, 8, color)),
        'x': pygame.transform.scale2x(get_sprite(50 * 8, 7, 8, 8, color)),
        'y': pygame.transform.scale2x(get_sprite(51 * 8, 7, 8, 8, color)),
        'z': pygame.transform.scale2x(get_sprite(52 * 8, 7, 8, 8, color)),
        'A': pygame.transform.scale2x(get_sprite(1 * 8, 7, 8, 8, color)),
        'B': pygame.transform.scale2x(get_sprite(2 * 8, 7, 8, 8, color)),
        'C': pygame.transform.scale2x(get_sprite(3 * 8, 7, 8, 8, color)),
        'D': pygame.transform.scale2x(get_sprite(4 * 8, 7, 8, 8, color)),
        'E': pygame.transform.scale2x(get_sprite(5 * 8, 7, 8, 8, color)),
        'F': pygame.transform.scale2x(get_sprite(6 * 8, 7, 8, 8, color)),
        'G': pygame.transform.scale2x(get_sprite(7 * 8, 7, 8, 8, color)),
        'H': pygame.transform.scale2x(get_sprite(8 * 8, 7, 8, 8, color)),
        'I': pygame.transform.scale2x(get_sprite(9 * 8, 7, 8, 8, color)),
        'J': pygame.transform.scale2x(get_sprite(10 * 8, 7, 8, 8, color)),
        'K': pygame.transform.scale2x(get_sprite(11 * 8, 7, 8, 8, color)),
        'L': pygame.transform.scale2x(get_sprite(12 * 8, 7, 8, 8, color)),
        'M': pygame.transform.scale2x(get_sprite(13 * 8, 7, 8, 8, color)),
        'N': pygame.transform.scale2x(get_sprite(14 * 8, 7, 8, 8, color)),
        'O': pygame.transform.scale2x(get_sprite(15 * 8, 7, 8, 8, color)),
        'P': pygame.transform.scale2x(get_sprite(16 * 8, 7, 8, 8, color)),
        'Q': pygame.transform.scale2x(get_sprite(17 * 8, 7, 8, 8, color)),
        'R': pygame.transform.scale2x(get_sprite(18 * 8, 7, 8, 8, color)),
        'S': pygame.transform.scale2x(get_sprite(19 * 8, 7, 8, 8, color)),
        'T': pygame.transform.scale2x(get_sprite(20 * 8, 7, 8, 8, color)),
        'U': pygame.transform.scale2x(get_sprite(21 * 8, 7, 8, 8, color)),
        'V': pygame.transform.scale2x(get_sprite(22 * 8, 7, 8, 8, color)),
        'W': pygame.transform.scale2x(get_sprite(23 * 8, 7, 8, 8, color)),
        'X': pygame.transform.scale2x(get_sprite(24 * 8, 7, 8, 8, color)),
        'Y': pygame.transform.scale2x(get_sprite(25 * 8, 7, 8, 8, color)),
        'Z': pygame.transform.scale2x(get_sprite(26 * 8, 7, 8, 8, color)),
        '0': pygame.transform.scale2x(get_sprite(1 * 8, 15, 8, 8, color)),
        '1': pygame.transform.scale2x(get_sprite(2 * 8, 15, 8, 8, color)),
        '2': pygame.transform.scale2x(get_sprite(3 * 8, 15, 8, 8, color)),
        '3': pygame.transform.scale2x(get_sprite(4 * 8, 15, 8, 8, color)),
        '4': pygame.transform.scale2x(get_sprite(5 * 8, 15, 8, 8, color)),
        '5': pygame.transform.scale2x(get_sprite(6 * 8, 15, 8, 8, color)),
        '6': pygame.transform.scale2x(get_sprite(7 * 8, 15, 8, 8, color)),
        '7': pygame.transform.scale2x(get_sprite(8 * 8, 15, 8, 8, color)),
        '8': pygame.transform.scale2x(get_sprite(9 * 8, 15, 8, 8, color)),
        '9': pygame.transform.scale2x(get_sprite(10 * 8, 15, 8, 8, color)),
        '.': pygame.transform.scale2x(get_sprite(11 * 8, 15, 8, 8, color)),
        ',': pygame.transform.scale2x(get_sprite(12 * 8, 15, 8, 8, color)),
        ';': pygame.transform.scale2x(get_sprite(13 * 8, 15, 8, 8, color)),
        ':': pygame.transform.scale2x(get_sprite(14 * 8, 15, 8, 8, color)),
        '-': pygame.transform.scale2x(get_sprite(15 * 8, 15, 8, 8, color)),
        '+': pygame.transform.scale2x(get_sprite(16 * 8, 15, 8, 8, color)),
        '*': pygame.transform.scale2x(get_sprite(17 * 8, 15, 8, 8, color)),
        '/': pygame.transform.scale2x(get_sprite(18 * 8, 15, 8, 8, color)),
        '%': pygame.transform.scale2x(get_sprite(19 * 8, 15, 8, 8, color)),
        '<': pygame.transform.scale2x(get_sprite(20 * 8, 15, 8, 8, color)),
        '>': pygame.transform.scale2x(get_sprite(21 * 8, 15, 8, 8, color)),
        '!': pygame.transform.scale2x(get_sprite(22 * 8, 15, 8, 8, color)),
        '?': pygame.transform.scale2x(get_sprite(23 * 8, 15, 8, 8, color)),
        '^': pygame.transform.scale2x(get_sprite(25 * 8, 15, 8, 8, color)),
        '[': pygame.transform.scale2x(get_sprite(26 * 8, 15, 8, 8, color)),
        ']': pygame.transform.scale2x(get_sprite(27 * 8, 15, 8, 8, color)),
        '(': pygame.transform.scale2x(get_sprite(28 * 8, 15, 8, 8, color)),
        ')': pygame.transform.scale2x(get_sprite(29 * 8, 15, 8, 8, color)),
        '{': pygame.transform.scale2x(get_sprite(30 * 8, 15, 8, 8, color)),
        '#': pygame.transform.scale2x(get_sprite(32 * 8, 15, 8, 8, color)),
        '&': pygame.transform.scale2x(get_sprite(33 * 8, 15, 8, 8, color)),
        '=': pygame.transform.scale2x(get_sprite(34 * 8, 15, 8, 8, color)),
        '\"': pygame.transform.scale2x(get_sprite(35 * 8, 15, 8, 8, color)),
        '\'': pygame.transform.scale2x(get_sprite(36 * 8, 15, 8, 8, color)),
        '@': pygame.transform.scale2x(get_sprite(37 * 8, 15, 8, 8, color)),
        '|': pygame.transform.scale2x(get_sprite(38 * 8, 15, 8, 8, color)),
        '\\': pygame.transform.scale2x(get_sprite(39 * 8, 15, 8, 8, color)),
        '_': pygame.transform.scale2x(get_sprite(42 * 8, 15, 8, 8, color)),
        '~': pygame.transform.scale2x(get_sprite(43 * 8, 15, 8, 8, color)),
        '$': pygame.transform.scale2x(get_sprite(44 * 8, 15, 8, 8, color)),
        ' ': pygame.transform.scale2x(get_sprite(0, 0, 8, 8, color)),
    }


def run():
    game_world = GameWorld()
    while game_world.is_running():
        game_world.process()


if __name__ == '__main__':
    import cProfile

    cProfile.run('run()', sort="cumtime")
