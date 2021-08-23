# -*- coding: utf-8 -*-
import sqlite3
import os
import contextlib
import csv
from io import StringIO


def ingest_data(csv_string: str, db_location: str, source_url=""):
    source_name = None
    with contextlib.closing(sqlite3.connect(db_location, uri=True)) as conn:
        f = StringIO(csv_string)
        csv_reader = csv.DictReader(f, delimiter=',')
        c = conn.cursor()
        c.execute(
            '''SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';''')
        print(c.fetchall())
        for row in csv_reader:
            if not source_name:
                source_name = row['sources'].split(':')[0]
            values = [row['fid'], row['name'], row['cr'], row['size'], row['type'], row['alignment'],
                      row['environment'], row['ac'], row['hp'], row['init'], row['lair?'], row['legendary?'], row['unique?'], row['sources'], 0 if source_url == "" else 1, source_url]

            for i in range(len(values)):
                if type(values[i]) == str:
                    values[i] = values[i].replace("'           '", "")
                    values[i] = values[i].strip()

            c.execute(
                '''INSERT INTO monsters VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (*values,),
            )

        conn.commit()
    return source_name


def load_csv_from_file(filename: str) -> str:
    with open(os.path.abspath(os.path.join(dir_path, filename))) as f:
        return f.read()


def configure_db(db_location: str) -> None:
    conn = sqlite3.connect(db_location)
    c = conn.cursor()

    c.execute('''DROP TABLE IF EXISTS monsters''')
    c.execute('''CREATE TABLE monsters(
                fid text,
                name text,
                cr text,
                size text,
                type text,
                alignment text,
                environment text,
                ac int,
                hp int,
                init text,
                lair int,
                legendary int,
                named int,
                source text,
                source_official int,
                source_url text)'''
              )

    conn.commit()


dir_path = os.path.join(os.path.dirname(__file__), os.pardir, "data/")
db_location = os.path.abspath(os.path.join(dir_path, "monsters.db"))


if __name__ == "__main__":
    configure_db(db_location)
    csv_string = load_csv_from_file("master.csv")
    ingest_data(csv_string, db_location)
