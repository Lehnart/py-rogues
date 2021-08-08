import random


class GoldComponent:

    def __init__(self, min_amount: int, max_amount):
        self._min_amount = min_amount
        self._max_amount = max_amount

    def random_amount(self) -> int:
        return random.randint(self._min_amount, self._max_amount)


class GoldBagComponent:

    def __init__(self, amount: int = 0):
        self._amount = amount

    def amount(self) -> int:
        return self._amount

    def add(self, quantity: int):
        self._amount += quantity
