import pygame

from roguengine.component.input_listener import InputListenerComponent
from roguengine.component.menu import MenuComponent
from roguengine.event.key_pressed import KeyPressedEvent
from roguengine.event.menu_select import MenuSelectEvent
from roguengine.event.move import MoveEvent
from roguengine.rogue_esper import Processor


class MenuProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        messages = self.world.receive(MoveEvent)
        for msg in messages:
            _, dy = msg.movement.dx_dy()
            if dy == 0:
                continue

            for _, [menu, _] in self.world.get_components(MenuComponent, InputListenerComponent):
                menu.move_selection(dy)

        messages = self.world.receive(KeyPressedEvent)
        for msg in messages:
            if msg.code != pygame.K_RETURN:
                continue
            self.world.publish(MenuSelectEvent())
