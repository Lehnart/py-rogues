from typing import Optional


class WeaponSlotComponent:

    def __init__(self, weapon_entity: Optional[int] = None):
        self._weapon_entity = weapon_entity

    def set_weapon(self, weapon_entity: int):
        self._weapon_entity = weapon_entity

    def get_weapon(self) -> Optional[int]:
        return self._weapon_entity
