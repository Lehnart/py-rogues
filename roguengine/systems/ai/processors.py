import math
import random
from typing import List

from roguengine.rogue_esper import Processor
from roguengine.systems.ai.components import AIComponent, State
from roguengine.systems.ai.events import AIEvent
from roguengine.systems.dungeon.events import Movement, MoveEvent
from roguengine.systems.dungeon.tools import get_position
from roguengine.systems.fight.tools import get_last_attacker
from roguengine.systems.player.tools import get_player_entity


class AIProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        events: List[AIEvent] = self.world.receive(AIEvent)
        for _ in events:
            ais = self.world.get_component(AIComponent)
            player_ent = get_player_entity(self.world)
            p_x, p_y = get_position(self.world, player_ent)

            for ai_ent, ai_component in ais:

                ai_x, ai_y = get_position(self.world, ai_ent)

                if ai_component.state() == State.PASSIVE:
                    last_attacker_ent = get_last_attacker(self.world, ai_ent)
                    if last_attacker_ent is not None:
                        ai_component.set_state(State.HOSTILE)
                        ai_component.set_enemy(last_attacker_ent)

                if ai_component.state() == State.GUARDING:
                    if math.sqrt((ai_x - p_x) ** 2 + (ai_y - p_y) ** 2) <= 2.:
                        ai_component.set_state(State.HOSTILE)
                        ai_component.set_enemy(player_ent)

                if ai_component.state() == State.HOSTILE:
                    hostile_moves = []
                    enemy_ent = ai_component.enemy()

                    if enemy_ent is None:
                        ai_component.hostile(player_ent)
                        enemy_ent = player_ent

                    ex, ey = get_position(self.world, enemy_ent)

                    if ex > ai_x:
                        hostile_moves.append(Movement(1, 0))
                    if ex < ai_x:
                        hostile_moves.append(Movement(-1, 0))
                    if ey > ai_y:
                        hostile_moves.append(Movement(0, 1))
                    if ey < ai_y:
                        hostile_moves.append(Movement(0, -1))
                    move = random.choice(hostile_moves)
                    self.world.publish(MoveEvent(ai_ent, move))
