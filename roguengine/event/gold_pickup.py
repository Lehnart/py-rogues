from roguengine.rogue_esper import Event


class GoldPickUpEvent(Event):

    def __init__(self, gold_ent: int):
        super().__init__()
        self.gold_ent = gold_ent
