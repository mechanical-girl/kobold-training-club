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

    assert received == expected


def test_size_gives_json_with_proper_mimetype(client):
    response = client.get("/api/sizes")
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_size_gives_json_with_sizes(client):
    expected = ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"]
    response = client.get("/api/sizes")
    received = response.get_json()

    assert received == expected


def test_cr_list_gives_json_with_proper_mimetype(client):
    response = client.get("/api/crs")
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_cr_list_gives_correct_list(client):
    expected = ['0', '1/8', '1/4', '1/2', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
                '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '30']
    response = client.get("/api/crs")
    received = response.get_json()

    assert received == expected


def test_source_list_gives_json_with_proper_mimetype(client):
    response = client.get("/api/sources")
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_source_list_gives_correct_list(client):
    expected = ['Basic Rules v1',  'Curse of Strahd',  'Fifth Edition Foes',  'Hoard of the Dragon Queen',  'HotDQ supplement',  'Monster Manual',  'Monster Module',  'Monster-A-Day',  "Nerzugal's Extended Bestiary",  'Out of the Abyss',  "Player's Handbook",
                'Primeval Thule Campaign Setting',  "Primeval Thule Gamemaster's Companion",  'Princes of the Apocalypse',  'Princes of the Apocalypse Online Supplement v1.0',  'Rise of Tiamat',  "Storm King's Thunder",  'Tales from the Yawning Portal',  'Tome of Beasts',  "Volo's Guide to Monsters"]
    response = client.get("/api/sources")
    received = response.get_json()

    assert received == expected
