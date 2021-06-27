import sys

import pygame

from roguengine.component.input_listener import InputListenerComponent
from roguengine.esper import Processor
from roguengine.event.ai import AIEvent
from roguengine.event.dungeon_generation import DungeonGenerationEvent
from roguengine.event.key_pressed import KeyPressedEvent
from roguengine.event.look import LookInputEvent
from roguengine.event.move import MoveEvent, Movement
from roguengine.event.start_game_event import StartGameEvent
from roguengine.event.wear import WearWeaponEvent, WearArmorEvent


class InputProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:

                self.world.publish(KeyPressedEvent(event.unicode))

                if event.key == pygame.K_r:
                    self.world.publish(DungeonGenerationEvent(None))
                    continue

                if event.key == pygame.K_RETURN:
                    self.world.publish(StartGameEvent())

                listeners = self.world.get_components(InputListenerComponent)
                if not listeners:
                    continue
                listener, _ = listeners[0]

                if event.key == pygame.K_DOWN:
                    self.world.publish(MoveEvent(listener, Movement(0, 1)))

                if event.key == pygame.K_UP:
                    self.world.publish(MoveEvent(listener, Movement(0, -1)))

                if event.key == pygame.K_LEFT:
                    self.world.publish(MoveEvent(listener, Movement(-1, 0)))

                if event.key == pygame.K_RIGHT:
                    self.world.publish(MoveEvent(listener, Movement(1, 0)))

                if event.key == pygame.K_l:
                    self.world.publish(LookInputEvent())

                if event.key == pygame.K_w:
                    self.world.publish(WearWeaponEvent(listener))
                    self.world.publish(WearArmorEvent(listener))
                    self.world.publish(AIEvent())
