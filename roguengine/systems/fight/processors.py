import random

from roguengine.rogue_esper import Processor
from roguengine.systems.dungeon.components import PositionComponent
from roguengine.systems.dungeon.events import SetPositionEvent, RemovePositionEvent
from roguengine.systems.fight.components import *
from roguengine.systems.fight.components import WeaponSlotComponent, WeaponComponent, ArmorSlotComponent, ArmorComponent
from roguengine.systems.fight.events import *
from roguengine.systems.fight.tools import get_weapon_at, get_armor_at
from roguengine.systems.log.events import LogEvent
from roguengine.systems.render.events import UpdateSpritePositionEvent, FlipEvent


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

            weapon = get_weapon_at(self.world, x, y)
            if not weapon:
                continue

            new_weapon_ent, _ = weapon
            weapon_slot: WeaponSlotComponent = self.world.component_for_entity(slot_ent, WeaponSlotComponent)
            old_weapon_ent = weapon_slot.get_weapon()
            weapon_slot.set_weapon(new_weapon_ent)

            if old_weapon_ent:
                self.world.publish(UpdateSpritePositionEvent(old_weapon_ent, x, y))
                self.world.publish(FlipEvent(old_weapon_ent))
                self.world.publish(SetPositionEvent(old_weapon_ent, x, y))

            self.world.publish(FlipEvent(new_weapon_ent))
            self.world.publish(RemovePositionEvent(new_weapon_ent))

            self.world.publish(LogEvent("You wear a weapon."))


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

            armor = get_armor_at(self.world, x, y)
            if not armor:
                continue

            new_armor_ent, _ = armor
            armor_slot: ArmorSlotComponent = self.world.component_for_entity(slot_ent, ArmorSlotComponent)
            old_armor_ent = armor_slot.get_armor()
            armor_slot.set_armor(new_armor_ent)

            if old_armor_ent:
                self.world.publish(UpdateSpritePositionEvent(old_armor_ent, x, y))
                self.world.publish(FlipEvent(old_armor_ent))
                self.world.publish(SetPositionEvent(old_armor_ent, x, y))

            self.world.publish(FlipEvent(new_armor_ent))
            self.world.publish(RemovePositionEvent(new_armor_ent))

            self.world.publish(LogEvent("You wear a armor."))
