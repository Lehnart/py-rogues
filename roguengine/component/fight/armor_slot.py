from typing import Optional


class ArmorSlotComponent:

    def __init__(self, armor_entity: Optional[int] = None):
        self._armor_entity = armor_entity

    def set_armor(self, armor_entity: int):
        self._armor_entity = armor_entity

    def get_armor(self) -> Optional[int]:
        return self._armor_entity
