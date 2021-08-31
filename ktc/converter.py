# -*- coding: utf-8 -*-
import sqlite3
import os
import contextlib
import csv
from io import StringIO
import re
import hashlib
from typing import Tuple, List


def hash_source_name(source: str) -> str:
    sourcebytes = source.encode('utf-8')
    sha = hashlib.sha1(sourcebytes)
    return "0x" + str(sha.hexdigest())


def check_if_key_processed(key: str) -> str:
    if key == "":
        return ""
    with contextlib.closing(sqlite3.connect(db_location, uri=True)) as conn:
        c = conn.cursor()
        c.execute(
            '''SELECT name FROM sources WHERE url = ?''', (key,))
        results = [result[0] for result in c.fetchall()]
        return ", ".join(results)


def split_source_from_index(source: str) -> Tuple[str, str]:
    if ':' not in source:
        return (source, '')
    try:
        index = re.findall(url_pattern, source)[0]
        source_name = re.sub(url_pattern, '', source).replace(':', '').strip()
        index = index[0].strip()
    except IndexError:
        source_name = ':'.join(source.split(':')[:-1]).strip()
        index = source.split(':')[-1].strip()  # ignore

    return (source_name, index)


def ingest_data(csv_string: str, db_location: str, source_url=""):
    official_sources = ['basicrulesv1', "player'shandbook", 'monstermanual', 'thewildbeyondthewitchlight', "vanrichten'sguidetoravenloft", 'strixhaven:acurriculumofchaos', "fizban'streasuryofdragons", 'candlekeepmysteries', "tasha'scauldronofeverything", 'strangerthingsanddungeons&dragons', 'beasts&behemoths', 'icewinddale:rimeofthefrostmaiden', 'mythicodysseysoftheros', "explorer'sguidetowildmount", 'dungeons&dragonsvsrickandmorty', 'eberron:risingfromthelastwar', 'infernalmachinerebuild', 'tyrranyofdragons', 'locathahrising', "baldur'sgate:descentintoavernus",
                        'dungeons&dragonsessentialskit', 'acquisitionsincorporated', 'ghostsofsaltmarsh', "guildmasters'guidetoravnica", 'waterdeep:dungeonofthemadmage', 'waterdeep:dragonheist', 'lostlaboratoryofkwalish', "mordenkainen'stomeoffoes", 'intotheborderlands', "xanathar'sguidetoeverything", 'tombofannihilation', 'thetortlepackage', 'talesfromtheyawningportal', "volo'sguidetomonsters", "stormking'sthunder", 'curseofstrahd', "swordcoastadventurer'sguide", 'outoftheabyss', "player'scompanion", 'princesoftheapocalypse', "dungeonmaster'sguide", 'riseoftiamat', 'hoardofthedragonqueen', "explorer'sguidetowildemount"]
    source_replace_from = [
        "Waterdeep dungeon Of The Mad Mage", "Waterdeep Dungeon of the Mad Mage", "Waterdeep Dragon Heist", 'Eberron - Rising from the Last War', "Baldur's Gate - Descent into Avernus", "Explorers Guide to Wildemount", "Rime of the Frost Maiden", "Icewind Dale"]
    source_replace_to = [
        "Waterdeep: Dungeon of the Mad Mage", "Waterdeep: Dungeon of the Mad Mage", "Waterdeep: Dragon Heist", "Eberron: Rising from the Last War", "Baldur's Gate: Descent into Avernus", "Explorer's Guide to Wildemount", "Icewind Dale: Rime of the Frost Maiden", "Icewind Dale: Rime of the Frost Maiden"]

    with contextlib.closing(sqlite3.connect(db_location, uri=True)) as conn:
        f = StringIO(csv_string)
        csv_reader = csv.DictReader(f, delimiter=',')
        c = conn.cursor()

        if sources_in_url := check_if_key_processed(source_url):
            return sources_in_url

        c.execute(
            '''SELECT name FROM sources WHERE official = 1''')
        sources_official = [source[0] for source in c.fetchall()]

        for row in csv_reader:
            sources = row['sources'].split(', ')
            source_hashes = []
            corrected_sources = []
            for source in sources:
                (source_name, index) = split_source_from_index(source)
                try:
                    source_name = source_replace_to[source_replace_from.index(
                        source_name)]
                except ValueError:
                    pass

                corrected_sources.append(f"{source_name}: {index}")

                if re.sub(whitespace_pattern, '', source_name.lower()) in official_sources or source_name in sources_official:
                    source_is_official = 1
                else:
                    source_is_official = 0

                source_hashes.append(hash_source_name(source_name))

                c.execute('''INSERT OR IGNORE INTO sources VALUES (?, ?, ?, ?, ?)''',
                          (source_name, source_is_official, hash_source_name(source_name), source_url, hash_source_name(f"{source_name}{source_url}")))

            hash_string = ','.join(source_hashes)

            try:
                values = [row['fid'], row['name'], row['cr'], row['size'], row['type'], row['alignment'],
                          row['environment'], row['ac'], row['hp'], row['init'], row['lair'], row['legendary'], row['named'], ', '.join(corrected_sources), hash_string]
            except KeyError:
                values = [row['fid'], row['name'], row['cr'], row['size'], row['type'], row['alignment'],
                          row['environment'], row['ac'], row['hp'], row['init'], row['lair?'], row['legendary?'], row['unique?'], ', '.join(corrected_sources), hash_string]

            for i in range(len(values)):
                if type(values[i]) == str:
                    values[i] = values[i].replace("'           '", "")
                    values[i] = values[i].strip()

            if values[6] == "":
                values[6] = "no environment specified"

            c.execute(
                '''INSERT OR IGNORE INTO monsters VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (*values,),
            )

        c.execute('''SELECT name FROM sources WHERE url = ?''', (source_url,))
        results = [result[0] for result in c.fetchall()]  # ignore
        sources_processed = ", ".join(results)
        conn.commit()

    return sources_processed


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
                sources text,
                sourcehashes text)'''
              )
    c.execute('''CREATE TABLE sources (
        name text,
        official int,
        hash text,
        url text,
        sourceurlhash text UNIQUE)'''
              )

    conn.commit()


dir_path = os.path.join(os.path.dirname(__file__), os.pardir, "data/")
db_location = os.path.abspath(os.path.join(dir_path, "monsters.db"))
whitespace_pattern = re.compile(r'\s+')
url_pattern = re.compile(r"(?P<url>https?://[^\s]+)")

if __name__ == "__main__":
    with contextlib.closing(sqlite3.connect(db_location, uri=True)) as conn:
        c = conn.cursor()
        c.execute('''SELECT name FROM sqlite_master WHERE type="table"''')
        if len(c.fetchall()) > 0:

            c.execute('''SELECT * FROM monsters''')
            results = c.fetchall()
            with open(f"{dir_path}/master.csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["fid", "name", "cr", "size", "type", "alignment", "environment",
                                "ac", "hp", "init", "lair", "legendary", "named", "sources", "sourcehashes"])
                writer.writerows(results)

            c.execute('''SELECT * FROM sources''')
            results = c.fetchall()
            with open(f"{dir_path}/master_sources.csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["name", "official", "hash", "url", "sourceurlhash"])
                writer.writerows(results)

    configure_db(db_location)
    csv_string = load_csv_from_file("master.csv")
    ingest_data(csv_string, db_location)

    csv_string = load_csv_from_file("master_sources.csv")
    with contextlib.closing(sqlite3.connect(db_location, uri=True)) as conn:
        f = StringIO(csv_string)
        csv_reader = csv.DictReader(f, delimiter=',')
        c = conn.cursor()
        for row in csv_reader:
            print(f"{row['name']}: {row['url']}")
            c.execute('''INSERT OR REPLACE INTO sources VALUES (?, ?, ?, ?, ?)''',
                      (row['name'], row['official'], row['hash'], row['url'], row['sourceurlhash']))

        conn.commit()
