import pytest
from ktc import app
import json


@pytest.fixture
def client():
    return app.app.test_client()


def test_environments_gives_json_with_proper_mimetype(client):
    response = client.get("/api/environments")
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_environments_gives_correct_list(client):
    expected = ['aquatic', 'arctic', 'cave', 'coast', 'desert', 'dungeon', 'forest',
                'grassland', 'mountain', 'planar', 'ruins', 'swamp', 'underground', 'urban']
    response = client.get("/api/environments")
    received = response.get_json()
    assert expected == received


def test_size_gives_json_with_proper_mimetype(client):
    response = client.get("/api/sizes")
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_size_gives_json_with_sizes(client):
    expected = ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"]
    response = client.get("/api/sizes")
    received = response.get_json()
    assert expected == received


def test_cr_list_gives_json_with_proper_mimetype(client):
    response = client.get("/api/crs")
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_cr_list_gives_correct_list(client):
    expected = ['0', '1/8', '1/4', '1/2', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
                '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '30']
    response = client.get("/api/crs")
    received = response.get_json()
    assert expected == received


def test_source_list_gives_json_with_proper_mimetype(client):
    response = client.get("/api/sources")
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_source_list_gives_correct_list(client):
    expected = ['Basic Rules v1',  'Curse of Strahd',  'Fifth Edition Foes',  'Hoard of the Dragon Queen',  'HotDQ supplement',  'Monster Manual',  'Monster Module',  'Monster-A-Day',  "Nerzugal's Extended Bestiary",  'Out of the Abyss',  "Player's Handbook",
                'Primeval Thule Campaign Setting',  "Primeval Thule Gamemaster's Companion",  'Princes of the Apocalypse',  'Princes of the Apocalypse Online Supplement v1.0',  'Rise of Tiamat',  "Storm King's Thunder",  'Tales from the Yawning Portal',  'Tome of Beasts',  "Volo's Guide to Monsters"]
    response = client.get("/api/sources")
    received = response.get_json()
    assert expected == received


def test_type_list_gives_json_with_proper_mimetype(client):
    response = client.get("/api/types")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_type_list_gives_correct_list(client):
    expected = ["Aberration", "Beast", "Celestial", "Construct", "Dragon", "Elemental",
                "Fey", "Fiend", "Giant", "Humanoid", "Monstrosity", "Ooze", "Plant", "Undead"]
    response = client.get("/api/types")
    received = response.get_json()
    assert expected == received


def test_alignment_list_gives_json_with_proper_mimetype(client):
    response = client.get("/api/alignments")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_alignment_list_gives_correct_list(client):
    expected = ['any', 'any chaotic', 'any evil', 'any good', 'any lawful', 'chaotic evil', 'chaotic good', 'chaotic neutral', 'lawful evil',
                'lawful good', 'lawful good', 'lawful neutral', 'neutral', 'neutral evil', 'neutral good', 'neutral good ', 'non-good', 'non-lawful', 'unaligned']
    response = client.get("/api/alignments")
    received = response.get_json()
    assert expected == received


def test_monster_list_gives_json_with_proper_mimetype(client):
    response = client.get("/api/monsters")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_monster_list_gives_correct_list(client):
    expected = [{'alignment': 'neutral good', 'cr': '1/4', 'name': 'Aarakocra', 'size': 'Medium', 'sources': 'Monster Manual: 12, Princes of the Apocalypse Online Supplement v1.0: 6', 'type': 'Humanoid'}, {'alignment': 'neutral good', 'cr': '3', 'name': 'Aarakocra Captain', 'size': 'Medium', 'sources': 'Monster Module: 3', 'type': 'Humanoid'}, {'alignment': 'neutral good', 'cr': '8', 'name': 'Aarakocra Priest of Aerdrie', 'size': 'Medium', 'sources': 'Monster Module: 4', 'type': 'Humanoid'}, {'alignment': 'neutral good', 'cr': '1/2', 'name': 'Aarakocra Sharpshooter', 'size': 'Medium', 'sources': 'Monster Module: 3', 'type': 'Humanoid'}, {'alignment': 'chaotic evil', 'cr': '4', 'name': 'Aaztar-Ghola', 'size': 'Medium', 'sources': 'Fifth Edition Foes: 5', 'type': 'Humanoid'}, {'alignment': 'any', 'cr': '9', 'name': 'Abjurer', 'size': 'Medium', 'sources': "Volo's Guide to Monsters: 209", 'type': 'Humanoid'}, {'alignment': 'lawful evil', 'cr': '10', 'name': 'Aboleth', 'size': 'Large', 'sources': 'Monster Manual: 13, Princes of the Apocalypse Online Supplement v1.0: 6', 'type': 'Aberration'}, {'alignment': 'lawful evil', 'cr': '16', 'name': 'Aboleth Sovereign', 'size': 'Huge', 'sources': 'Monster Module: 5', 'type': 'Aberration'}, {'alignment': 'neutral evil', 'cr': '11', 'name': 'Abominable Beauty', 'size': 'Medium', 'sources': 'Tome of Beasts: 11', 'type': 'Fey'}, {'alignment': 'unaligned', 'cr': '6', 'name': 'Abominable Sloth', 'size': 'Huge', 'sources': 'Primeval Thule Campaign Setting: 220', 'type': 'Beast'},
                {'alignment': 'chaotic evil', 'cr': '9', 'name': 'Abominable Yeti', 'size': 'Huge', 'sources': 'Monster Manual: 306', 'type': 'Monstrosity'}, {'alignment': 'neutral evil', 'cr': '4', 'name': 'Accursed Defiler', 'size': 'Medium', 'sources': 'Tome of Beasts: 12', 'type': 'Undead'}, {'alignment': 'any', 'cr': '1/4', 'name': 'Acolyte', 'size': 'Medium', 'sources': 'Basic Rules v1: 53, HotDQ supplement: 4, Monster Manual: 342', 'type': 'Humanoid'}, {'alignment': 'lawful evil', 'cr': '2', 'name': 'Adherer', 'size': 'Medium', 'sources': 'Fifth Edition Foes: 6', 'type': 'Aberration'}, {'alignment': 'chaotic evil', 'cr': '14', 'name': 'Adult Black Dragon', 'size': 'Huge', 'sources': 'Monster Manual: 88, Princes of the Apocalypse Online Supplement v1.0: 7', 'type': 'Dragon'}, {'alignment': 'lawful evil', 'cr': '17', 'name': 'Adult Blue Dracolich', 'size': 'Huge', 'sources': 'Monster Manual: 84', 'type': 'Undead'}, {'alignment': 'lawful evil', 'cr': '16', 'name': 'Adult Blue Dragon', 'size': 'Huge', 'sources': 'HotDQ supplement: 4, Monster Manual: 91', 'type': 'Dragon'}, {'alignment': 'chaotic good', 'cr': '13', 'name': 'Adult Brass Dragon', 'size': 'Huge', 'sources': 'Monster Manual: 105', 'type': 'Dragon'}, {'alignment': 'lawful good', 'cr': '15', 'name': 'Adult Bronze Dragon', 'size': 'Huge', 'sources': 'Monster Manual: 108, Princes of the Apocalypse Online Supplement v1.0: 7', 'type': 'Dragon'}, {'alignment': 'neutral evil', 'cr': '16', 'name': 'Adult Cave Dragon', 'size': 'Huge', 'sources': 'Tome of Beasts: 125', 'type': 'Dragon'}]
    response = client.get("/api/monsters?params=[]")
    received = response.get_json()

    for i, monster in enumerate(expected):
        assert monster == received[i]
