# -*- coding: utf-8 -*-
import pytest
from ktc import convertor
import sqlite3


@pytest.fixture
def setup_database():
    """Fixture to setup an in-memory database"""
    conn = sqlite3.connect("file::memory:?cache=shared", uri=True)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE monsters(
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
                source_url text)''')

    yield conn


@pytest.fixture
def populate_database(setup_database):
    conn = setup_database
    c = conn.cursor()

    sample_data = [['tcs.ashari-firetamer', 'Ashari Firetamer', '7', 'Medium', 'Humanoid', 'any', 'neutral good', '17',
                    '92', '2', '', '', '', "Tal'Dorei Campaign Setting: 128", 0, '1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40'],
                   ['tcs.ashari-stoneguard', 'Ashari Stoneguard', '7', 'Medium', 'Humanoid', 'any', 'lawful good', '15',
                       '152', '0', '', '', '', "Tal'Dorei Campaign Setting: 128", 0, '1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40'],
                   ['tcs.ashari-waverider', 'Ashari Waverider', '4', 'Medium', 'Humanoid', 'any', 'neutral good', '14',
                       '77', '2', '', '', '', "Tal'Dorei Campaign Setting: 129", 0, '1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40'],
                   ['tcs.ashari-skydancer', 'Ashari Skydancer', '5', 'Medium', 'Humanoid', 'any', 'chaotic neutral', '14',
                    '63', '4', '', '', '', "Tal'Dorei Campaign Setting: 129", 0, '1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40'],
                   ['tcs.cinderslag-elemantal', 'Cinderslag Elemantal', '5', 'Large', 'Elemental', '', 'chaotic evil', '15',
                    '102', '1', '', '', '', "Tal'Dorei Campaign Setting: 130", 0, '1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40'],
                   ['tcs.clasp-cutthroat', 'Clasp Cutthroat', '3', 'Medium', 'Humanoid', 'any', 'non-lawful', '14',
                    '44', '3', '', '', '', "Tal'Dorei Campaign Setting: 131", 0, '1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40'],
                   ['tcs.clasp-enforcer', 'Clasp Enforcer', '5', 'Medium', 'Humanoid', 'any', 'non-lawful', '16', '102',
                    '1', '', '', '', "Tal'Dorei Campaign Setting: 131", 0, '1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40'],
                   ['tcs.cyclops-stormcaller', 'Cyclops Stormcaller', '10', 'Large', 'Giant', '', 'neutral evil', '18',
                    '119', '0', '', '', '', "Tal'Dorei Campaign Setting: 132", 0, '1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40'],
                   ['tcs.goliath-stormborn', 'Goliath Stormborn', '4', 'Medium', 'Humanoid', 'Goliath', 'chaotic neutral',
                    '13', '102', '1', '', '', '', "Tal'Dorei Campaign Setting: 133", 0, '1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40'],
                   ['tcs.goliath-brawler', 'Goliath Brawler', '3', 'Medium', 'Humanoid', 'Goliath', 'chaotic neutral', '15',
                    '65', '2', '', '', '', "Tal'Dorei Campaign Setting: 134", 0, '1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40'],
                   ['tcs.kraghammer-goat-knight', 'Kraghammer Goat-Knight', '3', 'Medium', 'Humanoid', 'Dwarf', 'neutral good',
                    '20', '52', '-1', '', '', '', "Tal'Dorei Campaign Setting: 134", 0, '1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40'],
                   ['tcs.goat-knight-steed', 'Goat-Knight Steed', '1/2', 'Large', 'Celestial', '', 'unaligned', '11',
                    '19', '0', '', '', '', "Tal'Dorei Campaign Setting: 135", 0, '1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40'],
                   ['tcs.ravager-stabby-stabber', 'Ravager Stabby-Stabber', '2', 'Small', 'Humanoid', 'Goblinoid', 'chaotic evil',
                    '15', '36', '3', '', '', '', "Tal'Dorei Campaign Setting: 137", 0, '1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40'],
                   ['tcs.ravager-slaughter-lord', 'Ravager Slaughter Lord', '9', 'Large', 'Humanoid', 'Orc', 'lawful evil',
                    '17', '152', '2', '', '', '', "Tal'Dorei Campaign Setting: 137", 0, '1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40'],
                   ['tcs.remnant-cultist', 'Remnant Cultist', '7', 'Medium', 'Humanoid', 'any', 'neutral evil', '13',
                    '60', '3', '', '', '', "Tal'Dorei Campaign Setting: 139", 0, '1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40'],
                   ['tcs.remnant-chosen', 'Remnant Chosen', '12', 'Medium', 'Humanoid', 'any', 'neutral evil',
                   '12', '117', '2', '', '', '', "Tal'Dorei Campaign Setting: 139", 0, '1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40'], ]

    c.executemany(
        '''INSERT INTO monsters VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', sample_data)

    yield conn


def test_connection(populate_database):
    """ Test to make sure that all items are in the database"""

    conn = populate_database
    c = conn.cursor()
    c.execute('''SELECT COUNT(*) FROM monsters''')
    assert c.fetchone()[0] == 16
    c.execute('''DROP TABLE monsters''')


def test_ingest(setup_database):
    """ Test the ingest function """
    conn = setup_database
    c = conn.cursor()
    csv_string = convertor.load_csv_from_file("tal'dorei.csv")
    convertor.ingest_data(csv_string, "file::memory:?cache=shared")
    c.execute('''SELECT COUNT(*) FROM monsters''')
    assert c.fetchone()[0] == 16
    c.execute('''DROP TABLE monsters''')


def test_configure_db():
    """ Test the configure_db function """
    convertor.configure_db("file::memory:?cache=shared")
