from roguengine.rogue_esper import Processor
from roguengine.systems.input.tools import is_listening
from roguengine.systems.menu.events import MenuSelectEvent, MenuMoveEvent
from roguengine.systems.ui.components import MenuComponent


class MenuProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        messages = self.world.receive(MenuMoveEvent)
        for msg in messages:
            _, dy = msg.dx, msg.dy
            if dy == 0:
                continue

            for menu_entity, [menu] in self.world.get_components(MenuComponent):
                if not is_listening(self.world, menu_entity):
                    continue
                menu.move_selection(dy)
                self.world.publish(MenuSelectEvent(menu_entity))
