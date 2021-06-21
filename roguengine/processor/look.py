from typing import List

import pygame

from roguengine.component.input_listener import InputListenerComponent
from roguengine.component.player import PlayerComponent
from roguengine.component.position import PositionComponent
from roguengine.component.sprite import VisibleSpriteComponent
from roguengine.esper import Processor
from roguengine.event.look import LookInputEvent


class LookProcessor(Processor):

    def __init__(self):
        super().__init__()
        self._is_in_look_mode = False
        self._cursor_sprite = None

    def process(self):
        look_inputs: List[LookInputEvent] = self.world.receive(LookInputEvent)
        for _ in look_inputs:
            if not self._is_in_look_mode:
                self._active_look_mode()
            else:
                self._unactive_look_mode()

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
        self.world.create_entity(PositionComponent(x, y), InputListenerComponent(), VisibleSpriteComponent(px, py, self._cursor_sprite, 3))

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
