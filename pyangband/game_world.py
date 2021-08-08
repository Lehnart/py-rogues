from enum import Enum
from typing import Dict

import pygame

from pyangband.font import FONT
from roguengine import rogue_esper
from roguengine.callable.components import CallableComponent
from roguengine.callable.processors import CallableProcessor



from roguengine.input.components import InputListenerComponent
from roguengine.input.processors import InputProcessor
from roguengine.menu.events import MenuSelectEvent
from roguengine.menu.processors import MenuProcessor

from roguengine.render.components import WindowComponent
from roguengine.render.processors import RenderProcessor
from roguengine.ui.components import MenuComponent, LabelComponent, DynamicLabelComponent
from roguengine.ui.processors import UIProcessor


class Race(Enum):
    HUMAN = 0
    HALF_ELF = 1
    ELF = 2
    HOBBIT = 3
    GNOME = 4
    DWARF = 5
    HALF_ORC = 6
    HALF_TROLL = 7
    DUNADAN = 8
    HIGH_ELF = 9
    KOBOLD = 10


RACE_STATS = {
    Race.HUMAN: {"str": 0, "dex": 0, "int": 0, "con": 0, "wis": 0},
    Race.HALF_ELF: {"str": 0, "dex": 1, "int": 1, "con": -1, "wis": -1},
    Race.ELF: {"str": -1, "dex": 1, "int": 2, "con": -1, "wis": -1},
    Race.HOBBIT: {"str": -2, "dex": 3, "int": 2, "con": 2, "wis": 1},
    Race.GNOME: {"str": -1, "dex": 2, "int": 2, "con": 1, "wis": 0},
    Race.DWARF: {"str": 2, "dex": -2, "int": -3, "con": 2, "wis": 2},
    Race.HALF_ORC: {"str": 2, "dex": 0, "int": -1, "con": 1, "wis": 0},
    Race.HALF_TROLL: {"str": 4, "dex": -4, "int": -4, "con": 3, "wis": -2},
    Race.DUNADAN: {"str": 1, "dex": 2, "int": 2, "con": 3, "wis": 2},
    Race.HIGH_ELF: {"str": 1, "dex": 3, "int": 3, "con": 1, "wis": -1},
    Race.KOBOLD: {"str": -1, "dex": 2, "int": -1, "con": 2, "wis": 0}
}

RACE_FIGHT_STATS = {
    Race.HUMAN: {"hit": 0, "shoot": 0, "throw": 0, "hit_die": 10, "xp_mod": 100},
    Race.HALF_ELF: {"hit": -1, "shoot": 5, "throw": 5, "hit_die": 10, "xp_mod": 120},
    Race.ELF: {"hit": -5, "shoot": 15, "throw": 15, "hit_die": 9, "xp_mod": 120},
    Race.HOBBIT: {"hit": -10, "shoot": 20, "throw": 20, "hit_die": 7, "xp_mod": 120},
    Race.GNOME: {"hit": -8, "shoot": 12, "throw": 12, "hit_die": 8, "xp_mod": 120},
    Race.DWARF: {"hit": 15, "shoot": 0, "throw": 0, "hit_die": 11, "xp_mod": 120},
    Race.HALF_ORC: {"hit": 12, "shoot": -5, "throw": -5, "hit_die": 10, "xp_mod": 120},
    Race.HALF_TROLL: {"hit": 20, "shoot": -10, "throw": -10, "hit_die": 12, "xp_mod": 120},
    Race.DUNADAN: {"hit": 15, "shoot": 10, "throw": 10, "hit_die": 10, "xp_mod": 120},
    Race.HIGH_ELF: {"hit": 10, "shoot": 25, "throw": 25, "hit_die": 10, "xp_mod": 145},
    Race.KOBOLD: {"hit": -5, "shoot": 10, "throw": 10, "hit_die": 8, "xp_mod": 120}
}

RACE_SKILLS = {
    Race.HUMAN: {"disarm": (0, 0), "devices": 0, "save": 0, "stealth": 0, "infravision": 0, "digging": 0, "search": 0},
    Race.HALF_ELF: {"disarm": (2, 2), "devices": 3, "save": 3, "stealth": 1, "infravision": 20, "digging": 0, "search": 3},
    Race.ELF: {"disarm": (5, 5), "devices": 6, "save": 6, "stealth": 2, "infravision": 30, "digging": 0, "search": 6},
    Race.HOBBIT: {"disarm": (15, 15), "devices": 18, "save": 18, "stealth": 4, "infravision": 40, "digging": 0, "search": 6},
    Race.GNOME: {"disarm": (10, 10), "devices": 22, "save": 12, "stealth": 3, "infravision": 40, "digging": 0, "search": 4},
    Race.DWARF: {"disarm": (2, 2), "devices": 9, "save": 9, "stealth": -1, "infravision": 50, "digging": 40, "search": 2},
    Race.HALF_ORC: {"disarm": (-3, -3), "devices": -3, "save": -3, "stealth": -1, "infravision": 30, "digging": 0, "search": -3},
    Race.HALF_TROLL: {"disarm": (-5, -5), "devices": -8, "save": -8, "stealth": -2, "infravision": 30, "digging": 0, "search": -9},
    Race.DUNADAN: {"disarm": (4, 4), "devices": 5, "save": 5, "stealth": 1, "infravision": 0, "digging": 0, "search": 3},
    Race.HIGH_ELF: {"disarm": (4, 4), "devices": 20, "save": 20, "stealth": 2, "infravision": 40, "digging": 0, "search": 10},
    Race.KOBOLD: {"disarm": (10, 10), "devices": 5, "save": 0, "stealth": 3, "infravision": 50, "digging": 0, "search": 10},
}


class RaceSelection:

    def __init__(self, race_stats: Dict, race_fight_stats: Dict, race_skills: Dict):
        self._race_stats = race_stats
        self._race_fight_stats = race_fight_stats
        self._race_skills = race_skills
        self.current_race = None

    def _get_stat(self, carac_str: str):
        if self.current_race is None:
            return ""
        stat = self._race_stats[self.current_race][carac_str]
        if stat >= 0:
            return "+" + str(stat)
        return str(stat)

    def str(self, _world: rogue_esper.RogueWorld) -> str:
        return self._get_stat("str")

    def dex(self, _world: rogue_esper.RogueWorld) -> str:
        return self._get_stat("dex")

    def int(self, _world: rogue_esper.RogueWorld) -> str:
        return self._get_stat("int")

    def con(self, _world: rogue_esper.RogueWorld) -> str:
        return self._get_stat("con")

    def wis(self, _world: rogue_esper.RogueWorld) -> str:
        return self._get_stat("wis")

    def update_selection(self, event: MenuSelectEvent, world: rogue_esper.RogueWorld):
        menu_component = world.component_for_entity(event.menu_entity, MenuComponent)
        select_index = menu_component.get_selected()
        if select_index is not None:
            self.current_race = Race(select_index)


class GameWorld(rogue_esper.RogueWorld):
    def __init__(self):
        super().__init__()
        self._is_running: bool = True

        window = WindowComponent((1600, 900))
        self.create_entity(window)

        race_selection = RaceSelection(RACE_STATS, RACE_FIGHT_STATS, RACE_SKILLS)

        label1_str = "Please select your character traits from the menu below :"
        label = LabelComponent(48, 48, label1_str, pygame.Color(0, 255, 255), pygame.Color(0, 0, 0))
        self.create_entity(label)

        label2_str = "Use the movement keys to scroll the menu, Enter to select the current menu item, \"*\" for a"
        label = LabelComponent(48, 96, label2_str, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0))
        self.create_entity(label)

        label3_str = "random menu item, \'ESC\' to step back through the birth process, \'=\' for the birth options, \'?\'"
        label = LabelComponent(48, 120, label3_str, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0))
        self.create_entity(label)

        label4_str = "for help, or \'Ctrl-X\' to quit."
        label = LabelComponent(48, 144, label4_str, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0))
        self.create_entity(label)

        label5_str = "Race affects stats and skills, and may confer resistances and abilities."
        label = LabelComponent(48, 184, label5_str, pygame.Color(206, 206, 0), pygame.Color(0, 0, 0))
        self.create_entity(label)

        label_strs = [
            "a) Human",
            "b) Half-Elf",
            "c) Elf",
            "d) Hobbit",
            "e) Gnome",
            "f) Dwarf",
            "g) Half-Orc",
            "h) Half-Troll",
            "i) Dunadan",
            "j) High-Elf",
            "k) Kobold"
        ]
        white = pygame.Color(255, 255, 255)
        black = pygame.Color(0, 0, 0)
        cyan = pygame.Color(0, 255, 255)
        n_labels = len(label_strs)
        menu = MenuComponent(48, 216, 24, label_strs, [white for _ in range(n_labels)], [black for _ in range(n_labels)], cyan)
        cc = CallableComponent(MenuSelectEvent, race_selection.update_selection)
        self.create_entity(menu, InputListenerComponent(), cc)

        label = LabelComponent(300, 216, "Str:", white, black)
        self.create_entity(label)
        label = DynamicLabelComponent(412, 216, race_selection.str, white, black)
        self.create_entity(label)

        label = LabelComponent(492, 216, "Dex:", white, black)
        self.create_entity(label)
        label = DynamicLabelComponent(604, 216, race_selection.dex, white, black)
        self.create_entity(label)

        label = LabelComponent(300, 240, "Int:", white, black)
        self.create_entity(label)
        label = DynamicLabelComponent(412, 240, race_selection.int, white, black)
        self.create_entity(label)

        label = LabelComponent(492, 240, "Con:", white, black)
        self.create_entity(label)
        label = DynamicLabelComponent(604, 240, race_selection.con, white, black)
        self.create_entity(label)

        label = LabelComponent(300, 264, "Wis:", white, black)
        self.create_entity(label)
        label = DynamicLabelComponent(412, 264, race_selection.wis, white, black)
        self.create_entity(label)

        label = LabelComponent(300, 312, "Hit/Shoot/Throw:", white, black)
        self.create_entity(label)
        label = LabelComponent(300, 336, "Hit die:", white, black)
        self.create_entity(label)
        label = LabelComponent(556, 336, "XP mod:", white, black)
        self.create_entity(label)
        label = LabelComponent(300, 360, "Disarm:", white, black)
        self.create_entity(label)
        label = LabelComponent(636, 360, "Devices:", white, black)
        self.create_entity(label)
        label = LabelComponent(300, 384, "Save:", white, black)
        self.create_entity(label)
        label = LabelComponent(556, 384, "Stealth:", white, black)
        self.create_entity(label)
        label = LabelComponent(300, 408, "Infravision:", white, black)
        self.create_entity(label)
        label = LabelComponent(300, 432, "Digging:", white, black)
        self.create_entity(label)
        label = LabelComponent(300, 456, "Search:", white, black)
        self.create_entity(label)

        self.add_processor(CallableProcessor())
        self.add_processor(MenuProcessor())
        self.add_processor(UIProcessor(FONT))
        self.add_processor(InputProcessor())
        self.add_processor(RenderProcessor())

    def is_running(self) -> bool:
        return self._is_running


def run():
    game_world = GameWorld()
    while game_world.is_running():
        game_world.process()


if __name__ == '__main__':
    import cProfile

    cProfile.run('run()', sort="cumtime")
