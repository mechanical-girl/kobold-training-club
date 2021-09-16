# -*- coding: utf-8 -*-
import os
import sqlite3
from re import A

import pytest

from ktc import api, converter


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


def test_environment_list_returns_list():
    expected = type(list())
    actual = type(api.get_list_of_environments())
    assert expected == actual


def test_environment_list_returns_unique_list_of_environments():
    expected = [
        "aquatic",
        "arctic",
        "cave",
        "coast",
        "desert",
        "dungeon",
        "forest",
        "grassland",
        "mountain",
        "no environment specified",
        "planar",
        "ruins",
        "swamp",
        "underground",
        "urban",
    ]
    actual = api.get_list_of_environments()
    assert expected == actual


def test_size_list_returns_list():
    expected = type(list())
    actual = type(api.get_list_of_sizes())
    assert expected == actual


def test_size_list_returns_unique_list_of_sizes():
    expected = ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"]
    actual = api.get_list_of_sizes()
    assert expected == actual


def test_type_list_returns_list():
    expected = type(list())
    actual = type(api.get_list_of_monster_types())
    assert expected == actual


def test_type_list_returns_unique_list_of_monster_types():
    expected = [
        "Aberration",
        "Beast",
        "Celestial",
        "Construct",
        "Dragon",
        "Elemental",
        "Fey",
        "Fiend",
        "Giant",
        "Humanoid",
        "Monstrosity",
        "Ooze",
        "Plant",
        "Undead",
    ]
    actual = api.get_list_of_monster_types()
    assert expected == actual


def test_cr_list_returns_list():
    expected = type(list())
    actual = type(api.get_list_of_challenge_ratings())
    assert expected == actual


def test_cr_list_returns_unique_list_of_challenge_ratings():
    expected = [
        "0",
        "1/8",
        "1/4",
        "1/2",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "30",
    ]
    actual = api.get_list_of_challenge_ratings()
    assert expected == actual


def test_source_list_returns_unique_list_of_sources():
    expected = ["Baldur's Gate: Descent into Avernus",
                'Basic Rules v1',
                'Curse of Strahd',
                'Eberron: Rising from the Last War',
                'Explorer\'s Guide to Wildemount',
                'Ghosts of Saltmarsh',
                "Guildmasters' Guide to Ravnica",
                'Hoard of the Dragon Queen',
                'Icewind Dale: Rime of the Frost Maiden',
                'Into The Borderlands',
                'Monster Manual',
                "Mordenkainen's Tome of Foes",
                'Mythic Odysseys of Theros',
                'Out of the Abyss',
                "Player's Handbook",
                'Princes of the Apocalypse',
                'Rise of Tiamat',
                "Storm King's Thunder",
                'Tales from the Yawning Portal',
                "Volo's Guide to Monsters",
                'Waterdeep: Dragon Heist',
                'Waterdeep: Dungeon of the Mad Mage']
    actual = api.get_list_of_sources()
    assert expected == actual


def test_get_unofficial_sources_returns_good_data():
    expected = ["D&D Beyond",
                "Fifth Edition Foes",
                "HotDQ supplement",
                "Lost Mines of Phandelver",
                "Monster Module",
                "Monster-A-Day",
                "Nerzugal's Extended Bestiary",
                "Primeval Thule Campaign Setting",
                "Primeval Thule Gamemaster's Companion",
                "Princes of the Apocalypse Online Supplement v1.0",
                "Tome of Beasts",
                "Tome of Beasts II"]
    actual = api.get_unofficial_sources()
    assert expected == actual


def test_alignment_list_returns_list():
    expected = type(list())
    actual = type(api.get_list_of_alignments())
    assert expected == actual


def test_alignment_list_returns_unique_list_of_alignments():
    expected = ["any alignment",
                "any chaotic",
                "any evil",
                "any good",
                "any lawful",
                "any non-good",
                "chaotic evil",
                "chaotic good",
                "chaotic neutral",
                "lawful evil",
                "lawful good",
                "lawful neutral",
                "neutral",
                "neutral evil",
                "neutral good",
                "non-good",
                "non-lawful",
                "unaligned",
                ]
    actual = api.get_list_of_alignments()
    assert expected == actual


def test_cr_list_returns_list():
    expected = type(list())
    actual = type(api.get_list_of_challenge_ratings())
    assert expected == actual


def test_cr_list_returns_correct_list():
    expected = [
        "0",
        "1/8",
        "1/4",
        "1/2",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "30",
    ]
    actual = api.get_list_of_challenge_ratings()
    assert expected == actual


def test_monster_list_returns_full_list_if_no_parameters_passed():
    expected = [['Aarakocra',
                 '1/4',
                 'Medium',
                 'Humanoid',
                 'neutral good',
                 'Monster Manual: 12, Princes of the Apocalypse Online Supplement v1.0: 6'],
                ['Abhorrent Overlord',
                 '9',
                 'Large',
                 'Fiend',
                 'lawful evil',
                 'Mythic Odysseys of Theros: 219'],
                ['Abjurer', '9', 'Medium', 'Humanoid',
                    'any alignment', "Volo's Guide to Monsters: 209"],
                ['Aboleth',
                 '10',
                 'Large',
                 'Aberration',
                 'lawful evil',
                 'Monster Manual: 13, Princes of the Apocalypse Online Supplement v1.0: 6'],
                ['Abominable Yeti',
                 '9',
                 'Huge',
                 'Monstrosity',
                 'chaotic evil',
                 'Monster Manual: 306'],
                ['Abyssal Chicken',
                 '1/4',
                 'Tiny',
                 'Fiend',
                 'chaotic evil',
                 "Baldur's Gate: Descent into Avernus: 97"],
                ['Abyssal Wretch',
                '1/4',
                 'Medium',
                 'Fiend',
                 'chaotic evil',
                 "Baldur's Gate: Descent into Avernus: 118"],
                ['Acolyte',
                 '1/4',
                 'Medium',
                 'Humanoid',
                 'any alignment',
                 'Basic Rules v1: 53, HotDQ supplement: 4, Monster Manual: 342'],
                ['Adept',
                 '1',
                 'Medium',
                 'Humanoid',
                 'chaotic evil',
                 'Into The Borderlands: 338'],
                ['Adult Black Dragon',
                 '14',
                 'Huge',
                 'Dragon',
                 'chaotic evil',
                 'Monster Manual: 88, Princes of the Apocalypse Online Supplement v1.0: 7'],
                ['Adult Blue Dracolich',
                 '17',
                 'Huge',
                 'Undead',
                 'lawful evil',
                 'Monster Manual: 84'],
                ['Adult Blue Dragon',
                 '16',
                 'Huge',
                 'Dragon',
                 'lawful evil',
                 'HotDQ supplement: 4, Monster Manual: 91'],
                ['Adult Brass Dragon',
                 '13',
                 'Huge',
                 'Dragon',
                 'chaotic good',
                 'Monster Manual: 105'],
                ['Adult Bronze Dragon',
                 '15',
                 'Huge',
                 'Dragon',
                 'lawful good',
                 'Monster Manual: 108, Princes of the Apocalypse Online Supplement v1.0: 7'],
                ['Adult Copper Dragon',
                 '14',
                 'Huge',
                 'Dragon',
                 'chaotic good',
                 'Monster Manual: 112'],
                ['Adult Gold Dragon',
                 '17',
                 'Huge',
                 'Dragon',
                 'lawful good',
                 'Monster Manual: 114'],
                ['Adult Green Dragon',
                 '15',
                 'Huge',
                 'Dragon',
                 'lawful evil',
                 'Monster Manual: 94'],
                ['Adult Red Dragon',
                 '17',
                 'Huge',
                 'Dragon',
                 'chaotic evil',
                 'Basic Rules v1: 8, Monster Manual: 98'],
                ['Adult Silver Dragon',
                 '16',
                 'Huge',
                 'Dragon',
                 'lawful good',
                 'Monster Manual: 117'],
                ['Adult White Dragon',
                 '13',
                 'Huge',
                 'Dragon',
                 'chaotic evil',
                 'HotDQ supplement: 5, Monster Manual: 101'],
                ['Aeorian Hunter',
                 '10',
                 'Large',
                 'Monstrosity',
                 'neutral evil',
                 "Explorer's Guide to Wildemount: "],
                ['Aeorian Nullifier',
                 '12',
                 'Large',
                 'Monstrosity',
                 'neutral evil',
                 "Explorer's Guide to Wildemount: "]]
    actual = api.get_list_of_monsters({})["data"]
    assert len(actual) == 1140
    for i, item in enumerate(expected):
        assert item == actual[i]


def test_monster_list_returns_good_single_constraint_list():
    parameters = {"sizes": ["sizes_Medium", "sizes_Large"]}
    actual = api.get_list_of_monsters(parameters)["data"]
    for monster in actual:
        assert monster[2] in ["Medium", "Large"]


def test_monster_list_returns_good_multiple_constraint_list():
    expected = ['Aboleth', 'Adept', 'Arachnia, Giant Water Spider', 'Barbarian Warrior', 'Boalisk', 'Chuul', 'Crabman', 'Crocodile', 'Crushing Wave Priest', 'Crushing Wave Reaver', 'Dagon', 'Dark Tide Knight', 'Dark Triton', 'Deep Scion', 'Dolphin', 'Elite Bullywug', 'Elite Hobgoblin', 'Evil Priest', 'Eye of the Deep', 'Fanged Sea Serpent', 'Fathomer', 'Fledgling Mage', 'Four-Armed Gargoyle', 'Giant Armadillo', 'Giant Clam', 'Giant Crab', 'Giant Electric Catfish', 'Giant Frog', 'Giant Moray Eel', 'Giant Octopus', 'Giant Pike', 'Giant Sea Horse', 'Giant Seahorse', 'Giant Toad', 'Giant Water Beetle', 'Giant Water Spider', 'Gray Nisp', 'Green Guardian Gargoyle', 'Gulper Eel',
                'Hippocampus', 'Hunter Shark', 'Iron Cobra', 'Kraken Priest', 'Kuo-toa', 'Kuo-toa Archpriest', 'Kuo-toa Whip', 'Lithonnite', 'Living Stone Statue', 'Living Wax Statue', 'Mad Hermit', 'Marevak, Advisor to the Castellan', 'Margoyle', 'Marid', 'Marine Basilisk', 'Merfolk', 'Merfolk Hydromancer', 'Merrow', 'Monstrous Crayfish', 'Morkoth', 'Mummy of the Deep', 'Ogre Skeleton', 'One-Eyed Shiver', 'Orc Chief', 'Plesiosaurus', 'Reef Shark', 'Sahuagin', 'Sahuagin Baron', 'Sahuagin Priestess', 'Sea Hag', 'Sea Hag (coven)', 'Sea Spawn', 'Spitting Sea Serpent', 'Strangle Weed', 'Swarm of Quippers', 'Thalasskoptis', 'Thoul', 'Tortoise', 'Troglodyte Shaman', 'Troglodyte Spore Servant', 'Water Elemental', 'Water Elemental Myrmidon', 'Wizard Golem', 'Young Aboleth', 'Zombie']
    parameters = {
        "sizes": ["sizes_Medium", "sizes_Large"],
        "environments": ["environments_aquatic"],
    }
    actual = api.get_list_of_monsters(parameters)["data"]
    for i, monster in enumerate(actual):
        assert monster[2] in ["Medium", "Large"]
        assert expected[i] == monster[0]


def test_monster_list_returns_good_challenge_rating_constrained_list():
    expected = []
    parameters = {"minimumChallengeRating": "1", "maximumChallengeRating": "2"}
    actual = api.get_list_of_monsters(parameters)["data"]
    for monster in actual:
        assert monster[1] in ["1", "2"]


def test_monster_list_returns_good_source_constraint_list():
    parameters = {"sources": ["sources_Monster Manual"]}
    actual = api.get_list_of_monsters(parameters)["data"]
    for monster in actual:
        assert "Monster Manual" in monster[5]


def test_monster_list_returns_good_legendary_constraint_list():
    parameters = {"allowLegendary": "false"}
    actual = len(api.get_list_of_monsters(parameters)["data"])
    assert 2271 == actual


def test_monster_list_returns_good_named_constraint_list():
    parameters = {"allowNamed": "false"}
    actual = len(api.get_list_of_monsters(parameters)["data"])
    assert 2245 == actual


def test_monster_list_returns_good_all_constraint_list():
    parameters = {"environments": ["_aquatic", "_forest", "_dungeon"],
                  "sizes": ["_small", "_medium", "_large", "_huge"],
                  "sources": ["_Baldur's Gate: Descent into Avernus",
                              "_Basic Rules v1",
                              "_Curse of Strahd",
                              "_Eberron: Rising from the Last War",
                              "_Explorer's Guide to Wildemount",
                              "_Ghosts of Saltmarsh",
                              "_Hoard of the Dragon Queen",
                              "_Icewind Dale: Rime of the Frost Maiden",
                              "_Into The Borderlands",
                              "_Monster Manual",
                              "_Mordenkainen's Tome of Foes",
                              "_Mythic Odysseys of Theros",
                              "_Out of the Abyss",
                              "_Player's Handbook",
                              "_Princes of the Apocalypse",
                              "_Rise of Tiamat",
                              "_Storm King's Thunder",
                              "_Tales from the Yawning Portal",
                              "_Volo's Guide to Monsters",
                              "_Waterdeep: Dragon Heist",
                              "_Waterdeep: Dungeon of the Mad Mage"],
                  "types": ["_beast", "_humanoid", "_fiend", "_dragon", "_undead"],
                  "alignments": ["_unaligned", "_chaotic evil", "_lawful evil", "_neutral evil", "_neutral"],
                  "minimumChallengeRating": "1",
                  "maximumChallengeRating": "15",
                  "allowLegendary": "false",
                  "allowNamed": "false"
                  }
    actual = api.get_list_of_monsters(parameters)["data"]

    parameters["environments"] = [param[1:]
                                  for param in parameters["environments"]]
    parameters["sizes"] = [param[1:] for param in parameters["environments"]]
    parameters["sources"] = [param[1:] for param in parameters["sources"]]
    parameters["types"] = [param[1:] for param in parameters["types"]]
    parameters["alignments"] = [param[1:]
                                for param in parameters["alignments"]]

    for monster in actual:
        assert float(Fraction(parameters["minimumChallengeRating"])) < float(Fraction(
            monster[1])) < float(Fraction(parameters["maximumChallengeRating"]))
        assert monster[2] in parameters["sizes"]
        assert monster[3] in parameters["types"]
        assert monster[4] in parameters['alignments']
        for source in monster[5].split(","):
            assert ':'.join(source.split[":"][:-1]) in parameters['sources']


def test_xp_calculator_returns_good_data():
    party = [[4, 5], [1, 2]]
    expected = [1050, 2100, 3150, 4600, 14600]
    actual = api.get_party_thresholds(party)

    assert expected == actual


def test_get_encounter_xp():
    monsters = [['Aarakocra', 4]]
    expected = 400
    actual = api.get_encounter_xp(monsters)
    assert expected == actual


def test_ingest_custom_csv(setup_database):

    csv_string = converter.load_csv_from_file("tal'dorei.csv")
    conn = setup_database
    api.ingest_custom_csv_string(csv_string, "test.db",
                                 url="1D7GC4otl-WhhCqcJRe7KxzwZTPJBTU-gJ7dg9wUL-40")

    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM monsters")
    assert c.fetchone()[0] == 16
    os.remove("test.db")


def test_check_for_processed_source():
    expected = "Into The Borderlands"
    actual = converter.check_if_key_processed(
        "1NwjJS2Jpf_CxCZtHRCIJxc-6rERIo9vbFSqcs5ttE8M")

    assert expected == actual


def test_check_for_unprocessed_source():
    expected = ""
    actual = converter.check_if_key_processed(
        "1qlMY1vtJhrOlrLDxA476YxkxpSP5UYudqy4WyVBlHHo")

    assert expected == actual
