import pygame

from pyangband.font import FONT
from roguengine import rogue_esper
from roguengine.component.label import LabelComponent
from roguengine.component.window import WindowComponent
from roguengine.processor.input import InputProcessor
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
        label = LabelComponent(48, 112, label3_str, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0))
        self.create_entity(label)

        label4_str = "for help, or \'Ctrl-X\' to quit."
        label = LabelComponent(48, 128, label4_str, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0))
        self.create_entity(label)

        label5_str = "Race affects stats and skills, and may confer resistances and abilities."
        label = LabelComponent(48, 160, label5_str, pygame.Color(206, 206, 0), pygame.Color(0, 0, 0))
        self.create_entity(label)

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
