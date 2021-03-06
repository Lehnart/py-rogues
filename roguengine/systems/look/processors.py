from typing import List

import pygame

from roguengine.rogue_esper import Processor
from roguengine.systems.dungeon.events import SetPositionEvent
from roguengine.systems.dungeon.tools import get_entities_at, get_position
from roguengine.systems.input.events import StopInputListeningEvent, StartInputListeningEvent
from roguengine.systems.look.components import LookCursorComponent
from roguengine.systems.look.events import LookInputEvent
from roguengine.systems.player.tools import get_player_entity
from roguengine.systems.render.events import DrawStringEvent, CreateSpriteEvent
from roguengine.systems.render.tools import get_sprite_position
from roguengine.systems.view.tools import is_visible
from roguengine.util.font import Font


class LookProcessor(Processor):

    def __init__(self, x0: int, y0: int, w: int, h: int, font: Font):
        super().__init__()
        self._x0 = x0
        self._y0 = y0
        self._w = w
        self._h = h
        self._font = font

        self._is_in_look_mode = False
        self._cursor_sprite = None

    def process(self):
        look_inputs: List[LookInputEvent] = self.world.receive(LookInputEvent)
        for _ in look_inputs:
            if not self._is_in_look_mode:
                self._active_look_mode()
            else:
                self._unactive_look_mode()

        cursors = self.world.get_component(LookCursorComponent)
        if not cursors:
            return
        assert (len(cursors) == 1)

        cursor_ent, _ = cursors[0]
        pos = get_position(self.world, cursor_ent)
        if pos is None:
            return

        x, y = pos
        entities = get_entities_at(self.world, x, y)

        y = self._y0
        for ent in entities:
            if not is_visible(self.world, ent):
                continue

            components = self.world.components_for_entity(ent)
            component_strs = [type(c).__name__ for c in components]
            for s in component_strs:
                self.world.publish(DrawStringEvent(s, self._x0, y, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0), self._font))
                y += self._font.get_char_height()
            y += self._font.get_char_height()

    def _active_look_mode(self):

        if not self._cursor_sprite:
            self._create_cursor_sprite()

        player_ent = get_player_entity(self.world)
        x, y = get_position(self.world, player_ent)
        px, py = get_sprite_position(self.world, player_ent)

        new_ent = self.world.create_entity(LookCursorComponent())
        self.world.publish(SetPositionEvent(new_ent, x, y))
        self.world.publish(StopInputListeningEvent(player_ent))
        self.world.publish(StartInputListeningEvent(new_ent))
        self.world.publish(CreateSpriteEvent(new_ent, px, py, self._cursor_sprite, 3))

        self._is_in_look_mode = True

    def _unactive_look_mode(self):
        listeners = self.world.get_component(LookCursorComponent)
        assert (len(listeners) == 1)
        listener_ent, _ = listeners[0]
        self.world.delete_entity(listener_ent, True)

        ent = get_player_entity(self.world)
        self.world.publish(StartInputListeningEvent(ent))

        self._is_in_look_mode = False

    def _create_cursor_sprite(self):
        size = (16, 16)

        empty_surface = pygame.Surface(size, pygame.SRCALPHA, 32)
        empty_surface = empty_surface.convert_alpha()
        pygame.draw.rect(empty_surface, pygame.Color(255, 0, 0), pygame.Rect(0, 0, 16, 16), 2)
        self._cursor_sprite = empty_surface
