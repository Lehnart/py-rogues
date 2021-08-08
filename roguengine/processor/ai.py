import math
import random
from typing import List

from roguengine.component.ai import AIComponent, State
from roguengine.component.player import PlayerComponent
from roguengine.dungeon.components import PositionComponent
from roguengine.event.ai import AIEvent
from roguengine.event.move import Movement, MoveEvent
from roguengine.fight.components import FighterComponent
from roguengine.rogue_esper import Processor


class AIProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        events: List[AIEvent] = self.world.receive(AIEvent)
        for _ in events:
            ais = self.world.get_component(AIComponent)
            player_ent = self.world.get_component(PlayerComponent)[0][0]
            player_pos = self.world.component_for_entity(player_ent, PositionComponent)

            for ai_ent, ai_component in ais:

                if ai_component.state() == State.PASSIVE:
                    ai_fighter_component = self.world.component_for_entity(ai_ent, FighterComponent)
                    if ai_fighter_component.last_attacker() is not None:
                        ai_component.set_state(State.HOSTILE)
                        ai_component.set_enemy(ai_fighter_component.last_attacker())

                if ai_component.state() == State.GUARDING:
                    ai_pos = self.world.component_for_entity(ai_ent, PositionComponent)
                    ai_x, ai_y = ai_pos.xy()
                    p_x, p_y = player_pos.xy()
                    if math.sqrt((ai_x - p_x) ** 2 + (ai_y - p_y) ** 2) <= 2.:
                        ai_component.set_state(State.HOSTILE)
                        ai_component.set_enemy(player_ent)

                if ai_component.state() == State.HOSTILE:
                    hostile_moves = []
                    enemy_ent = ai_component.enemy()

                    if enemy_ent is None:
                        ai_component.hostile(player_ent)
                        enemy_ent = player_ent
                    ai_pos = self.world.component_for_entity(ai_ent, PositionComponent)
                    ax, ay = ai_pos.xy()

                    enemy_pos = self.world.component_for_entity(enemy_ent, PositionComponent)
                    ex, ey = enemy_pos.xy()

                    if ex > ax:
                        hostile_moves.append(Movement(1, 0))
                    if ex < ax:
                        hostile_moves.append(Movement(-1, 0))
                    if ey > ay:
                        hostile_moves.append(Movement(0, 1))
                    if ey < ay:
                        hostile_moves.append(Movement(0, -1))
                    move = random.choice(hostile_moves)
                    self.world.publish(MoveEvent(ai_ent, move))
