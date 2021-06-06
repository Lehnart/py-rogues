from typing import Dict

import pygame

from roguengine.component.dungeon import DungeonComponent
from roguengine.component.fighter import FighterComponent
from roguengine.component.gauge import GaugeComponent
from roguengine.component.goldbag import GoldBagComponent
from roguengine.component.player import PlayerComponent
from roguengine.component.window import WindowComponent
from roguengine.esper import Processor


class Font:

    def __init__(self, char_sprite_sheet: pygame.Surface, char_width: int, char_height: int):
        self._sheet = char_sprite_sheet
        self._char_width = char_width
        self._char_height = char_height

    def _get_char_sprite(self, px: int, py: int, bkgd_color: pygame.Color, font_color: pygame.Color) -> pygame.Surface:
        sprite = self._sheet.subsurface(pygame.Rect(px, py, self._char_width, self._char_height))
        sprite: pygame.Surface = sprite.convert()

        bkgd_oc = sprite.map_rgb(pygame.Color(255, 255, 255))
        bkgd_c = sprite.map_rgb(bkgd_color)

        font_oc = sprite.map_rgb(pygame.Color(0, 0, 0))
        font_c = sprite.map_rgb(font_color)

        pixel_array = pygame.PixelArray(sprite)
        pixel_array.replace(bkgd_oc, bkgd_c)
        pixel_array.replace(font_oc, font_c)

        sprite = pixel_array.surface
        return sprite

    def get_char(self, character: str, font_color: pygame.Color, bkgd_color: pygame.Color) -> pygame.Surface:
        return self.get_char_sprite_dict(font_color, bkgd_color)[character]

    def get_char_sprite_dict(self, font_color: pygame.Color, bkgd_color: pygame.Color) -> Dict[str, pygame.Surface]:
        return {
            'a': self._get_char_sprite(4, 16, font_color, bkgd_color),
            'b': self._get_char_sprite(8, 16, font_color, bkgd_color),
            'c': self._get_char_sprite(12, 16, font_color, bkgd_color),
            'd': self._get_char_sprite(16, 16, font_color, bkgd_color),
            'e': self._get_char_sprite(20, 16, font_color, bkgd_color),
            'f': self._get_char_sprite(24, 16, font_color, bkgd_color),
            'g': self._get_char_sprite(28, 16, font_color, bkgd_color),
            'h': self._get_char_sprite(32, 16, font_color, bkgd_color),
            'i': self._get_char_sprite(36, 16, font_color, bkgd_color),
            'j': self._get_char_sprite(40, 16, font_color, bkgd_color),
            'k': self._get_char_sprite(44, 16, font_color, bkgd_color),
            'l': self._get_char_sprite(48, 16, font_color, bkgd_color),
            'm': self._get_char_sprite(52, 16, font_color, bkgd_color),
            'n': self._get_char_sprite(56, 16, font_color, bkgd_color),
            'o': self._get_char_sprite(60, 16, font_color, bkgd_color),
            'p': self._get_char_sprite(64, 16, font_color, bkgd_color),
            'q': self._get_char_sprite(68, 16, font_color, bkgd_color),
            'r': self._get_char_sprite(72, 16, font_color, bkgd_color),
            's': self._get_char_sprite(76, 16, font_color, bkgd_color),
            't': self._get_char_sprite(80, 16, font_color, bkgd_color),
            'u': self._get_char_sprite(84, 16, font_color, bkgd_color),
            'v': self._get_char_sprite(88, 16, font_color, bkgd_color),
            'w': self._get_char_sprite(92, 16, font_color, bkgd_color),
            'x': self._get_char_sprite(96, 16, font_color, bkgd_color),
            'y': self._get_char_sprite(100, 16, font_color, bkgd_color),
            'z': self._get_char_sprite(104, 16, font_color, bkgd_color),
            'A': self._get_char_sprite(4, 8, font_color, bkgd_color),
            'B': self._get_char_sprite(8, 8, font_color, bkgd_color),
            'C': self._get_char_sprite(12, 8, font_color, bkgd_color),
            'D': self._get_char_sprite(16, 8, font_color, bkgd_color),
            'E': self._get_char_sprite(20, 8, font_color, bkgd_color),
            'F': self._get_char_sprite(24, 8, font_color, bkgd_color),
            'G': self._get_char_sprite(28, 8, font_color, bkgd_color),
            'H': self._get_char_sprite(32, 8, font_color, bkgd_color),
            'I': self._get_char_sprite(36, 8, font_color, bkgd_color),
            'J': self._get_char_sprite(40, 8, font_color, bkgd_color),
            'K': self._get_char_sprite(44, 8, font_color, bkgd_color),
            'L': self._get_char_sprite(48, 8, font_color, bkgd_color),
            'M': self._get_char_sprite(52, 8, font_color, bkgd_color),
            'N': self._get_char_sprite(56, 8, font_color, bkgd_color),
            'O': self._get_char_sprite(60, 8, font_color, bkgd_color),
            'P': self._get_char_sprite(64, 8, font_color, bkgd_color),
            'Q': self._get_char_sprite(68, 8, font_color, bkgd_color),
            'R': self._get_char_sprite(72, 8, font_color, bkgd_color),
            'S': self._get_char_sprite(76, 8, font_color, bkgd_color),
            'T': self._get_char_sprite(80, 8, font_color, bkgd_color),
            'U': self._get_char_sprite(84, 8, font_color, bkgd_color),
            'V': self._get_char_sprite(88, 8, font_color, bkgd_color),
            'W': self._get_char_sprite(92, 8, font_color, bkgd_color),
            'X': self._get_char_sprite(96, 8, font_color, bkgd_color),
            'Y': self._get_char_sprite(100, 8, font_color, bkgd_color),
            'Z': self._get_char_sprite(104, 8, font_color, bkgd_color),
            # '0': get_sprite(1 * 8, 15, 8, 8, color),
            # '1': get_sprite(2 * 8, 15, 8, 8, color),
            # '2': get_sprite(3 * 8, 15, 8, 8, color),
            # '3': get_sprite(4 * 8, 15, 8, 8, color),
            # '4': get_sprite(5 * 8, 15, 8, 8, color),
            # '5': get_sprite(6 * 8, 15, 8, 8, color),
            # '6': get_sprite(7 * 8, 15, 8, 8, color),
            # '7': get_sprite(8 * 8, 15, 8, 8, color),
            # '8': get_sprite(9 * 8, 15, 8, 8, color),
            # '9': get_sprite(10 * 8, 15, 8, 8, color),
            # '.': get_sprite(11 * 8, 15, 8, 8, color),
            # ',': get_sprite(12 * 8, 15, 8, 8, color),
            # ';': get_sprite(13 * 8, 15, 8, 8, color),
            # ':': get_sprite(14 * 8, 15, 8, 8, color),
            # '-': get_sprite(15 * 8, 15, 8, 8, color),
            # '+': get_sprite(16 * 8, 15, 8, 8, color),
            # '*': get_sprite(17 * 8, 15, 8, 8, color),
            # '/': get_sprite(18 * 8, 15, 8, 8, color),
            # '%': get_sprite(19 * 8, 15, 8, 8, color),
            # '<': get_sprite(20 * 8, 15, 8, 8, color),
            # '>': get_sprite(21 * 8, 15, 8, 8, color),
            # '!': get_sprite(22 * 8, 15, 8, 8, color),
            # '?': get_sprite(23 * 8, 15, 8, 8, color),
            # '^': get_sprite(25 * 8, 15, 8, 8, color),
            # '[': get_sprite(26 * 8, 15, 8, 8, color),
            # ']': get_sprite(27 * 8, 15, 8, 8, color),
            # '(': get_sprite(28 * 8, 15, 8, 8, color),
            # ')': get_sprite(29 * 8, 15, 8, 8, color),
            # '{': get_sprite(30 * 8, 15, 8, 8, color),
            # '#': get_sprite(32 * 8, 15, 8, 8, color),
            # '&': get_sprite(33 * 8, 15, 8, 8, color),
            # '=': get_sprite(34 * 8, 15, 8, 8, color),
            # '\"': get_sprite(35 * 8, 15, 8, 8, color),
            # '\'': get_sprite(36 * 8, 15, 8, 8, color),
            # '@': get_sprite(37 * 8, 15, 8, 8, color),
            # '|': get_sprite(38 * 8, 15, 8, 8, color),
            # '\\': get_sprite(39 * 8, 15, 8, 8, color),
            # '_': get_sprite(42 * 8, 15, 8, 8, color),
            # '~': get_sprite(43 * 8, 15, 8, 8, color),
            # '$': get_sprite(44 * 8, 15, 8, 8, color),
            # ' ': get_sprite(0, 0, 8, 8, color),
        }


class GenericUIDrawerProcessor(Processor):

    def __init__(self, font : Font):
        super().__init__()
        self._font = font

    def process(self):
        gauge_components = self.world.get_components(GaugeComponent)
        for gauge in gauge_components:
            pass


class UIProcessor(Processor):

    def __init__(self, px: int, py: int, char_sprite_dict: Dict[str, pygame.Surface]):
        super().__init__()
        self._char_sprite_dict = char_sprite_dict
        self._px = px
        self._py = py

    def process(self):

        player_components = self.world.get_components(PlayerComponent, FighterComponent, GoldBagComponent)
        dungeons = self.world.get_component(DungeonComponent)

        if not player_components or not dungeons:
            return

        player_component: PlayerComponent = player_components[0][1][0]
        fighter_component: FighterComponent = player_components[0][1][1]
        gold_component: GoldBagComponent = player_components[0][1][2]
        dungeon_component: DungeonComponent = dungeons[0][1]
        for window_entity, [window_component] in self.world.get_components(WindowComponent):
            window_surface = window_component.surface()
            string = "Level:{} HP:{}/{} Str:{} Gold:{} Armor:{} Exp:{}/{}".format(
                dungeon_component.level(),
                fighter_component.hp(),
                fighter_component.hp_max(),
                fighter_component.attack(),
                gold_component.amount(),
                fighter_component.defense(),
                player_component.level(),
                player_component.exp()
            )
            x = self._px
            y = self._py
            for c in string:
                if c not in self._char_sprite_dict:
                    continue
                sprite = self._char_sprite_dict[c]
                window_surface.blit(sprite, (x, y))
                x += sprite.get_width()
