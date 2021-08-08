class TextFormComponent:

    def __init__(self):
        self._text = ""

    def add_char(self, s: str):
        self._text += s

    def del_char(self):
        self._text = self._text[:-1]

    def get(self) -> str:
        return self._text
