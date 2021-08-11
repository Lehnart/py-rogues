from roguengine.rogue_esper import Event


class MenuMoveEvent(Event):

    def __init__(self, dx: int, dy: int):
        super().__init__()
        self.dx = dx
        self.dy = dy


class MenuSelectEvent(Event):

    def __init__(self, menu_entity: int):
        super().__init__()
        self.menu_entity = menu_entity
