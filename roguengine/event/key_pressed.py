from roguengine.esper import Event


class KeyPressedEvent(Event):

    def __init__(self, code: str):
        super().__init__()
        self.code = code
