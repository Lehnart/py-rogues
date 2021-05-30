from roguengine.esper import Event


class GoldPickUpEvent(Event):

    def __init__(self, gold_ent: int):
        super().__init__()
        self.gold_ent = gold_ent
