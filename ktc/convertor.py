# -*- coding: utf-8 -*-
import sqlite3
import os


path_to_database = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, "data/monsters.db")
)
db_location = path_to_database


conn = sqlite3.connect(db_location)
c = conn.cursor()

c.execute("""DROP TABLE IF EXISTS monsters""")
c.execute(
    """CREATE TABLE monsters(
                guid test,
                fid text,
                name text,
                cr text,
                size text,
                type text,
                tags text,
                section text,
                alignment text,
                environment text,
                ac int,
                hp int,
                init text,
                lair int,
                legendary int,
                named int,
                source text)"""
)

conn.commit()


with open("data/kfc master monster list - Monsters.tsv") as f:
    line = f.readline()
    while True:
        line = f.readline()
        if not line:
            break

        values = line.split("\t")
        for i in range(len(values)):
            values[i] = values[i].replace("'           '", "")
            values[i] = values[i].replace("'           '", "")
            values[i] = values[i].strip()

        c.execute(
            """INSERT INTO monsters VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (*values,),
        )

    conn.commit()
