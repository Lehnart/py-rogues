from typing import List

import pygame

from roguengine.component.input.input_listener import InputListenerComponent
from roguengine.component.look_cursor import LookCursorComponent
from roguengine.component.player import PlayerComponent
from roguengine.component.position import PositionComponent
from roguengine.component.sprite import VisibleSpriteComponent
from roguengine.component.visible import VisibleComponent
from roguengine.component.window.window import WindowComponent
from roguengine.event.look import LookInputEvent
from roguengine.rogue_esper import Processor
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
        pos_component = self.world.component_for_entity(cursor_ent, PositionComponent)
        x, y = pos_component.xy()
        entities = self._get_entities_at(x, y)

        windows = self.world.get_components(WindowComponent)
        assert (len(windows) == 1)
        window_entity, [window_component] = windows[0]
        window_surface = window_component.surface()

        y = self._y0
        for ent in entities:
            components = self.world.components_for_entity(ent)
            if not any(isinstance(c, VisibleComponent) for c in components):
                continue

            component_strs = [type(c).__name__ for c in components]
            for s in component_strs:
                self._font.draw_string(s, self._x0, y, window_surface, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0))
                y += self._font.get_char_height()
            y += self._font.get_char_height()

    def _active_look_mode(self):

        if not self._cursor_sprite:
            self._create_cursor_sprite()

        players = self.world.get_component(PlayerComponent)
        assert (len(players) == 1)
        player_ent, _ = players[0]

        self.world.remove_component(player_ent, InputListenerComponent)

        sprite = self.world.component_for_entity(player_ent, VisibleSpriteComponent)
        pos = self.world.component_for_entity(player_ent, PositionComponent)
        x, y = pos.xy()
        px, py = sprite.top_left_pixel_position()
        self.world.create_entity(
            PositionComponent(x, y),
            InputListenerComponent(),
            VisibleSpriteComponent(px, py, self._cursor_sprite, 3),
            LookCursorComponent()
        )

        self._is_in_look_mode = True

    def _unactive_look_mode(self):
        listeners = self.world.get_component(InputListenerComponent)
        assert (len(listeners) == 1)
        listener_ent, _ = listeners[0]

        self.world.delete_entity(listener_ent, True)

        players = self.world.get_component(PlayerComponent)
        assert (len(players) == 1)
        player_ent, _ = players[0]
        self.world.add_component(player_ent, InputListenerComponent())

        self._is_in_look_mode = False

    def _create_cursor_sprite(self):
        size = (16, 16)

        empty_surface = pygame.Surface(size, pygame.SRCALPHA, 32)
        empty_surface = empty_surface.convert_alpha()
        pygame.draw.rect(empty_surface, pygame.Color(255, 0, 0), pygame.Rect(0, 0, 16, 16), 2)
        self._cursor_sprite = empty_surface

    def _get_entities_at(self, x: int, y: int):
        entities = []
        for ent, (pos, *_) in self.world.get_components(PositionComponent):
            if pos.xy() == (x, y):
                entities.append(ent)
        return entities
