from roguengine.rogue_esper import Event


class FightEvent(Event):

    def __init__(self, attacker: int, defender: int):
        super().__init__()
        self.attacker = attacker
        self.defender = defender


class WearArmorEvent(Event):

    def __init__(self, slot_entity: int):
        super().__init__()
        self.slot_entity = slot_entity


class WearWeaponEvent(Event):

    def __init__(self, slot_entity: int):
        super().__init__()
        self.slot_entity = slot_entity
