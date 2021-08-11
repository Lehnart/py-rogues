import sys

import pygame

import roguengine.systems.callable.events as callable_events
import roguengine.systems.text_form.events as text_form_events
from roguengine.rogue_esper import Processor
from roguengine.systems.ai.events import AIEvent
from roguengine.systems.dungeon.events import DungeonGenerationEvent, Movement, MoveEvent
from roguengine.systems.fight.events import WearWeaponEvent, WearArmorEvent
from roguengine.systems.input.components import InputListenerComponent
from roguengine.systems.input.events import StartInputListeningEvent, StopInputListeningEvent
from roguengine.systems.look.events import LookInputEvent
from roguengine.systems.menu.events import MenuMoveEvent


class InputProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):

        for msg in self.world.receive(StartInputListeningEvent):
            self.world.add_component(msg.ent, InputListenerComponent())

        for msg in self.world.receive(StopInputListeningEvent):
            self.world.remove_component(msg.ent, InputListenerComponent)

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
                    self.world.publish(MoveEvent(listener, Movement(0, 1)))
                    self.world.publish(MenuMoveEvent(0, 1))

                if event.key == pygame.K_UP:
                    self.world.publish(MoveEvent(listener, Movement(0, -1)))
                    self.world.publish(MenuMoveEvent(0, -1))

                if event.key == pygame.K_LEFT:
                    self.world.publish(MoveEvent(listener, Movement(-1, 0)))
                    self.world.publish(MenuMoveEvent(-1, 0))

                if event.key == pygame.K_RIGHT:
                    self.world.publish(MoveEvent(listener, Movement(1, 0)))
                    self.world.publish(MenuMoveEvent(1, 0))

                if event.key == pygame.K_l:
                    self.world.publish(LookInputEvent())

                if event.key == pygame.K_w:
                    self.world.publish(WearWeaponEvent(listener))
                    self.world.publish(WearArmorEvent(listener))
                    self.world.publish(AIEvent())
