from roguengine.esper import Event


class FightEvent(Event):

    def __init__(self, attacker: int, defender: int):
        super().__init__()
        self.attacker = attacker
        self.defender = defender
