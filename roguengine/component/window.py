from typing import Tuple

import pygame


class WindowComponent:

    def __init__(self, size: Tuple[int, int]):
        pygame.init()
        self._window_surface: pygame.Surface = pygame.display.set_mode(size)

    def surface(self) -> pygame.Surface:
        return self._window_surface
