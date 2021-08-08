import sys

import pygame

from roguengine.ai.events import AIEvent
from roguengine.dungeon.events import DungeonGenerationEvent, Movement, MoveEvent
from roguengine.fight.events import WearWeaponEvent, WearArmorEvent

from roguengine.input.components import InputListenerComponent
from roguengine.look.events import LookInputEvent
from roguengine.rogue_esper import Processor
import roguengine.text_form.events as text_form_events
import roguengine.callable.events as callable_events


class InputProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:

                self.world.publish(text_form_events.KeyPressedEvent(event.unicode))
                self.world.publish(callable_events.KeyPressedEvent(event.unicode))

                if event.key == pygame.K_r:
                    self.world.publish(DungeonGenerationEvent(None))
                    continue

                listeners = self.world.get_components(InputListenerComponent)
                if not listeners:
                    continue
                listener, _ = listeners[0]

                if event.key == pygame.K_DOWN:
                    self.world.publish(MoveEvent(listener, Movement(0, 1), True))

                if event.key == pygame.K_UP:
                    self.world.publish(MoveEvent(listener, Movement(0, -1), True))

                if event.key == pygame.K_LEFT:
                    self.world.publish(MoveEvent(listener, Movement(-1, 0), True))

                if event.key == pygame.K_RIGHT:
                    self.world.publish(MoveEvent(listener, Movement(1, 0), True))

                if event.key == pygame.K_l:
                    self.world.publish(LookInputEvent())

                if event.key == pygame.K_w:
                    self.world.publish(WearWeaponEvent(listener))
                    self.world.publish(WearArmorEvent(listener))
                    self.world.publish(AIEvent())
