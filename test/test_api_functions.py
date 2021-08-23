# -*- coding: utf-8 -*-
from re import A
from ktc import api
import sqlite3
import pytest


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
        "30",
    ]
    actual = api.get_list_of_challenge_ratings()
    assert expected == actual


def test_source_list_returns_unique_list_of_sources():
    expected = [
        "Basic Rules v1",
        "Curse of Strahd",
        "Fifth Edition Foes",
        "Hoard of the Dragon Queen",
        "HotDQ supplement",
        "Monster Manual",
        "Monster Module",
        "Monster-A-Day",
        "Nerzugal's Extended Bestiary",
        "Out of the Abyss",
        "Player's Handbook",
        "Primeval Thule Campaign Setting",
        "Primeval Thule Gamemaster's Companion",
        "Princes of the Apocalypse",
        "Princes of the Apocalypse Online Supplement v1.0",
        "Rise of Tiamat",
        "Storm King's Thunder",
        "Tales from the Yawning Portal",
        "Tome of Beasts",
        "Volo's Guide to Monsters",
    ]
    actual = api.get_list_of_sources()
    assert expected == actual


def test_alignment_list_returns_list():
    expected = type(list())
    actual = type(api.get_list_of_alignments())
    assert expected == actual


def test_alignment_list_returns_unique_list_of_alignments():
    expected = [
        "any",
        "any chaotic",
        "any evil",
        "any good",
        "any lawful",
        "chaotic evil",
        "chaotic good",
        "chaotic neutral",
        "lawful evil",
        "lawful good",
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
        "30",
    ]
    actual = api.get_list_of_challenge_ratings()
    assert expected == actual


def test_monster_list_returns_full_list_if_no_parameters_passed():
    expected = [
        [
            "Aarakocra",
            "1/4",
            "Medium",
            "Humanoid",
            "neutral good",
            "Monster Manual: 12, Princes of the Apocalypse Online Supplement v1.0: 6",
        ],
        [
            "Aarakocra Captain",
            "3",
            "Medium",
            "Humanoid",
            "neutral good",
            "Monster Module: 3",
        ],
        [
            "Aarakocra Priest of Aerdrie",
            "8",
            "Medium",
            "Humanoid",
            "neutral good",
            "Monster Module: 4",
        ],
        [
            "Aarakocra Sharpshooter",
            "1/2",
            "Medium",
            "Humanoid",
            "neutral good",
            "Monster Module: 3",
        ],
        [
            "Aaztar-Ghola",
            "4",
            "Medium",
            "Humanoid",
            "chaotic evil",
            "Fifth Edition Foes: 5",
        ],
        ["Abjurer", "9", "Medium", "Humanoid",
            "any", "Volo's Guide to Monsters: 209"],
        [
            "Aboleth",
            "10",
            "Large",
            "Aberration",
            "lawful evil",
            "Monster Manual: 13, Princes of the Apocalypse Online Supplement v1.0: 6",
        ],
        [
            "Aboleth Sovereign",
            "16",
            "Huge",
            "Aberration",
            "lawful evil",
            "Monster Module: 5",
        ],
        [
            "Abominable Beauty",
            "11",
            "Medium",
            "Fey",
            "neutral evil",
            "Tome of Beasts: 11",
        ],
        [
            "Abominable Sloth",
            "6",
            "Huge",
            "Beast",
            "unaligned",
            "Primeval Thule Campaign Setting: 220",
        ],
        [
            "Abominable Yeti",
            "9",
            "Huge",
            "Monstrosity",
            "chaotic evil",
            "Monster Manual: 306",
        ],
        [
            "Accursed Defiler",
            "4",
            "Medium",
            "Undead",
            "neutral evil",
            "Tome of Beasts: 12",
        ],
        [
            "Acolyte",
            "1/4",
            "Medium",
            "Humanoid",
            "any",
            "Basic Rules v1: 53, HotDQ supplement: 4, Monster Manual: 342",
        ],
        [
            "Adherer",
            "2",
            "Medium",
            "Aberration",
            "lawful evil",
            "Fifth Edition Foes: 6",
        ],
        [
            "Adult Black Dragon",
            "14",
            "Huge",
            "Dragon",
            "chaotic evil",
            "Monster Manual: 88, Princes of the Apocalypse Online Supplement v1.0: 7",
        ],
        [
            "Adult Blue Dracolich",
            "17",
            "Huge",
            "Undead",
            "lawful evil",
            "Monster Manual: 84",
        ],
        [
            "Adult Blue Dragon",
            "16",
            "Huge",
            "Dragon",
            "lawful evil",
            "HotDQ supplement: 4, Monster Manual: 91",
        ],
        [
            "Adult Brass Dragon",
            "13",
            "Huge",
            "Dragon",
            "chaotic good",
            "Monster Manual: 105",
        ],
        [
            "Adult Bronze Dragon",
            "15",
            "Huge",
            "Dragon",
            "lawful good",
            "Monster Manual: 108, Princes of the Apocalypse Online Supplement v1.0: 7",
        ],
        [
            "Adult Cave Dragon",
            "16",
            "Huge",
            "Dragon",
            "neutral evil",
            "Tome of Beasts: 125",
        ],
    ]
    actual = api.get_list_of_monsters({})["data"]
    assert len(actual) == 1643
    for i, item in enumerate(expected):
        assert item == actual[i]


def test_monster_list_returns_good_single_constraint_list():
    parameters = {"sizes": ["sizes_Medium", "sizes_Large"]}
    actual = api.get_list_of_monsters(parameters)["data"]
    for monster in actual:
        assert monster[2] in ["Medium", "Large"]


def test_monster_list_returns_good_multiple_constraint_list():
    expected = [
        "Aboleth",
        "Archdruid",
        "Boalisk",
        "Chuul",
        "Crabman",
        "Crocodile",
        "Crushing Wave Priest",
        "Crushing Wave Reaver",
        "Dagon",
        "Dark Tide Knight",
        "Dark Triton",
        "Deep Scion",
        "Dolphin",
        "Eye of the Deep",
        "Fanged Sea Serpent",
        "Fathomer",
        "Four-Armed Gargoyle",
        "Giant Clam",
        "Giant Crab",
        "Giant Electric Catfish",
        "Giant Frog",
        "Giant Moray Eel",
        "Giant Octopus",
        "Giant Sea Horse",
        "Giant Seahorse",
        "Giant Toad",
        "Giant Water Beetle",
        "Gray Nisp",
        "Green Guardian Gargoyle",
        "Gulper Eel",
        "Hippocampus",
        "Hunter Shark",
        "Kelpie",
        "Kraken Priest",
        "Kuo-toa",
        "Kuo-toa Archpriest",
        "Kuo-toa Whip",
        "Lithonnite",
        "Margoyle",
        "Marid",
        "Marine Basilisk",
        "Merfolk",
        "Merfolk Hydromancer",
        "Merrow",
        "Monstrous Crayfish",
        "Morkoth",
        "Mummy of the Deep",
        "One-Eyed Shiver",
        "Plesiosaurus",
        "Reef Shark",
        "Sahuagin",
        "Sahuagin Baron",
        "Sahuagin Priestess",
        "Sea Hag",
        "Sea Hag (coven)",
        "Sea Spawn",
        "Spitting Sea Serpent",
        "Strangle Weed",
        "Swarm of Quippers",
        "Thalasskoptis",
        "Tortoise",
        "Water Elemental",
        "Water Elemental Myrmidon",
        "Young Aboleth",
        "Zombie",
    ]
    parameters = {
        "sizes": ["sizes_Medium", "sizes_Large"],
        "environments": ["environments_aquatic"],
    }
    actual = api.get_list_of_monsters(parameters)["data"]
    print([item[0] for item in actual])
    for i, monster in enumerate(actual):
        assert monster[2] in ["Medium", "Large"]
        assert monster[0] == expected[i]


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
    source = """fid,name,cr,size,type,tags,section,alignment,environment,ac,hp,init,lair?,legendary?,unique?,sources
veiled.abigor,Abigor,6,Medium,Fiend,Devil,,lawful evil,,18,19,1,,,,Veiled Threats: 3
veiled.barathrum,Barathrum,11,Large,Construct,,,unaligned,,12,189,-1,,,,Veiled Threats: 4
veiled.blackthraw,Blackthraw,2,Small,Fiend,Devil,,l#awful evil,,12,36,2,,,,Veiled Threats: 5
veiled.cankerbeast,Cankerbeast,9,Large,Aberration,,Cankerbeast,neutral evil,,15,114,1,,legendary,,Veiled Threats: 7
veiled.cankerbeast-larva,Cankerbeast Larva,1/4,Small,Ooze,,Cankerbeast,neutral evil,,9,19,-1,,,,Veiled Threats: 8
veiled.captain-hogsblood,"Captain Hogsblood",23,Large,Fiend,Devil,,lawful evil,,21,300,3,,legendary,unique,Veiled Threats: 10
veiled.fleetflesh-doppelganger,Fleetflesh Doppelganger,5,Medium,Monstrosity,Shapechanger,"Doppelganger, Fleetflesh",neutral evil,,14,84,4,,,,Veiled Threats: 12
veiled.feralshifter-doppelganger,Feralshifter Doppelganger,4,Medium,Monstrosity,Shapechanger,"Doppelganger, Fleetflesh",neutral evil,,16,84,4,,,,Veiled Threats: 13
veiled.fleshsplitter-doppelganger,Fleshsplitter Doppelganger,5,Medium,Monstrosity,Shapechanger,"Doppelganger, Fleetflesh",chaotic neutral or chaotic evil,,14,84,4,,,,Veiled Threats: 13
veiled.eshaedra-old-blue-dragon,"Eshaedra, Old Blue Dragon",20,Huge,Dragon,,,lawful evil,,20,351,0,,legendary,unique,Veiled Threats: 15
veiled.eshaedra-old-blue-dragon-gifted-worshipper,"Eshaedra, Old Blue Dragon (Gifted Worshipper)",24,Huge,Dragon,,,lawful evil,,20,351,0,,legendary,unique,Veiled Threats: 15
veiled.gerasa,Gerasa,2,Medium,Fiend,Devil,,lawful evil,,17,26,1,,,,Veiled Threats: 16
veiled.githyanki-harrier,Githyanki Harrier,12,Medium,Humanoid,Gith,,lawful evil,,19,105,2,,,,Veiled Threats: 17
veiled.grimjaw-hound,Grimjaw Hound,1/2,Medium,Beast,,,unaligned,,12,19,1,,,,Veiled Threats: 18
veiled.fiendish-grimjaw,Fiendish Grimjaw,3,Large,Fiend,,,neutral evil,,14,60,0,,,,Veiled Threats: 18
veiled.halphus,Halphus,9,Medium,Fiend,Devil,,lawful evil,,18,102,-1,,,,Veiled Threats. 19
veiled.macroscian,Macroscian,9,Large,Undead,,,chaotic evil,,15,144,5,,,,Veiled Threats: 21
veiled.mindsnare-naga,Mindsnare Naga,10,Large,Monstrosity,,,lawful evil,,16,119,4,,,,Veiled Threats: 22
veiled.nothic-ascendant,Nothic Ascendant,3,Medium,Aberration,,Nothic Savant,neutral evil,,15,45,3,,,,Veiled Threats: 24
veiled.nothic-savant,Nothic Savant,10,Medium,Aberration,,Nothic Savant,neutral evil,,15,105,3,,legendary,,Veiled Threats: 25
veiled.nothic-savant-in-lair,Nothic Savant (in lair),11,Medium,Aberration,,Nothic Savant,neutral evil,,15,105,3,lair,legendary,,Veiled Threats 25
veiled.ogre-slug,Ogre Slug,4,Large,Monstrosity,,,chaotic evil,,12,104,-1,,,,Veiled Threats: 26
veiled.selktas-veld-altraloth-guardian,"Selktas-Veld, Altraloth Guardian",17,Huge,Fiend,Yugoloth,,neutral evil,,20,300,-1,,legendary,unique,Veiled Threats: 28
veiled.giant-slug-large,Giant Slug (Large),3,Large,Beast,,,unaligned,,11,85,-2,,,,Veiled Threats: 29
veiled.giant-slug-huge,Giant Slug (Huge),5,Huge,Beast,,,unaligned,,11,136,-2,,,,Veiled Threats: 29
veiled.giant-bolas-spider,Giant Bolas Spider,3,Large,Beast,,,unaligned,,14,52,3,,,,Veiled Threats: 30
veiled.giant-jumping-spider,Giant Jumping Spider,1,Small,Beast,,,unaligned,,14,18,4,,,,Veiled Threats: 31
veiled.giant-gladiator-spider,Giant Gladiator Spider,3,Large,Beast,,,unaligned,,14,52,3,,,,Veiled Threats: 32
veiled.giant-spitting-spider,Giant Spitting Spider,2,Medium,Beast,,,unaligned,,13,45,2,,,,Veiled Threats: 32
veiled.giant-six-eyed-sand-spider,Giant Six-Eyed Sand Spider,1/2,Medium,Beast,,,unaligned,,13,11,3,,,,Veiled Threats: 33"""
    conn = setup_database
    api.ingest_custom_csv_string(source, "file::memory:?cache=shared",
                                 url="1ayOpMBbMd7ay2gOVhsZqyQEbQmP5liKnPuV_jcNkjRk")

    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM monsters")
    assert c.fetchone()[0] == 30
