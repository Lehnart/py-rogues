from roguengine.rogue_esper import Event


class StartInputListeningEvent(Event):

    def __init__(self, ent: int):
        super().__init__()
        self.ent = ent


class StopInputListeningEvent(Event):

    def __init__(self, ent: int):
        super().__init__()
        self.ent = ent
