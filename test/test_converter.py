# -*- coding: utf-8 -*-

import pytest

from ktc.converter import configure_db, ingest_data, load_csv_from_file


@pytest.fixture
def setup_database():
    conn = configure_db("testing.db")
    yield conn


@pytest.fixture
def populate_database(setup_database):
    conn = setup_database
    c = conn.cursor()

    csv_string = """fid,name,cr,size,type,tags,section,alignment,environment,ac,hp,init,lair?,legendary?,unique?,sources,
mot.monster_one,Monster One, 1, Medium,,,,,,,,,,,,Mythic Odysseys of Theros: 123,
mot.monster_two,Monster Two, 1, Medium,,,,,,,,,,,,Mythic Odysseys of Theros: 123,
kuk.monster_three,Monster Three, 1, Medium,,,,,,,,,,,,Klarota's Underdark Kingdom: 456,
kuk.monster_four,Monster Four, 1, Medium,,,,,,,,,,,,Klarota's Underdark Kingdom: 456,
mot.monster_five,Monster Five, 1, Medium,,,,,,,,,,,,Mythic Odysseys of Theros: 123,
kuk.monster_five,Monster Five (KUK), 1, Medium,,,,,,,,,,,,Klarota's Underdark Kingdom: 456,
mot.monster_six,Monster Six, 1, Medium,,,,,,,,,,,,Mythic Odysseys of Theros: 123,
kuk.monster_six,Monster Six (KUK), 1, Medium,,,,,,,,,,,,Klarota's Underdark Kingdom: 456,"""
    ingest_data(csv_string, "testing.db", "abc123ericthehalfabee")

    yield conn

    c.execute('''DROP TABLE monsters''')
    c.execute('''DROP TABLE sources''')


def test_official_in_db_official_added(populate_database):
    """Expected behaviour: official is updated with new source"""
    conn = populate_database
    c = conn.cursor()

    csv_string = """fid,name,cr,size,type,tags,section,alignment,environment,ac,hp,init,lair?,legendary?,unique?,sources,
gos.monster_one,Monster One, 1, Medium,,,,,,,,,,,,Ghosts of Saltmarsh: 123,"""
    ingest_data(csv_string, "testing.db", "ahahaheheheericthehalfabee")

    c.execute(
        '''SELECT name, sources FROM monsters WHERE name = "Monster One"''')
    src = c.fetchall()[0]
    print(src)

    assert src[0] == "Monster One"
    assert src[1] == "Ghosts of Saltmarsh: 123, Mythic Odysseys of Theros: 123"


def test_official_in_db_unofficial_monster_added(populate_database):
    """Expected behaviour: official is left untouched, unofficial name has (KUK) added to the end"""
    conn = populate_database
    c = conn.cursor()

    csv_string = """fid,name,cr,size,type,tags,section,alignment,environment,ac,hp,init,lair?,legendary?,unique?,sources,
kuk.monster_two,Monster Two, 1, Medium,,,,,,,,,,,,Klarota's Underdark Kingdom: 456"""
    ingest_data(csv_string, "testing.db", "ahahaheheheericthehalfabee")

    c.execute(
        '''SELECT name, sources FROM monsters WHERE name LIKE "%Monster Two%"''')
    monster_list = c.fetchall()

    assert ("Monster Two (KUK)",
            "Klarota's Underdark Kingdom: 456") in monster_list
    assert ("Monster Two",
            "Mythic Odysseys of Theros: 123") in monster_list


def test_unofficial_in_db_official_added(populate_database):
    """Expected behaviour: official is created, unofficial name has (KUK) added to the end"""
    conn = populate_database
    c = conn.cursor()

    csv_string = """fid,name,cr,size,type,tags,section,alignment,environment,ac,hp,init,lair?,legendary?,unique?,sources,
kuk.monster_three,Monster Three, 1, Medium,,,,,,,,,,,,Mythic Odysseys of Theros: 123,"""
    ingest_data(csv_string, "testing.db", "ahahaheheheericthehalfabee")

    c.execute(
        '''SELECT name, sources FROM monsters WHERE name LIKE "%Monster Three%"''')
    monster_list = c.fetchall()
    print(monster_list)

    assert ("Monster Three (KUK)",
            "Klarota's Underdark Kingdom: 456") in monster_list
    assert ("Monster Three",
            "Mythic Odysseys of Theros: 123") in monster_list


def test_unofficial_in_db_unofficial_added(populate_database):
    """Expected behaviour: existing unofficial is unchanged, new unofficial name has (MUS) added to the end"""
    conn = populate_database
    c = conn.cursor()

    csv_string = """fid,name,cr,size,type,tags,section,alignment,environment,ac,hp,init,lair?,legendary?,unique?,sources,
mus.monster_four,Monster Four, 1, Medium,,,,,,,,,,,,Mythic Undead Servants: 123,"""
    ingest_data(csv_string, "testing.db", "ahahaheheheericthehalfabee")

    c.execute(
        '''SELECT name, sources FROM monsters WHERE name LIKE "%Monster Four%"''')
    monster_list = c.fetchall()

    assert ("Monster Four (KUK)",
            "Klarota's Underdark Kingdom: 456") in monster_list
    assert ("Monster Four (MUS)",
            "Mythic Undead Servants: 123") in monster_list


def test_both_in_db_official_added(populate_database):
    """Expected behaviour: existing unofficial is unchanged, existing official has new sources added"""
    conn = populate_database
    c = conn.cursor()

    csv_string = """fid,name,cr,size,type,tags,section,alignment,environment,ac,hp,init,lair?,legendary?,unique?,sources,
gos.monster_five,Monster Five, 1, Medium,,,,,,,,,,,,Ghosts of Saltmarsh: 123,"""
    ingest_data(csv_string, "testing.db", "ahahaheheheericthehalfabee")

    c.execute(
        '''SELECT name, sources FROM monsters WHERE name LIKE "%Monster Five%"''')
    monster_list = c.fetchall()

    assert ("Monster Five (KUK)",
            "Klarota's Underdark Kingdom: 456") in monster_list
    assert ("Monster Five",
            "Ghosts of Saltmarsh: 123, Mythic Odysseys of Theros: 123") in monster_list


def test_both_in_db_unofficial_added(populate_database):
    """Expected behaviour: existing official is unchanged, existing unofficial has new sources added"""
    conn = populate_database
    c = conn.cursor()

    csv_string = """fid,name,cr,size,type,tags,section,alignment,environment,ac,hp,init,lair?,legendary?,unique?,sources,
mus.monster_six,Monster Six, 1, Medium,,,,,,,,,,,,Mythic Undead Servants: 123,"""
    ingest_data(csv_string, "testing.db", "ahahaheheheericthehalfabee")

    c.execute(
        '''SELECT name, sources FROM monsters WHERE name LIKE "%Monster Six%"''')
    monster_list = c.fetchall()

    assert ("Monster Six (KUK)",
            "Klarota's Underdark Kingdom: 456") in monster_list
    assert ("Monster Six (MUS)",
            "Mythic Undead Servants: 123") in monster_list
    assert ("Monster Six",
            "Mythic Odysseys of Theros: 123") in monster_list


def test_neither_in_db_official_added(populate_database):
    """Expected behaviour: official is created"""
    conn = populate_database
    c = conn.cursor()

    csv_string = """fid,name,cr,size,type,tags,section,alignment,environment,ac,hp,init,lair?,legendary?,unique?,sources,
mot.monster_seven,Monster Seven, 1, Medium,,,,,,,,,,,,Mythic Odysseys of Theros: 123,"""
    ingest_data(csv_string, "testing.db", "ahahaheheheericthehalfabee")

    c.execute(
        '''SELECT name, sources FROM monsters WHERE name LIKE "%Monster Seven%"''')
    monster_list = c.fetchall()

    assert ("Monster Seven",
            "Mythic Odysseys of Theros: 123") in monster_list


def test_neither_in_db_unofficial_added(populate_database):
    """Expected behaviour: unofficial is created without (KUK)"""
    conn = populate_database
    c = conn.cursor()

    csv_string = """fid,name,cr,size,type,tags,section,alignment,environment,ac,hp,init,lair?,legendary?,unique?,sources,
kuk.monster_seven,Monster Seven, 1, Medium,,,,,,,,,,,,Klarota's Underdark Kingdom: 456,"""
    ingest_data(csv_string, "testing.db", "ahahaheheheericthehalfabee")

    c.execute(
        '''SELECT name, sources FROM monsters WHERE name LIKE "%Monster Seven%"''')
    monster_list = c.fetchall()

    assert ("Monster Seven",
            "Klarota's Underdark Kingdom: 456") in monster_list
