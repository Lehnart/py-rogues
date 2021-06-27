import time


class BlinkingComponent:

    def __init__(self, period: float):
        self._blinking_period = period
        self._last_blinking_time = time.time()
        self._blinking_count = 0

    def get_period(self) -> float:
        return self._blinking_period

    def get_last_blinking_time(self) -> float:
        return self._last_blinking_time

    def get_blinking_count(self) -> int:
        return self._blinking_count

    def blink(self):
        self._last_blinking_time = time.time()
        self._blinking_count += 1
