from typing import Dict, Tuple

import pygame

from roguengine.component.dungeon import DungeonComponent
from roguengine.component.fighter import FighterComponent
from roguengine.component.goldbag import GoldBagComponent
from roguengine.component.label import LabelComponent
from roguengine.component.player import PlayerComponent
from roguengine.component.window import WindowComponent
from roguengine.esper import Processor


class Font:

    def __init__(self, char_sprite_sheet: pygame.Surface, char_width: int, char_height: int, map_char_to_xy: Dict[str, Tuple[int, int]]):
        self._sheet = char_sprite_sheet
        self._char_width = char_width
        self._char_height = char_height
        self._map_char_to_xy = map_char_to_xy

    def _get_colored_char_sprite(self, char_sprite: pygame.Surface, bkgd_color: pygame.Color, font_color: pygame.Color) -> pygame.Surface:
        bkgd_oc = char_sprite.map_rgb(pygame.Color(255, 255, 255))
        bkgd_c = char_sprite.map_rgb(bkgd_color)

        font_oc = char_sprite.map_rgb(pygame.Color(0, 0, 0))
        font_c = char_sprite.map_rgb(font_color)

        pixel_array = pygame.PixelArray(char_sprite)
        pixel_array.replace(bkgd_oc, bkgd_c)
        pixel_array.replace(font_oc, font_c)

        sprite = pixel_array.surface
        return sprite

    def _get_char_sprite(self, px: int, py: int) -> pygame.Surface:
        sprite = self._sheet.subsurface(pygame.Rect(px, py, self._char_width, self._char_height))
        sprite: pygame.Surface = sprite.convert()
        return sprite

    def get_char(self, character: str, font_color: pygame.Color, bkgd_color: pygame.Color) -> pygame.Surface:
        x, y = self._map_char_to_xy[character]
        char_sprite = self._get_char_sprite(x, y)
        return self._get_colored_char_sprite(char_sprite, bkgd_color, font_color)


class GenericUIDrawerProcessor(Processor):

    def __init__(self, font: Font):
        super().__init__()
        self.font = font

    def process(self):

        window = self.world.get_component(WindowComponent)
        assert (len(window) == 1)
        window_surface = window[0][1].surface()

        label_components = self.world.get_component(LabelComponent)
        for _, label in label_components:
            x, y = label.get_position()
            s = label.get_label()
            for c in s:
                sprite = self.font.get_char(c, label.get_font_color(), label.get_bkgd_color())
                window_surface.blit(sprite, (x, y))
                x += sprite.get_width()


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
