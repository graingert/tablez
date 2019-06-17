import importlib.resources
import json

import eztable

DATA = json.loads(importlib.resources.read_text(__package__, 'database.json'))
WEAPONS = json.loads(importlib.resources.read_text(__package__, 'weapons.json'))


attackers = (
    eztable
    .Table([
        ("alliance_id", int),
        ("character_id", int),
        ("corporation_id", int),
        ("damage_done", int),
        ("final_blow", bool),
        ("security_status", float),
        ("ship_type_id", int),
        ("weapon_type_id", int),
    ])
)
attackers.weapon_type_id_index = attackers.add_index(['weapon_type_id'])

weapons = eztable.Table([
    ("id", int),
    ("name", str)
])
weapons.id_index = weapons.add_index(['id'])

def load():
    for attacker in DATA['attackers']:
        attackers.append([attacker.get(col) for col in attackers.column_names])

    for id, name in WEAPONS.items():
        weapons.append([int(id), name])

load()

print(
    attackers
    .left_join(keys=('weapon_type_id', ), other=weapons, other_keys=('id', ))
)
