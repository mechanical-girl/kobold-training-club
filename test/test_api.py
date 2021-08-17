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
                'lawful good', 'lawful good', 'lawful neutral', 'neutral', 'neutral evil', 'neutral good', 'non-good', 'non-lawful', 'unaligned']
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
    response = client.get("/api/monsters")
    received = response.get_json()

    for i, monster in enumerate(expected):
        assert monster == received[i]


def test_monster_list_returns_good_single_constraint_list(client):
    expected = [{'alignment': 'neutral good',  'cr': '1/4',  'name': 'Aarakocra',  'size': 'Medium',  'sources': 'Monster Manual: 12, Princes of the Apocalypse Online Supplement '  'v1.0: 6',  'type': 'Humanoid'},  {'alignment': 'neutral good',  'cr': '3',  'name': 'Aarakocra Captain',  'size': 'Medium',  'sources': 'Monster Module: 3',  'type': 'Humanoid'},  {'alignment': 'neutral good',  'cr': '8',  'name': 'Aarakocra Priest of Aerdrie',  'size': 'Medium',  'sources': 'Monster Module: 4',  'type': 'Humanoid'},  {'alignment': 'neutral good',  'cr': '1/2',  'name': 'Aarakocra Sharpshooter',  'size': 'Medium',  'sources': 'Monster Module: 3',  'type': 'Humanoid'},  {'alignment': 'chaotic evil',  'cr': '4',  'name': 'Aaztar-Ghola',  'size': 'Medium',  'sources': 'Fifth Edition Foes: 5',  'type': 'Humanoid'},  {'alignment': 'any',  'cr': '9',  'name': 'Abjurer',  'size': 'Medium',  'sources': "Volo's Guide to Monsters: 209",  'type': 'Humanoid'},  {'alignment': 'lawful evil',  'cr': '10',  'name': 'Aboleth',  'size': 'Large',  'sources': 'Monster Manual: 13, Princes of the Apocalypse Online Supplement '  'v1.0: 6',  'type': 'Aberration'},  {'alignment': 'neutral evil',  'cr': '11',  'name': 'Abominable Beauty',  'size': 'Medium',  'sources': 'Tome of Beasts: 11',  'type': 'Fey'},  {'alignment': 'neutral evil',  'cr': '4',  'name': 'Accursed Defiler',  'size': 'Medium',  'sources': 'Tome of Beasts: 12',  'type': 'Undead'},  {'alignment': 'any',  'cr': '1/4',  'name': 'Acolyte',  'size': 'Medium',  'sources': 'Basic Rules v1: 53, HotDQ supplement: 4, Monster Manual: 342',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     'type': 'Humanoid'},  {'alignment': 'lawful evil',  'cr': '2',  'name': 'Adherer',  'size': 'Medium',  'sources': 'Fifth Edition Foes: 6',  'type': 'Aberration'},  {'alignment': 'chaotic evil',  'cr': '2',  'name': 'Adult Leucrotta',  'size': 'Large',  'sources': 'Fifth Edition Foes: 164',  'type': 'Monstrosity'},  {'alignment': 'neutral',  'cr': '6',  'name': 'Adult Rime Worm',  'size': 'Large',  'sources': 'Tome of Beasts: 327',  'type': 'Elemental'},  {'alignment': 'neutral',  'cr': '9',  'name': 'Aerial Servant',  'size': 'Medium',  'sources': 'Fifth Edition Foes: 7',  'type': 'Fiend'},  {'alignment': 'neutral evil',  'cr': '7',  'name': 'Aerisi Kalinoth',  'size': 'Medium',  'sources': 'Princes of the Apocalypse: 192',  'type': 'Humanoid'},  {'alignment': 'neutral evil',  'cr': '9',  'name': 'Aerisi Kalinoth (in lair)',  'size': 'Medium',  'sources': 'Princes of the Apocalypse: 192',  'type': 'Humanoid'},  {'alignment': 'Lawful Good',  'cr': '4',  'name': 'Agathion',  'size': 'Medium',  'sources': 'Monster Module: 7',  'type': 'Celestial'},  {'alignment': 'neutral',  'cr': '5',  'name': 'Air Elemental',  'size': 'Large',  'sources': 'Basic Rules v1: 9, HotDQ supplement: 5, Monster Manual: 124',  'type': 'Elemental'},  {'alignment': 'neutral',  'cr': '7',  'name': 'Air Elemental Myrmidon',  'size': 'Medium',  'sources': 'Princes of the Apocalypse: 212',  'type': 'Elemental'},  {'alignment': 'chaotic evil',  'cr': '12',  'name': 'Akyishigal, Demon Lord of Cockroaches',  'size': 'Large',  'sources': 'Tome of Beasts: 82',  'type': 'Fiend'}]
    parameters = {"sizes": ["sizes_Medium", "sizes_Large"]}
    response = client.get("/api/monsters?params="+str(parameters))
    received = response.get_json()

    for i, monster in enumerate(expected):
        assert monster == received[i]


def test_monster_list_returns_good_multiple_constraint_list(client):
    expected = [{'alignment': 'neutral', 'cr': '1', 'name': 'Crabman', 'size': 'Large', 'sources': 'Fifth Edition Foes: 69', 'type': 'Monstrosity'}, {'alignment': 'chaotic evil', 'cr': '1', 'name': 'Dark Triton', 'size': 'Large', 'sources': 'Fifth Edition Foes: 233', 'type': 'Monstrosity'}, {'alignment': 'neutral evil', 'cr': '5', 'name': 'Fanged Sea Serpent', 'size': 'Large', 'sources': 'Fifth Edition Foes: 201', 'type': 'Dragon'}, {'alignment': 'unaligned', 'cr': '1/4', 'name': 'Giant Clam', 'size': 'Large', 'sources': 'Fifth Edition Foes: 61', 'type': 'Beast'}, {'alignment': 'unaligned', 'cr': '3', 'name': 'Giant Electric Catfish', 'size': 'Large', 'sources': 'Fifth Edition Foes: 46', 'type': 'Beast'}, {'alignment': 'unaligned', 'cr': '2', 'name': 'Giant Moray Eel', 'size': 'Medium', 'sources': 'Fifth Edition Foes: 91', 'type': 'Beast'}, {'alignment': 'unaligned', 'cr': '1', 'name': 'Giant Octopus', 'size': 'Large', 'sources': 'Basic Rules v1: 26, Monster Manual: 326', 'type': 'Beast'}, {'alignment': 'unaligned', 'cr': '1/2', 'name': 'Giant Sea Horse', 'size': 'Large', 'sources': 'Basic Rules v1: 27, Monster Manual: 328', 'type': 'Beast'}, {'alignment': 'unaligned', 'cr': '1/2', 'name': 'Giant Seahorse', 'size': 'Large', 'sources': 'Fifth Edition Foes: 205', 'type': 'Beast'}, {'alignment': 'unaligned', 'cr': '1/2', 'name': 'Giant Water Beetle', 'size': 'Medium', 'sources': 'Fifth Edition Foes: 25', 'type': 'Beast'}, {'alignment': 'chaotic neutral',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'cr': '6', 'name': 'Gray Nisp', 'size': 'Large', 'sources': 'Fifth Edition Foes: 133', 'type': 'Fey'}, {'alignment': 'unaligned', 'cr': '3', 'name': 'Gulper Eel', 'size': 'Large', 'sources': 'Fifth Edition Foes: 92', 'type': 'Beast'}, {'alignment': 'chaotic good', 'cr': '1', 'name': 'Hippocampus', 'size': 'Large', 'sources': 'Fifth Edition Foes: 144', 'type': 'Monstrosity'}, {'alignment': 'unaligned', 'cr': '2', 'name': 'Hunter Shark', 'size': 'Large', 'sources': 'Basic Rules v1: 33, Monster Manual: 330', 'type': 'Beast'}, {'alignment': 'neutral evil', 'cr': '1', 'name': 'Kelpie', 'size': 'Medium', 'sources': 'Fifth Edition Foes: 156', 'type': 'Plant'}, {'alignment': 'neutral', 'cr': '1/8', 'name': 'Merfolk', 'size': 'Medium', 'sources': 'Basic Rules v1: 35, Monster Manual: 218', 'type': 'Humanoid'}, {'alignment': 'chaotic evil', 'cr': '2', 'name': 'Merrow', 'size': 'Large', 'sources': 'Monster Manual: 219, Princes of the Apocalypse Online Supplement '            'v1.0: 25', 'type': 'Monstrosity'}, {'alignment': 'unaligned', 'cr': '2', 'name': 'Monstrous Crayfish', 'size': 'Large', 'sources': 'Fifth Edition Foes: 70', 'type': 'Beast'}, {'alignment': 'neutral evil', 'cr': '2', 'name': 'Mummy of the Deep', 'size': 'Medium', 'sources': 'Fifth Edition Foes: 173', 'type': 'Undead'}, {'alignment': 'unaligned', 'cr': '2', 'name': 'Plesiosaurus', 'size': 'Large', 'sources': 'Basic Rules v1: 40, Monster Manual: 80', 'type': 'Beast'}]
    parameters = {"sizes": ["sizes_Medium", "sizes_Large"],
                  "environments": ["environments_aquatic"]}
    response = client.get("/api/monsters?params="+str(parameters))
    received = response.get_json()

    for i, monster in enumerate(expected):
        assert monster == received[i]


def test_monster_list_returns_good_source_constraint_list(client):
    expected = [{'alignment': 'neutral good', 'cr': '1/4', 'name': 'Aarakocra', 'size': 'Medium', 'sources': 'Monster Manual: 12, Princes of the Apocalypse Online Supplement v1.0: 6', 'type': 'Humanoid'}, {'alignment': 'lawful evil', 'cr': '10', 'name': 'Aboleth', 'size': 'Large', 'sources': 'Monster Manual: 13, Princes of the Apocalypse Online Supplement v1.0: 6', 'type': 'Aberration'}, {'alignment': 'chaotic evil', 'cr': '9', 'name': 'Abominable Yeti', 'size': 'Huge', 'sources': 'Monster Manual: 306', 'type': 'Monstrosity'}, {'alignment': 'any', 'cr': '1/4', 'name': 'Acolyte', 'size': 'Medium', 'sources': 'Basic Rules v1: 53, HotDQ supplement: 4, Monster Manual: 342', 'type': 'Humanoid'}, {'alignment': 'chaotic evil', 'cr': '14', 'name': 'Adult Black Dragon', 'size': 'Huge', 'sources': 'Monster Manual: 88, Princes of the Apocalypse Online Supplement v1.0: 7', 'type': 'Dragon'}, {'alignment': 'lawful evil', 'cr': '17', 'name': 'Adult Blue Dracolich', 'size': 'Huge', 'sources': 'Monster Manual: 84', 'type': 'Undead'}, {'alignment': 'lawful evil', 'cr': '16', 'name': 'Adult Blue Dragon', 'size': 'Huge', 'sources': 'HotDQ supplement: 4, Monster Manual: 91', 'type': 'Dragon'}, {'alignment': 'chaotic good', 'cr': '13', 'name': 'Adult Brass Dragon', 'size': 'Huge', 'sources': 'Monster Manual: 105', 'type': 'Dragon'}, {'alignment': 'lawful good', 'cr': '15', 'name': 'Adult Bronze Dragon', 'size': 'Huge', 'sources': 'Monster Manual: 108, Princes of the Apocalypse Online Supplement v1.0: 7', 'type': 'Dragon'}, {'alignment': 'chaotic good', 'cr': '14', 'name': 'Adult Copper Dragon',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         'size': 'Huge', 'sources': 'Monster Manual: 112', 'type': 'Dragon'}, {'alignment': 'lawful good', 'cr': '17', 'name': 'Adult Gold Dragon', 'size': 'Huge', 'sources': 'Monster Manual: 114', 'type': 'Dragon'}, {'alignment': 'lawful evil', 'cr': '15', 'name': 'Adult Green Dragon', 'size': 'Huge', 'sources': 'Monster Manual: 94', 'type': 'Dragon'}, {'alignment': 'chaotic evil', 'cr': '17', 'name': 'Adult Red Dragon', 'size': 'Huge', 'sources': 'Basic Rules v1: 8, Monster Manual: 98', 'type': 'Dragon'}, {'alignment': 'lawful good', 'cr': '16', 'name': 'Adult Silver Dragon', 'size': 'Huge', 'sources': 'Monster Manual: 117', 'type': 'Dragon'}, {'alignment': 'chaotic evil', 'cr': '13', 'name': 'Adult White Dragon', 'size': 'Huge', 'sources': 'HotDQ supplement: 5, Monster Manual: 101', 'type': 'Dragon'}, {'alignment': 'neutral', 'cr': '5', 'name': 'Air Elemental', 'size': 'Large', 'sources': 'Basic Rules v1: 9, HotDQ supplement: 5, Monster Manual: 124', 'type': 'Elemental'}, {'alignment': 'unaligned', 'cr': '2', 'name': 'Allosaurus', 'size': 'Large', 'sources': 'Basic Rules v1: 9, Monster Manual: 79', 'type': 'Beast'}, {'alignment': 'chaotic evil', 'cr': '21', 'name': 'Ancient Black Dragon', 'size': 'Gargantuan', 'sources': 'Monster Manual: 87', 'type': 'Dragon'}, {'alignment': 'lawful evil', 'cr': '23', 'name': 'Ancient Blue Dragon', 'size': 'Gargantuan', 'sources': 'Monster Manual: 90', 'type': 'Dragon'}, {'alignment': 'chaotic good', 'cr': '20', 'name': 'Ancient Brass Dragon', 'size': 'Gargantuan', 'sources': 'Monster Manual: 104', 'type': 'Dragon'}]
    parameters = {"sources": ["sources_Monster Manual"]}
    response = client.get("/api/monsters?params="+str(parameters))
    received = response.get_json()

    for i, monster in enumerate(expected):
        assert monster == received[i]
