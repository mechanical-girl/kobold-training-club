# -*- coding: utf-8 -*-
import pytest
from ktc import app
import json


@pytest.fixture
def client():
    return app.app.test_client()


def test_environments_gives_json_with_proper_mimetype(client):
    response = client.get("/api/environments")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_environments_gives_correct_list(client):
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
        "planar",
        "ruins",
        "swamp",
        "underground",
        "urban",
    ]
    response = client.get("/api/environments")
    received = response.get_json()
    assert expected == received


def test_size_gives_json_with_proper_mimetype(client):
    response = client.get("/api/sizes")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_size_gives_json_with_sizes(client):
    expected = ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"]
    response = client.get("/api/sizes")
    received = response.get_json()
    assert expected == received


def test_cr_list_gives_json_with_proper_mimetype(client):
    response = client.get("/api/crs")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_cr_list_gives_correct_list(client):
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
    response = client.get("/api/crs")
    received = response.get_json()
    assert expected == received


def test_source_list_gives_json_with_proper_mimetype(client):
    response = client.get("/api/sources")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_source_list_gives_correct_list(client):
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
    response = client.get("/api/sources")
    received = response.get_json()
    assert expected == received


def test_type_list_gives_json_with_proper_mimetype(client):
    response = client.get("/api/types")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_type_list_gives_correct_list(client):
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
    response = client.get("/api/types")
    received = response.get_json()
    assert expected == received


def test_alignment_list_gives_json_with_proper_mimetype(client):
    response = client.get("/api/alignments")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_alignment_list_gives_correct_list(client):
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
    response = client.get("/api/alignments")
    received = response.get_json()
    assert expected == received


def test_cr_list_gives_json_with_proper_mimetype(client):
    response = client.get("/api/crs")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_cr_list_gives_correct_list(client):
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
    response = client.get("/api/crs")
    received = response.get_json()
    print(received)
    assert expected == received


def test_monster_list_gives_json_with_proper_mimetype(client):
    response = client.get("/api/monsters")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_monster_list_gives_correct_list(client):
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
        ["Abjurer", "9", "Medium", "Humanoid", "any", "Volo's Guide to Monsters: 209"],
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
    response = client.get("/api/monsters")
    received = response.get_json()["data"]

    assert len(received) == 1643
    for i, monster in enumerate(expected):
        assert monster == received[i]


def test_monster_list_returns_good_single_constraint_list(client):
    parameters = {"sizes": ["sizes_Medium", "sizes_Large"]}
    response = client.get("/api/monsters?params=" + str(parameters))
    received = response.get_json()["data"]

    for monster in received:
        assert monster[2] in ["Medium", "Large"]


def test_monster_list_returns_good_multiple_constraint_list(client):
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
    response = client.get("/api/monsters?params=" + str(parameters))
    received = response.get_json()["data"]

    for i, monster in enumerate(received):
        assert monster[2] in ["Medium", "Large"]
        assert monster[0] == expected[i]


def test_monster_list_returns_good_source_constraint_list(client):
    parameters = {"sources": ["sources_Monster Manual"]}
    response = client.get("/api/monsters?params=" + str(parameters))
    received = response.get_json()["data"]

    for monster in received:
        assert "Monster Manual" in monster[5]
