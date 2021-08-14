import sqlite3
import contextlib
from typing import List
from fractions import Fraction


db_location = "data/monsters.db"


def get_list_of_environments() -> List[str]:
    with contextlib.closing(sqlite3.connect(db_location)) as conn:
        c = conn.cursor()

        c.execute('''SELECT DISTINCT environment FROM monsters''')
        unique_environments = [item[0] for item in c.fetchall()]

    set_of_environments = set()
    for environment in unique_environments:
        if not environment:
            continue
        for env in environment.split(','):
            set_of_environments.add(env.strip())

    environments = list(set_of_environments)
    environments.sort()
    return environments


def get_list_of_sizes() -> List[str]:
    return ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"]


def get_list_of_monster_types() -> List[str]:
    with contextlib.closing(sqlite3.connect(db_location)) as conn:
        c = conn.cursor()

        c.execute('''SELECT DISTINCT type FROM monsters''')
        unique_types = [item[0] for item in c.fetchall()]

    unique_types.sort()
    return unique_types


def get_list_of_challenge_ratings() -> List[str]:
    with contextlib.closing(sqlite3.connect(db_location)) as conn:
        c = conn.cursor()

        c.execute('''SELECT DISTINCT cr FROM monsters''')
        unique_crs = [item[0] for item in c.fetchall()]

    unique_crs.sort(key=Fraction)
    return unique_crs
