# -*- coding: utf-8 -*-
import sqlite3
import os
import contextlib
import csv
from io import StringIO
import re


def ingest_data(csv_string: str, db_location: str, source_url=""):
    print(db_location)
    official_sources = ['basicrulesv1', "player'shandbook", 'monstermanual', 'thewildbeyondthewitchlight', "vanrichten'sguidetoravenloft", 'strixhaven:acurriculumofchaos', "fizban'streasuryofdragons", 'candlekeepmysteries', "tasha'scauldronofeverything", 'strangerthingsanddungeons&dragons', 'beasts&behemoths', 'icewinddale:rimeofthefrostmaiden', 'mythicodysseysoftheros', "explorer'sguidetowildmount", 'dungeons&dragonsvsrickandmorty', 'eberron:risingfromthelastwar', 'infernalmachinerebuild', 'tyrranyofdragons', 'locathahrising', "baldur'sgate:descentintoavernus",
                        'dungeons&dragonsessentialskit', 'acquisitionsincorporated', 'ghostsofsaltmarsh', "guildmasters'guidetoravnica", 'waterdeep:dungeonofthemadmage', 'waterdeep:dragonheist', 'lostlaboratoryofkwalish', "mordenkainen'stomeoffoes", 'intotheborderlands', "xanathar'sguidetoeverything", 'tombofannihilation', 'thetortlepackage', 'talesfromtheyawningportal', "volo'sguidetomonsters", "stormking'sthunder", 'curseofstrahd', "swordcoastadventurer'sguide", 'outoftheabyss', "player'scompanion", 'princesoftheapocalypse', "dungeonmaster'sguide", 'riseoftiamat', 'hoardofthedragonqueen', "explorer'sguidetowildemount"]
    source_replace_from = [
        "Waterdeep dungeon Of The Mad Mage", "Waterdeep Dragon Heist", 'Eberron - Rising from the Last War', "Baldur's Gate - Descent into Avernus", "Explorers Guide to Wildemount", "Rime of the Frost Maiden", "Icewind Dale"]
    source_replace_to = [
        "Waterdeep: Dungeon of the Mad Mage", "Waterdeep: Dragon Heist", "Eberron: Rising from the Last War", "Baldur's Gate: Descent into Avernus", "Explorer's Guide to Wildemount", "Icewind Dale: Rime of the Frost Maiden", "Icewind Dale: Rime of the Frost Maiden"]
    source_name = None
    with contextlib.closing(sqlite3.connect(db_location, uri=True)) as conn:
        f = StringIO(csv_string)
        csv_reader = csv.DictReader(f, delimiter=',')
        c = conn.cursor()
        c.execute(
            '''SELECT name FROM sources WHERE official = 1''')
        sources_official = [source[0] for source in c.fetchall()]

        for row in csv_reader:
            sources = row['sources'].split(', ')
            for source in sources:
                if ':' in source:
                    source_name = ':'.join(source.split(':')[:-1]).strip()
                else:
                    source_name = source
                try:
                    source_name = source_replace_to[source_replace_from.index(
                        source_name)]
                except ValueError:
                    pass

                if re.sub(whitespace_pattern, '', source_name.lower()) in official_sources or source_name in sources_official:
                    source_is_official = 1
                else:
                    source_is_official = 0

                c.execute('''INSERT OR REPLACE INTO sources VALUES (?, ?, ?)''',
                          (source_name, source_is_official, source_url))

            try:
                values = [row['fid'], row['name'], row['cr'], row['size'], row['type'], row['alignment'],
                          row['environment'], row['ac'], row['hp'], row['init'], row['lair'], row['legendary'], row['named'], row['sources']]
            except KeyError:
                values = [row['fid'], row['name'], row['cr'], row['size'], row['type'], row['alignment'],
                          row['environment'], row['ac'], row['hp'], row['init'], row['lair?'], row['legendary?'], row['unique?'], row['sources']]

            for i in range(len(values)):
                if type(values[i]) == str:
                    values[i] = values[i].replace("'           '", "")
                    values[i] = values[i].strip()

            if values[6] == "":
                values[6] = "no environment specified"

            try:
                if source_replace_from.index(values[13]) != -1:
                    values[13] = source_replace_to[source_replace_from.index(
                        values[13])]
            except ValueError:
                pass

            c.execute(
                '''INSERT OR IGNORE INTO monsters VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (*values,),
            )

        conn.commit()
        c.execute(
            '''SELECT name FROM sources WHERE official = 0''')
        sources_official = [source[0] for source in c.fetchall()]
    return source_name


def load_csv_from_file(filename: str) -> str:
    with open(os.path.abspath(os.path.join(dir_path, filename))) as f:
        return f.read()


def configure_db(db_location: str) -> None:
    conn = sqlite3.connect(db_location)
    c = conn.cursor()

    c.execute('''DROP TABLE IF EXISTS monsters''')
    c.execute('''DROP TABLE IF EXISTS sources''')
    c.execute('''CREATE TABLE monsters (
                fid text UNIQUE,
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
                sources text)'''
              )
    c.execute('''CREATE TABLE sources (
        name text UNIQUE,
        official int,
        url text)'''
              )

    conn.commit()


dir_path = os.path.join(os.path.dirname(__file__), os.pardir, "data/")
db_location = os.path.abspath(os.path.join(dir_path, "monsters.db"))
whitespace_pattern = re.compile(r'\s+')
url_pattern = re.compile(r"(?P<url>https?://[^\s]+)")

if __name__ == "__main__":
    """with contextlib.closing(sqlite3.connect(db_location, uri=True)) as conn:
        c = conn.cursor()
        c.execute('''SELECT * FROM monsters''')
        results = c.fetchall()
        with open(f"{dir_path}/master.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["fid", "name", "cr", "size", "type", "alignment", "environment",
                             "ac", "hp", "init", "lair", "legendary", "named", "sources"])
            writer.writerows(results)

        c.execute('''SELECT * FROM sources''')
        results = c.fetchall()
        with open(f"{dir_path}/master_sources.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["name", "official", "url"])
            writer.writerows(results)"""

    configure_db(db_location)
    csv_string = load_csv_from_file("master.csv")
    ingest_data(csv_string, db_location)

    csv_string = load_csv_from_file("master_sources.csv")
    with contextlib.closing(sqlite3.connect(db_location, uri=True)) as conn:
        f = StringIO(csv_string)
        csv_reader = csv.DictReader(f, delimiter=',')
        c = conn.cursor()
        for row in csv_reader:
            c.execute('''INSERT OR REPLACE INTO sources VALUES (?, ?, ?)''',
                      (row['name'], row['official'], row['url'],))
