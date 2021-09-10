# -*- coding: utf-8 -*-
import contextlib
import csv
import hashlib
import os
import re
import sqlite3
from io import StringIO
from typing import Any, List, Tuple, Union

dir_path = os.path.join(os.path.dirname(__file__), os.pardir, "data/")
db_location = os.path.abspath(os.path.join(dir_path, "monsters.db"))
whitespace_pattern = re.compile(r'\s+')
url_pattern = re.compile(r"(?P<url>https?://[^\s]+)")


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
        index = index.strip()
    except IndexError:
        source_name = ':'.join(source.split(':')[:-1]).strip()
        index = source.split(':')[-1].strip()  # ignore

    return (source_name, index)


def write_to_db(query: str, values: List[List[Any]], db_location=db_location):
    with contextlib.closing(sqlite3.connect(db_location)) as conn:
        c = conn.cursor()
        c.executemany(query, values)
        conn.commit()


def amalgamate_sources(sources_list: List[List[str]]) -> List[str]:
    master: List[str] = []
    for source_list in sources_list:
        for source in source_list:
            plain_source = re.sub(whitespace_pattern, '', source.lower())
            plain_master = [re.sub(
                whitespace_pattern, '', master_source.lower()) for master_source in master]
            if plain_source not in plain_master:
                master.append(source)

    return master


def ingest_data(csv_string: str, db_location: str, source=""):
    source_url = str(source)
    official_sources = ['basicrulesv1', "player'shandbook", 'monstermanual', 'thewildbeyondthewitchlight', "vanrichten'sguidetoravenloft", 'strixhaven:acurriculumofchaos', "fizban'streasuryofdragons", 'candlekeepmysteries', "tasha'scauldronofeverything", 'strangerthingsanddungeons&dragons', 'beasts&behemoths', 'icewinddale:rimeofthefrostmaiden', 'mythicodysseysoftheros', "explorer'sguidetowildmount", 'dungeons&dragonsvsrickandmorty', 'eberron:risingfromthelastwar', 'infernalmachinerebuild', 'tyrranyofdragons', 'locathahrising', "baldur'sgate:descentintoavernus",
                        'dungeons&dragonsessentialskit', 'acquisitionsincorporated', 'ghostsofsaltmarsh', "guildmasters'guidetoravnica", 'waterdeep:dungeonofthemadmage', 'waterdeep:dragonheist', 'lostlaboratoryofkwalish', "mordenkainen'stomeoffoes", 'intotheborderlands', "xanathar'sguidetoeverything", 'tombofannihilation', 'thetortlepackage', 'talesfromtheyawningportal', "volo'sguidetomonsters", "stormking'sthunder", 'curseofstrahd', "swordcoastadventurer'sguide", 'outoftheabyss', "player'scompanion", 'princesoftheapocalypse', "dungeonmaster'sguide", 'riseoftiamat', 'hoardofthedragonqueen', "explorer'sguidetowildemount"]
    source_replace_from = [
        "Waterdeep dungeon Of The Mad Mage", "Waterdeep Dungeon of the Mad Mage", "Waterdeep Dragon Heist", 'Eberron - Rising from the Last War', "Baldur's Gate - Descent into Avernus", "Explorers Guide to Wildemount", "Rime of the Frost Maiden", "Icewind Dale", "Tome of Beasts 2"]
    source_replace_to = [
        "Waterdeep: Dungeon of the Mad Mage", "Waterdeep: Dungeon of the Mad Mage", "Waterdeep: Dragon Heist", "Eberron: Rising from the Last War", "Baldur's Gate: Descent into Avernus", "Explorer's Guide to Wildemount", "Icewind Dale: Rime of the Frost Maiden", "Icewind Dale: Rime of the Frost Maiden", "Tome of Beasts II"]

    with contextlib.closing(sqlite3.connect(db_location, uri=True)) as conn:
        f = StringIO(csv_string)
        csv_reader = csv.DictReader(f, delimiter=',')
        c = conn.cursor()
        sources_in_url: List[str] = []

        if already_processed := check_if_key_processed(source_url):
            return already_processed

        c.execute(
            '''SELECT name FROM sources WHERE official = 1''')
        sources_official = [source[0] for source in c.fetchall()]

        for row in csv_reader:
            monster_is_official = False
            dirty_sources = row['sources'].split(', ')
            sources = []
            for source in dirty_sources:
                (source_name, index) = split_source_from_index(source)
                try:
                    source_name = source_replace_to[source_replace_from.index(
                        source_name)]
                except ValueError:
                    pass
                finally:
                    if index == '':
                        sources.append(f"{source_name}")
                    else:
                        sources.append(f"{source_name}: {index}")

                if re.sub(whitespace_pattern, '', source_name.lower()) in official_sources or source_name in sources_official:
                    monster_is_official = True

            # Now comes the fun; we need to define some logic for handling monsters with similar names
            # Specifically, if monsters from multiple sources have the same name, we need to put a name
            # abbreviation next to the name to prevent confusion.
            # However, official monsters should not have an abbreviation next to their name, and many
            # official monsters are in multiple sourcebooks.
            # This logic should hold true even if a custom monster is in the db before an official monster
            # of the same name.
            # Start situations: official monster in db, unofficial monster in db, both in db, neither in db
            # Changes: official monster added, unofficial monster added

            monster_name = row['name']
            sources_of_nametwins = []

            c.execute('SELECT sources FROM monsters WHERE name = ?',
                      (monster_name,))

            existing_monsters_with_name_string = c.fetchall()
            for string in existing_monsters_with_name_string:
                sources_of_nametwins += string[0].split(', ')

            official_nametwins = []
            unofficial_nametwins = []
            for source in sources_of_nametwins:
                name, _ = split_source_from_index(source)
                c.execute(
                    '''SELECT official FROM sources WHERE name = ?''', (name,))
                if c.fetchall()[0][0]:
                    official_nametwins.append(source)
                else:
                    unofficial_nametwins.append(source)

            if sources_of_nametwins:
                if monster_is_official:
                    sources = amalgamate_sources(
                        [sources, official_nametwins])
                    updates = []
                    for un_source in unofficial_nametwins:
                        name, _ = split_source_from_index(un_source)
                        source_acronym = ''.join([word[0]
                                                  for word in name.split()])
                        new_name = f"{row['name']} ({source_acronym})"
                        updates.append((new_name, monster_name, un_source))
                    c.executemany(
                        '''UPDATE monsters SET name = ? WHERE name = ? AND sources = ?''', (updates))

                else:
                    updates = []
                    for un_source in unofficial_nametwins:
                        name, _ = split_source_from_index(un_source)
                        source_acronym = ''.join([word[0]
                                                  for word in name.split()])
                        new_name = f"{row['name']} ({source_acronym})"
                        updates.append((new_name, monster_name, un_source))
                    name, _ = split_source_from_index(sources[0])
                    source_acronym = ''.join([word[0]
                                              for word in name.split()])
                    monster_name = f"{row['name']} ({source_acronym})"
                    c.executemany(
                        '''UPDATE OR IGNORE monsters SET name = ? WHERE name = ? AND sources = ?''', (updates))

            # Standardise the way sources are saved and confirm officiality - or lack thereof - of source
            source_hashes = []
            corrected_sources = []
            storing_sources = []
            for source in sources:
                (source_name, index) = split_source_from_index(source)
                if re.sub(whitespace_pattern, '', source_name.lower()) in official_sources or source_name in sources_official:
                    source_is_official = 1
                else:
                    source_is_official = 0

                corrected_sources.append(f"{source_name}: {index}")
                source_hashes.append(hash_source_name(source_name))

                storing_sources.append([source_name, source_is_official, hash_source_name(
                    source_name), source_url, hash_source_name(f"{source_name}{source_url}")])

            c.executemany('''INSERT OR REPLACE INTO sources VALUES (?, ?, ?, ?, ?)''',
                          storing_sources)

            hash_string = ','.join(source_hashes)
            if corrected_sources == 0:
                continue

            # Start sanity checking the data

            # Tidy up alignments
            if row['alignment'] == "any":
                alignment = "any alignment"
            elif row['alignment'] == "" or row['alignment'] == "none":
                alignment = "unaligned"
            else:
                alignment = row['alignment'].lower()

            # Prevent blank environments
            if re.sub(whitespace_pattern, '', row['environment']) == "":
                environments = "no environment specified"
            else:
                environments = row['environment']

            values: List[Any] = []
            try:
                values = [row['fid'], monster_name, row['cr'], row['size'], row['type'], alignment,
                          environments, row['ac'], row['hp'], row['init'], row['lair'], row['legendary'], row['named'], ', '.join(corrected_sources), hash_string]
            except KeyError:
                values = [row['fid'], monster_name, row['cr'], row['size'], row['type'], alignment,
                          environments, row['ac'], row['hp'], row['init'], row['lair?'], row['legendary?'], row['unique?'], ', '.join(corrected_sources), hash_string]

            for i in range(len(values)):
                if type(values[i]) == str:
                    values[i] = values[i].replace("'           '", "")
                    values[i] = values[i].strip()

            c.execute(
                '''INSERT OR REPLACE INTO monsters VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', values)

        conn.commit()

        return check_if_key_processed(source_url)


def load_csv_from_file(filename: str) -> str:
    with open(os.path.abspath(os.path.join(dir_path, filename))) as f:
        csv_string = f.read()
        end_of_first_line = csv_string.find("\n")
        csv_string = csv_string.replace(
            csv_string[:end_of_first_line], csv_string[:end_of_first_line].lower())
        return csv_string


def configure_db(db_location: str):
    conn = sqlite3.connect(db_location)
    c = conn.cursor()

    c.execute('''DROP TABLE IF EXISTS monsters''')
    c.execute('''DROP TABLE IF EXISTS sources''')
    c.execute('''CREATE TABLE monsters (
                fid text,
                name text UNIQUE,
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
    return conn


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
    f = StringIO(csv_string)
    csv_reader = csv.DictReader(f, delimiter=',')
    storing_sources: List[List[Any]] = []
    for row in csv_reader:
        storing_sources.append(
            [row['name'], row['official'], row['hash'], row['url'], row['sourceurlhash']])

    write_to_db(
        '''INSERT OR IGNORE INTO sources VALUES (?, ?, ?, ?, ?)''', storing_sources)
