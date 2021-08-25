# -*- coding: utf-8 -*-
import pytest
from ktc import app
import json
from fractions import Fraction
import sqlite3


@pytest.fixture
def client():
    return app.app.test_client()


@pytest.fixture
def setup_database():
    """Fixture to setup an in-memory database"""
    conn = sqlite3.connect("test.db", uri=True)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS monsters")
    c.execute("DROP TABLE IF EXISTS sources")
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
                source text )''')
    c.execute('''CREATE TABLE sources(
                name text,
                official int,
                url text)''')

    yield conn


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
        "no environment specified",
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
    expected = ["Baldur's Gate: Descent into Avernus",
                'Basic Rules v1',
                'Curse of Strahd',
                'Eberron: Rising from the Last War',
                "Explorer's Guide to Wildemount",
                'Ghosts of Saltmarsh',
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
        "any alignment",
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
        "28",
        "30",
    ]
    response = client.get("/api/crs")
    received = response.get_json()
    assert expected == received


def test_monster_list_gives_json_with_proper_mimetype(client):
    response = client.get("/api/monsters")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_monster_list_gives_correct_list(client):
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
                    'any', "Volo's Guide to Monsters: 209"],
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
                ['Acolyte',
                 '1/4',
                 'Medium',
                 'Humanoid',
                 'any',
                 'Basic Rules v1: 53, HotDQ supplement: 4, Monster Manual: 342'],
                ['Adept',
                 '1',
                 'Medium',
                 'Humanoid',
                 'Chaotic Evil',
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
                 'Neutral Evil',
                 "Explorer's Guide to Wildemount"],
                ['Aeorian Nullifier',
                 '12',
                 'Large',
                 'Monstrosity',
                 'Neutral Evil',
                 "Explorer's Guide to Wildemount"]]
    response = client.get("/api/monsters")
    received = response.get_json()["data"]

    assert len(received) == 907
    for i, monster in enumerate(expected):
        assert monster == received[i]


def test_monster_list_returns_good_single_constraint_list(client):
    parameters = '{"sizes": ["sizes_Medium", "sizes_Large"]}'
    response = client.get("/api/monsters?params=" +
                          json.dumps(json.loads(parameters)))
    received = response.get_json()["data"]

    for monster in received:
        assert monster[2] in ["Medium", "Large"]


def test_monster_list_returns_good_multiple_constraint_list(client):
    expected = ['Aboleth', 'Adept', 'Arachnia, Giant Water Spider', 'Archdruid', 'Archdruid', 'Barbarian Warrior', 'Boalisk', 'Bone Golem', 'Caryatid Column', 'Chuul', 'Coffer Corpse', 'Crabman', 'Crocodile', 'Crushing Wave Priest', 'Crushing Wave Reaver', 'Dagon', 'Dark Tide Knight', 'Dark Triton', 'Deep Scion', 'Dolphin', 'Elite Bullywug', 'Elite Hobgoblin', 'Evil Priest', 'Eye of the Deep', 'Fanged Sea Serpent', 'Fathomer', 'Fledgling Mage', 'Four-Armed Gargoyle', 'Giant Armadillo', 'Giant Clam', 'Giant Crab', 'Giant Crayfish', 'Giant Electric Catfish', 'Giant Frog', 'Giant Moray Eel', 'Giant Octopus', 'Giant Pike', 'Giant Sea Horse', 'Giant Seahorse', 'Giant Toad', 'Giant Water Beetle', 'Giant Water Spider', 'Gray Nisp', 'Green Guardian Gargoyle', 'Gulper Eel',
                'Hippocampus', 'Hunter Shark', 'Iron Cobra', 'Kelpie', 'Kraken Priest', 'Kuo-toa', 'Kuo-toa Archpriest', 'Kuo-toa Whip', 'Lithonnite', 'Living Stone Statue', 'Living Wax Statue', 'Mad Hermit', 'Marevak, Advisor to the Castellan', 'Margoyle', 'Marid', 'Marine Basilisk', 'Merfolk', 'Merfolk Hydromancer', 'Merrow', 'Monstrous Crayfish', 'Morkoth', 'Mummy of the Deep', 'Ogre Skeleton', 'One-Eyed Shiver', 'Orc Chief', 'Plesiosaurus', 'Reef Shark', 'Sahuagin', 'Sahuagin Baron', 'Sahuagin Priestess', 'Sea Hag', 'Sea Hag (coven)', 'Sea Spawn', 'Spitting Sea Serpent', 'Strangle Weed', 'Swarm of Quippers', 'Thalasskoptis', 'Thoul', 'Tortoise', 'Troglodyte Shaman', 'Troglodyte Spore Servant', 'Water Elemental', 'Water Elemental Myrmidon', 'Wizard Golem', 'Young Aboleth', 'Zombie']
    parameters = '{"sizes": ["sizes_Medium", "sizes_Large"], "environments": ["environments_aquatic"]}'
    response = client.get("/api/monsters?params=" +
                          json.dumps(json.loads(parameters)))
    received = response.get_json()["data"]

    for i, monster in enumerate(received):
        assert monster[2] in ["Medium", "Large"]
        assert monster[0] == expected[i]


def test_monster_list_returns_good_source_constraint_list(client):
    parameters = '{"sources": ["sources_Monster Manual"]}'
    response = client.get("/api/monsters?params=" +
                          json.dumps(json.loads(parameters)))
    received = response.get_json()["data"]

    for monster in received:
        assert "Monster Manual" in monster[5]


def test_monster_list_returns_good_all_constraint_list(client):
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
                  "maximumChallengeRating": "15"
                  }
    print(json.dumps(parameters))
    response = client.get(f"/api/monsters?params={json.dumps(parameters)}")
    received = response.get_json()["data"]

    parameters["environments"] = [param[1:]
                                  for param in parameters["environments"]]
    parameters["sizes"] = [param[1:] for param in parameters["environments"]]
    parameters["sources"] = [param[1:] for param in parameters["sources"]]
    parameters["types"] = [param[1:] for param in parameters["types"]]
    parameters["alignments"] = [param[1:]
                                for param in parameters["alignments"]]

    for monster in received:
        print(monster[1])
        assert float(Fraction(parameters["minimumChallengeRating"])) < float(Fraction(
            monster[1])) < float(Fraction(parameters["maximumChallengeRating"]))
        assert monster[2] in parameters["sizes"]
        assert monster[3] in parameters["types"]
        assert monster[4] in parameters['alignments']
        for source in monster[5].split(","):
            assert ':'.join(source.split[":"][:-1]) in parameters['sources']


def test_exp_calc_gives_json_with_proper_mimetype(client):
    response = client.get("/api/expthresholds?party=" + str([[1, 1]]))
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_exp_calc_returns_good_data(client):
    party = [[4, 5], [1, 2]]
    expected = [1050, 2100, 3150, 4600, 14600]
    response = client.get("/api/expthresholds?party=" + str(party))
    received = response.get_json()

    assert expected == received


def test_encounter_xp_gives_json_with_proper_mimetype(client):
    monsters = [["Aarakocra", '4']]
    response = client.get("/api/encounterxp?monsters=" + json.dumps(monsters))
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_encounter_xp_returns_good_data(client):
    monsters = [["Aarakocra", '4']]
    expected = 400
    response = client.get(
        "/api/encounterxp?monsters=" + json.dumps(monsters))
    received = response.get_json()

    assert expected == received
