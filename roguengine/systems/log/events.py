from roguengine.rogue_esper import Event


class LogEvent(Event):

    def __init__(self, msg: str):
        super().__init__()
        self.msg = msg
