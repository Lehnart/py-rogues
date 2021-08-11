import numpy
import tcod

from roguengine.rogue_esper import Processor
from roguengine.systems.dungeon.tools import get_position, get_room, get_w_and_h, get_entities_with_position
from roguengine.systems.player.tools import get_player_entity
from roguengine.systems.render.tools import get_entities_with_sprite
from roguengine.systems.view.components import VisibleComponent, ViewedComponent, OpaqueComponent
from roguengine.systems.view.events import TransparentEvent


class RoomViewProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        player_ent = get_player_entity(self.world)
        if not player_ent:
            return
        px, py = get_position(self.world, player_ent)

        room = get_room(self.world, px, py)
        entities = get_entities_with_sprite(self.world)
        if not room:
            for ent in entities:
                x, y = get_position(self.world, ent)
                if not (px - 1 <= x <= px + 1 and py - 1 <= y <= py + 1):
                    if self.world.has_component(ent, VisibleComponent):
                        self.world.remove_component(ent, VisibleComponent)

                elif not self.world.has_component(ent, VisibleComponent):
                    self.world.add_component(ent, VisibleComponent())
                    if not self.world.has_component(ent, ViewedComponent):
                        self.world.add_component(ent, ViewedComponent())

        else:
            for ent in entities:
                x, y = get_position(self.world, ent)
                if not room.is_in(x, y):
                    if self.world.has_component(ent, VisibleComponent):
                        self.world.remove_component(ent, VisibleComponent)
                elif not self.world.has_component(ent, VisibleComponent):
                    self.world.add_component(ent, VisibleComponent())
                    if not self.world.has_component(ent, ViewedComponent):
                        self.world.add_component(ent, ViewedComponent())


class FOVViewProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        player_ent = get_player_entity(self.world)
        if not player_ent:
            return

        px, py = get_position(self.world, player_ent)

        w, h = get_w_and_h(self.world)
        transparency = numpy.ones((w, h))
        opaque_tiles = self.world.get_components(OpaqueComponent)
        for ent, [_] in opaque_tiles:
            x, y = get_position(self.world, ent)
            transparency[x, y] = 0

        seen_array = tcod.map.compute_fov(transparency, (px, py))
        entities = get_entities_with_position(self.world)
        for ent in entities:
            x, y = get_position(self.world, ent)
            if not seen_array[x, y] and self.world.has_component(ent, VisibleComponent):
                self.world.remove_component(ent, VisibleComponent)

            if seen_array[x, y] and not self.world.has_component(ent, VisibleComponent):
                self.world.add_component(ent, VisibleComponent())
                if not self.world.has_component(ent, ViewedComponent):
                    self.world.add_component(ent, ViewedComponent())

        for msg in self.world.receive(TransparentEvent):
            ent = msg.ent
            if self.world.has_component(ent, OpaqueComponent):
                self.world.remove_component(ent, OpaqueComponent)
