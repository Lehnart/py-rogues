from typing import Dict

import pygame

from roguengine.component.dungeon import DungeonComponent
from roguengine.component.fighter import FighterComponent
from roguengine.component.goldbag import GoldBagComponent
from roguengine.component.player import PlayerComponent
from roguengine.component.window import WindowComponent
from roguengine.esper import Processor


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
