from roguengine.systems.dungeon.events import MoveEvent
from roguengine.systems.input.components import InputListenerComponent
from roguengine.systems.menu.events import MenuSelectEvent
from roguengine.rogue_esper import Processor
from roguengine.systems.ui.components import MenuComponent


class MenuProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        messages = self.world.receive(MoveEvent)
        for msg in messages:
            _, dy = msg.movement.dx_dy()
            if dy == 0:
                continue

            for menu_entity, [menu, _] in self.world.get_components(MenuComponent, InputListenerComponent):
                menu.move_selection(dy)
                self.world.publish(MenuSelectEvent(menu_entity))
