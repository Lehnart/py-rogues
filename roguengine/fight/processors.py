import random
from typing import List

from roguengine.dungeon.components import PositionComponent
from roguengine.fight.components import *
from roguengine.fight.components import WeaponSlotComponent, WeaponComponent, ArmorSlotComponent, ArmorComponent
from roguengine.fight.events import *
from roguengine.log.events import LogEvent
from roguengine.render.components import VisibleSpriteComponent
from roguengine.rogue_esper import Processor


class FightProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        for msg in self.world.receive(FightEvent):
            attacker_ent, defender_ent = msg.attacker, msg.defender

            try:
                attacker = self.world.component_for_entity(attacker_ent, FighterComponent)
                defender = self.world.component_for_entity(defender_ent, FighterComponent)
            except KeyError:
                continue

            if attacker.type() == defender.type():
                continue

            defender.set_last_attacker(attacker_ent)

            attack_bonus = 0
            weapon_slot = self.world.try_component(attacker_ent, WeaponSlotComponent)
            if weapon_slot:
                weapon_ent = weapon_slot.get_weapon()
                if weapon_ent:
                    weapon = self.world.try_component(weapon_ent, WeaponComponent)
                    attack_bonus = weapon.attack_bonus() if weapon else 0

            defense_bonus = 0
            armor_slot = self.world.try_component(defender_ent, ArmorSlotComponent)
            if armor_slot:
                armor_ent = armor_slot.get_armor()
                if armor_ent:
                    armor = self.world.try_component(armor_ent, ArmorComponent)
                    defense_bonus = armor.defense_bonus() if armor else 0

            roll_need = 20 - attacker.attack() - attack_bonus + defender.defense() + defense_bonus
            roll = random.randint(1, 20)
            if roll >= roll_need:
                msg = "You have hit."
                damage = random.randint(1, 4)
                msg += "You did " + str(damage) + " damage."
                defender.damage(damage)
                if defender.hp() > 0:
                    msg += "Enemy has " + str(defender.hp()) + " left."
                else:
                    msg += "Enemy is dead."
                    self.world.delete_entity(defender_ent, True)

                self.world.publish(LogEvent(msg))

            else:
                self.world.publish(LogEvent("You have miss."))


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
