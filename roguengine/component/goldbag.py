class GoldBagComponent:

    def __init__(self, amount: int = 0):
        self._amount = amount

    def amount(self) -> int:
        return self._amount

    def add(self, quantity: int):
        self._amount += quantity
