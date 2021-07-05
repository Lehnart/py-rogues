import pygame

from pyangband.font import FONT
from roguengine import rogue_esper
from roguengine.component.input_listener import InputListenerComponent
from roguengine.component.label import LabelComponent
from roguengine.component.menu import MenuComponent
from roguengine.component.window import WindowComponent
from roguengine.processor.input import InputProcessor
from roguengine.processor.menu import MenuProcessor
from roguengine.processor.render import RenderProcessor
from roguengine.processor.ui import UI


class GameWorld(rogue_esper.RogueWorld):
    def __init__(self):
        super().__init__()
        self._is_running: bool = True

        window = WindowComponent((1600, 900))
        self.create_entity(window)

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
        self.create_entity(menu, InputListenerComponent())

        label = LabelComponent(300, 216, "Str:", white, black)
        self.create_entity(label)
        label = LabelComponent(492, 216, "Dex:", white, black)
        self.create_entity(label)
        label = LabelComponent(300, 240, "Int:", white, black)
        self.create_entity(label)
        label = LabelComponent(492, 240, "Con:", white, black)
        self.create_entity(label)
        label = LabelComponent(300, 264, "Wis:", white, black)
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

        self.add_processor(MenuProcessor())
        self.add_processor(UI(FONT))
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
