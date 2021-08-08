from roguengine.rogue_esper import Event


class MenuSelectEvent(Event):

    def __init__(self, menu_entity: int):
        super().__init__()
        self.menu_entity = menu_entity
