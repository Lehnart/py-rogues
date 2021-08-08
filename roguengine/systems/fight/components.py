from enum import Enum
from typing import Optional


class Type(Enum):
    MONSTER = 0,
    HUMAN = 1


class ArmorComponent:

    def __init__(self, defense: int):
        self._defense_bonus = defense

    def defense_bonus(self) -> int:
        return self._defense_bonus


class ArmorSlotComponent:

    def __init__(self, armor_entity: Optional[int] = None):
        self._armor_entity = armor_entity

    def set_armor(self, armor_entity: int):
        self._armor_entity = armor_entity

    def get_armor(self) -> Optional[int]:
        return self._armor_entity


class WeaponComponent:

    def __init__(self, atk: int):
        self._attack_bonus = atk

    def attack_bonus(self) -> int:
        return self._attack_bonus


class WeaponSlotComponent:

    def __init__(self, weapon_entity: Optional[int] = None):
        self._weapon_entity = weapon_entity

    def set_weapon(self, weapon_entity: int):
        self._weapon_entity = weapon_entity

    def get_weapon(self) -> Optional[int]:
        return self._weapon_entity


class CharacterStatComponent:

    def __init__(self, strength: int, dexterity: int, constitution: int, intelligence: int, wisdom: int, charism: int):
        self._st = strength
        self._dx = dexterity
        self._co = constitution
        self._in = intelligence
        self._wi = wisdom
        self._ch = charism

    def strength(self) -> int:
        return self._st

    def dexterity(self) -> int:
        return self._dx

    def constitution(self) -> int:
        return self._co

    def intelligence(self) -> int:
        return self._in

    def wisdom(self) -> int:
        return self._wi

    def charism(self) -> int:
        return self._ch


class FighterComponent:

    def __init__(self, attack: int, defense: int, hp: int, type: Type = Type.MONSTER):
        self._attack = attack
        self._defense = defense
        self._hp = hp
        self._hp_max = hp
        self._type = type
        self._last_attacker = None

    def set_last_attacker(self, ent: int):
        self._last_attacker = ent

    def last_attacker(self) -> Optional[int]:
        return self._last_attacker

    def hp(self) -> int:
        return self._hp

    def hp_max(self) -> int:
        return self._hp_max

    def attack(self) -> int:
        return self._attack

    def defense(self) -> int:
        return self._defense

    def damage(self, damage: int):
        self._hp -= damage

    def type(self) -> Type:
        return self._type

