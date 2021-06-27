from typing import List

from .esper import esper


class Processor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self, *args, **kwargs):
        raise NotImplementedError


class MessageQueue:

    def __init__(self):
        self._queue = {}

    def add(self, key: str, message: object):
        if key not in self._queue:
            self._queue[key] = []
        self._queue[key].append([message, 0])

    def tick(self):
        for key in self._queue.keys():
            for message in self._queue[key]:
                message[1] += 1

        for key in self._queue.keys():
            self._queue[key] = [msg for msg in self._queue[key] if msg[1] < 2]

    def get(self, key: str) -> List:
        if key not in self._queue:
            return []
        return [msg[0] for msg in self._queue[key] if msg[1] == 1]


class Event:

    def __init__(self):
        pass

    def key(self) -> str:
        return self.__class__.__name__


class RogueWorld(esper.World):
    def __init__(self):
        super().__init__()
        self._message_queue = MessageQueue()

    def _process(self, *args, **kwargs):
        self._message_queue.tick()
        super()._process()

    def publish(self, event: Event):
        self._message_queue.add(event.key(), event)

    def receive(self, event_class) -> List:
        return self._message_queue.get(event_class.__name__)
