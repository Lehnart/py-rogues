import random


class GoldComponent:

    def __init__(self, min_amount: int, max_amount):
        self._min_amount = min_amount
        self._max_amount = max_amount

    def random_amount(self) -> int:
        return random.randint(self._min_amount, self._max_amount)
