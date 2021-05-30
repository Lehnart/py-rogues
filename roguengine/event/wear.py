from roguengine.esper import Event


class WearArmorEvent(Event):

    def __init__(self, slot_entity: int):
        super().__init__()
        self.slot_entity = slot_entity


class WearWeaponEvent(Event):

    def __init__(self, slot_entity: int):
        super().__init__()
        self.slot_entity = slot_entity
