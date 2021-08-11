from roguengine.rogue_esper import Event


class TransparentEvent(Event):

    def __init__(self, ent: int):
        super().__init__()
        self.ent = ent
