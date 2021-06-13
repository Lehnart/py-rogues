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
