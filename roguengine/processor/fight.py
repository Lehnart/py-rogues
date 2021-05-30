import random

from roguengine.component.armor import ArmorComponent
from roguengine.component.armor_slot import ArmorSlotComponent
from roguengine.component.fighter import FighterComponent
from roguengine.component.weapon import WeaponComponent
from roguengine.component.weapon_slot import WeaponSlotComponent
from roguengine.esper import Processor
from roguengine.event.fight import FightEvent
from roguengine.event.log import LogEvent


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
