from typing import List

from roguengine.component.armor import ArmorComponent
from roguengine.component.armor_slot import ArmorSlotComponent
from roguengine.component.position import PositionComponent
from roguengine.component.sprite import VisibleSpriteComponent
from roguengine.component.weapon import WeaponComponent
from roguengine.component.weapon_slot import WeaponSlotComponent
from roguengine.esper import Processor
from roguengine.event.log import LogEvent
from roguengine.event.wear import WearWeaponEvent, WearArmorEvent


class WearWeaponProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        for msg in self.world.receive(WearWeaponEvent):
            slot_ent = msg.slot_entity

            if not self.world.has_component(slot_ent, WeaponSlotComponent):
                continue

            slot_pos: PositionComponent = self.world.component_for_entity(slot_ent, PositionComponent)
            x, y = slot_pos.xy()

            weapons = self.get_entities_at(x, y, WeaponComponent)
            if not weapons:
                continue

            new_weapon_ent = weapons[0]
            weapon_slot: WeaponSlotComponent = self.world.component_for_entity(slot_ent, WeaponSlotComponent)
            old_weapon_ent = weapon_slot.get_weapon()
            weapon_slot.set_weapon(new_weapon_ent)

            if old_weapon_ent:
                old_weapon_sprite: VisibleSpriteComponent = self.world.component_for_entity(old_weapon_ent, VisibleSpriteComponent)
                old_weapon_sprite.flip()
                old_weapon_sprite.set_position(x, y)
                self.world.add_component(old_weapon_ent, PositionComponent(x, y))

            new_weapon_sprite: VisibleSpriteComponent = self.world.component_for_entity(new_weapon_ent, VisibleSpriteComponent)
            new_weapon_sprite.flip()
            self.world.remove_component(new_weapon_ent, PositionComponent)

            self.world.publish(LogEvent("You wear a weapon."))

    def get_entities_at(self, x: int, y: int, *component_types) -> List[int]:
        entities = []
        for ent, (pos, *_) in self.world.get_components(PositionComponent, *component_types):
            if pos.xy() == (x, y):
                entities.append(ent)
        return entities


class WearArmorProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        for msg in self.world.receive(WearArmorEvent):
            slot_ent = msg.slot_entity

            if not self.world.has_component(slot_ent, ArmorSlotComponent):
                continue

            slot_pos: PositionComponent = self.world.component_for_entity(slot_ent, PositionComponent)
            x, y = slot_pos.xy()

            armors = self.get_entities_at(x, y, ArmorComponent)
            if not armors:
                continue

            new_armor_ent = armors[0]
            armor_slot: ArmorSlotComponent = self.world.component_for_entity(slot_ent, ArmorSlotComponent)
            old_armor_ent = armor_slot.get_armor()
            armor_slot.set_armor(new_armor_ent)

            if old_armor_ent:
                old_armor_sprite: VisibleSpriteComponent = self.world.component_for_entity(old_armor_ent, VisibleSpriteComponent)
                old_armor_sprite.flip()
                old_armor_sprite.set_position(x, y)
                self.world.add_component(old_armor_ent, PositionComponent(x, y))

            new_armor_sprite: VisibleSpriteComponent = self.world.component_for_entity(new_armor_ent, VisibleSpriteComponent)
            new_armor_sprite.flip()
            self.world.remove_component(new_armor_ent, PositionComponent)

            self.world.publish(LogEvent("You wear a armor."))

    def get_entities_at(self, x: int, y: int, *component_types) -> List[int]:
        entities = []
        for ent, (pos, *_) in self.world.get_components(PositionComponent, *component_types):
            if pos.xy() == (x, y):
                entities.append(ent)
        return entities
