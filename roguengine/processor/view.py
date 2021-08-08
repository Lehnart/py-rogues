import numpy
import tcod

from roguengine.component.dungeon.dungeon import DungeonComponent
from roguengine.component.opaque import OpaqueComponent
from roguengine.component.player import PlayerComponent
from roguengine.component.position import PositionComponent
from roguengine.component.sprite import VisibleSpriteComponent
from roguengine.component.viewed import ViewedComponent
from roguengine.component.visible import VisibleComponent
from roguengine.rogue_esper import Processor


class RoomViewProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        players = self.world.get_components(PlayerComponent, PositionComponent)
        if not players:
            return
        player, [_, position] = players[0]
        px, py = position.xy()

        dungeon_entity, dungeon_component = self.world.get_component(DungeonComponent)[0]
        entities = self.world.get_components(PositionComponent, VisibleSpriteComponent)
        inside_room = [r for r in dungeon_component.rooms() if r.is_in(px, py)]
        if not inside_room:
            for ent, (pos, _) in entities:
                x, y = pos.xy()
                if not (px - 1 <= x <= px + 1 and py - 1 <= y <= py + 1):
                    if self.world.has_component(ent, VisibleComponent):
                        self.world.remove_component(ent, VisibleComponent)

                elif not self.world.has_component(ent, VisibleComponent):
                    self.world.add_component(ent, VisibleComponent())
                    if not self.world.has_component(ent, ViewedComponent):
                        self.world.add_component(ent, ViewedComponent())

        else:
            room = inside_room[0]
            for ent, (pos, _) in entities:
                x, y = pos.xy()
                if not room.is_in(x, y):
                    if self.world.has_component(ent, VisibleComponent):
                        self.world.remove_component(ent, VisibleComponent)
                elif not self.world.has_component(ent, VisibleComponent):
                    self.world.add_component(ent, VisibleComponent())
                    if not self.world.has_component(ent, ViewedComponent):
                        self.world.add_component(ent, ViewedComponent())

    def get_entities_at(self, x: int, y: int, *component_types):
        entities = []
        for ent, (pos, *_) in self.world.get_components(PositionComponent, *component_types):
            if pos.xy() == (x, y):
                entities.append(ent)
        return entities


class FOVViewProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        players = self.world.get_components(PlayerComponent, PositionComponent)
        if not players:
            return
        player, [_, position] = players[0]
        px, py = position.xy()

        dungeon_entity, dungeon_component = self.world.get_component(DungeonComponent)[0]
        w, h = dungeon_component.width(), dungeon_component.height()
        transparency = numpy.ones((w, h))
        opaque_tiles = self.world.get_components(OpaqueComponent, PositionComponent)
        for _, [_, pos] in opaque_tiles:
            x, y = pos.xy()
            transparency[x, y] = 0

        seen_array = tcod.map.compute_fov(transparency, (px, py))
        positions = self.world.get_components(PositionComponent)
        for ent, [pos] in positions:
            x, y = pos.xy()
            if not seen_array[x, y] and self.world.has_component(ent, VisibleComponent):
                self.world.remove_component(ent, VisibleComponent)

            if seen_array[x, y] and not self.world.has_component(ent, VisibleComponent):
                self.world.add_component(ent, VisibleComponent())
                if not self.world.has_component(ent, ViewedComponent):
                    self.world.add_component(ent, ViewedComponent())

    def get_entities_at(self, x: int, y: int, *component_types):
        entities = []
        for ent, (pos, *_) in self.world.get_components(PositionComponent, *component_types):
            if pos.xy() == (x, y):
                entities.append(ent)
        return entities
