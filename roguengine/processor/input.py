import sys

import pygame

from roguengine.component.fighter import FighterComponent
from roguengine.component.player import PlayerComponent
from roguengine.esper import Processor
from roguengine.event.ai import AIEvent
from roguengine.event.dungeon_generation import DungeonGenerationEvent
from roguengine.event.move import MoveEvent, Movement
from roguengine.event.wear import WearWeaponEvent, WearArmorEvent


class InputProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    self.world.publish(DungeonGenerationEvent(None))
                    continue

                players = self.world.get_components(PlayerComponent)
                if not players:
                    continue
                player, _ = self.world.get_components(PlayerComponent)[0]

                if event.key == pygame.K_DOWN:
                    self.world.publish(MoveEvent(player, Movement(0, 1)))
                    self.world.publish(AIEvent())
                if event.key == pygame.K_UP:
                    self.world.publish(MoveEvent(player, Movement(0, -1)))
                    self.world.publish(AIEvent())
                if event.key == pygame.K_LEFT:
                    self.world.publish(MoveEvent(player, Movement(-1, 0)))
                    self.world.publish(AIEvent())
                if event.key == pygame.K_RIGHT:
                    self.world.publish(MoveEvent(player, Movement(1, 0)))
                    self.world.publish(AIEvent())

                if event.key == pygame.K_c:
                    fighter = self.world.get_component(FighterComponent)
                    fighter[0][1]._hp -= 1

                if event.key == pygame.K_w:
                    self.world.publish(WearWeaponEvent(player))
                    self.world.publish(WearArmorEvent(player))
                    self.world.publish(AIEvent())
