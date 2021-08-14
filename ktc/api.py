import sqlite3
import contextlib
from typing import List
from fractions import Fraction


db_location = "data/monsters.db"


def sort_sizes(size_list: List[str]) -> List[str]:
    to_return = []

    size_list = [size.lower() for size in size_list]

    if "tiny" in size_list:
        to_return.append("tiny")
    if "small" in size_list:
        to_return.append("small")
    if "medium" in size_list:
        to_return.append("medium")
    if "large" in size_list:
        to_return.append("large")
    if "huge" in size_list:
        to_return.append("huge")
    if "gargantuan" in size_list:
        to_return.append("gargantuan")

    to_return = [size.title() for size in to_return]
    return to_return


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
    with contextlib.closing(sqlite3.connect(db_location)) as conn:
        c = conn.cursor()

        c.execute('''SELECT DISTINCT size FROM monsters''')
        unique_types = [item[0] for item in c.fetchall()]

    size_list = sort_sizes(unique_types)
    return size_list


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


def get_list_of_sources() -> List[str]:
    with contextlib.closing(sqlite3.connect(db_location)) as conn:
        c = conn.cursor()

        c.execute('''SELECT DISTINCT source FROM monsters''')
        unique_sources = [item[0] for item in c.fetchall()]

    set_of_sources = set()
    for source_set in unique_sources:
        sources = source_set.split(',')
        for source in sources:
            set_of_sources.add(source.split(':')[0].strip())

    sources = list(set_of_sources)
    sources.sort()
    return sources
