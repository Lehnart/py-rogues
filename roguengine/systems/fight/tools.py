from typing import Optional

from roguengine.esper import esper
from roguengine.systems.dungeon.tools import get_entities_at
from roguengine.systems.fight.components import FighterComponent, WeaponComponent, ArmorComponent


def is_fighter(world: esper.World, entity: int) -> bool:
    return world.has_component(entity, FighterComponent)


def get_last_attacker(world: esper.World, entity: int) -> Optional[int]:
    fighter_component = world.component_for_entity(entity, FighterComponent)
    return fighter_component.last_attacker()


def get_weapon_at(world: esper.World, x: int, y: int) -> Optional[int]:
    weapons = []
    entities = get_entities_at(world, x, y)
    for ent in entities:
        if world.has_component(ent, WeaponComponent):
            weapons.append((ent, world.get_component(WeaponComponent)))

    assert len(weapons) <= 1

    return weapons[0][0] if weapons else None


def get_armor_at(world: esper.World, x: int, y: int) -> Optional[int]:
    armors = []
    entities = get_entities_at(world, x, y)
    for ent in entities:
        if world.has_component(ent, ArmorComponent):
            armors.append((ent, world.get_component(ArmorComponent)))

    assert len(armors) <= 1

    return armors[0][0] if armors else None
