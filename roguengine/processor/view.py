from roguengine.component.dungeon import DungeonComponent
from roguengine.component.dungeon_resident import DungeonResidentComponent
from roguengine.component.player import PlayerComponent
from roguengine.component.position import PositionComponent
from roguengine.component.sprite import VisibleSpriteComponent
from roguengine.component.viewed import ViewedComponent
from roguengine.component.visible import VisibleComponent
from roguengine.esper import Processor


class ViewProcessor(Processor):

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
