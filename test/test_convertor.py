# -*- coding: utf-8 -*-
import pytest
from ktc import converter
import sqlite3
import os


@pytest.fixture
def setup_database():
    """Fixture to setup an in-memory database"""
    try:
        os.remove("test.db")
    except FileNotFoundError:
        pass

    conn = sqlite3.connect("test.db", uri=True)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS monsters")
    c.execute("DROP TABLE IF EXISTS sources")
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

    yield conn


@pytest.fixture
def populate_database(setup_database):
    conn = setup_database
    c = conn.cursor()

    sample_data = [["tcs.ashari-firetamer", " Ashari Firetamer", " 7", " Medium", " Humanoid", " neutral good", " no environment specified", " 17", " 92", " 2", " ", " ", " ", " Tal'Dorei Campaign Setting: 128", " 0x64654ff7750489ef2e2a9ae135e408a4d2a40811"],
                   ["tcs.ashari-stoneguard", " Ashari Stoneguard", " 7", " Medium", " Humanoid", " lawful good", " no environment specified",
                       " 15", " 152", " 0", " ", " ", " ", " Tal'Dorei Campaign Setting: 128", " 0x64654ff7750489ef2e2a9ae135e408a4d2a40811"],
                   ["tcs.ashari-waverider", " Ashari Waverider", " 4", " Medium", " Humanoid", " neutral good", " no environment specified",
                       " 14", " 77", " 2", " ", " ", " ", " Tal'Dorei Campaign Setting: 129", " 0x64654ff7750489ef2e2a9ae135e408a4d2a40811"],
                   ["tcs.ashari-skydancer", " Ashari Skydancer", " 5", " Medium", " Humanoid", " chaotic neutral", " no environment specified",
                       " 14", " 63", " 4", " ", " ", " ", " Tal'Dorei Campaign Setting: 129", " 0x64654ff7750489ef2e2a9ae135e408a4d2a40811"],
                   ["tcs.cinderslag-elemantal", " Cinderslag Elemantal", " 5", " Large", " Elemental", " chaotic evil", " no environment specified",
                       " 15", " 102", " 1", " ", " ", " ", " Tal'Dorei Campaign Setting: 130", " 0x64654ff7750489ef2e2a9ae135e408a4d2a40811"],
                   ["tcs.clasp-cutthroat", " Clasp Cutthroat", " 3", " Medium", " Humanoid", " non-lawful", " no environment specified",
                       " 14", " 44", " 3", " ", " ", " ", " Tal'Dorei Campaign Setting: 131", " 0x64654ff7750489ef2e2a9ae135e408a4d2a40811"],
                   ["tcs.clasp-enforcer", " Clasp Enforcer", " 5", " Medium", " Humanoid", " non-lawful", " no environment specified",
                       " 16", " 102", " 1", " ", " ", " ", " Tal'Dorei Campaign Setting: 131", " 0x64654ff7750489ef2e2a9ae135e408a4d2a40811"],
                   ["tcs.cyclops-stormcaller", " Cyclops Stormcaller", " 10", " Large", " Giant", " neutral evil", " no environment specified",
                       " 18", " 119", " 0", " ", " ", " ", " Tal'Dorei Campaign Setting: 132", " 0x64654ff7750489ef2e2a9ae135e408a4d2a40811"],
                   ["tcs.goliath-stormborn", " Goliath Stormborn", " 4", " Medium", " Humanoid", " chaotic neutral", " no environment specified",
                       " 13", " 102", " 1", " ", " ", " ", " Tal'Dorei Campaign Setting: 133", " 0x64654ff7750489ef2e2a9ae135e408a4d2a40811"],
                   ["tcs.goliath-brawler", " Goliath Brawler", " 3", " Medium", " Humanoid", " chaotic neutral", " no environment specified",
                       " 15", " 65", " 2", " ", " ", " ", " Tal'Dorei Campaign Setting: 134", " 0x64654ff7750489ef2e2a9ae135e408a4d2a40811"],
                   ["tcs.kraghammer-goat-knight", " Kraghammer Goat-Knight", " 3", " Medium", " Humanoid", " neutral good", " no environment specified",
                       " 20", " 52", " -1", " ", " ", " ", " Tal'Dorei Campaign Setting: 134", " 0x64654ff7750489ef2e2a9ae135e408a4d2a40811"],
                   ["tcs.goat-knight-steed", " Goat-Knight Steed", " 1/2", " Large", " Celestial", " unaligned", " no environment specified",
                       " 11", " 19", " 0", " ", " ", " ", " Tal'Dorei Campaign Setting: 135", " 0x64654ff7750489ef2e2a9ae135e408a4d2a40811"],
                   ["tcs.ravager-stabby-stabber", " Ravager Stabby-Stabber", " 2", " Small", " Humanoid", " chaotic evil", " no environment specified",
                       " 15", " 36", " 3", " ", " ", " ", " Tal'Dorei Campaign Setting: 137", " 0x64654ff7750489ef2e2a9ae135e408a4d2a40811"],
                   ["tcs.ravager-slaughter-lord", " Ravager Slaughter Lord", " 9", " Large", " Humanoid", " lawful evil", " no environment specified",
                       " 17", " 152", " 2", " ", " ", " ", " Tal'Dorei Campaign Setting: 137", " 0x64654ff7750489ef2e2a9ae135e408a4d2a40811"],
                   ["tcs.remnant-cultist", " Remnant Cultist", " 7", " Medium", " Humanoid", " neutral evil", " no environment specified",
                       " 13", " 60", " 3", " ", " ", " ", " Tal'Dorei Campaign Setting: 139", " 0x64654ff7750489ef2e2a9ae135e408a4d2a40811"],
                   ["tcs.remnant-chosen", " Remnant Chosen", " 12", " Medium", " Humanoid", " neutral evil", " no environment specified", " 12", " 117", " 2", " ", " ", " ", " Tal'Dorei Campaign Setting: 139", " 0x64654ff7750489ef2e2a9ae135e408a4d2a40811"]]

    c.executemany(
        '''INSERT INTO monsters VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', sample_data)

    yield conn


def test_connection(populate_database):
    """ Test to make sure that all items are in the database"""

    conn = populate_database
    c = conn.cursor()
    c.execute('''SELECT COUNT(*) FROM monsters''')
    assert c.fetchone()[0] == 16
    os.remove("test.db")


def test_ingest(setup_database):
    """ Test the ingest function """
    conn = setup_database
    c = conn.cursor()
    csv_string = converter.load_csv_from_file("tal'dorei.csv")
    converter.ingest_data(csv_string, "test.db")
    c.execute('''SELECT COUNT(*) FROM monsters''')
    print(c.fetchone())
    #assert c.fetchone()[0] == 16
    os.remove("test.db")


def test_configure_db():
    """ Test the configure_db function """
    converter.configure_db("test.db")
    os.remove("test.db")
