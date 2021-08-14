import sqlite3
import contextlib
from typing import List


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
