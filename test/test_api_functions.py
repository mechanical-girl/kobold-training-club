from ktc import api


def test_environment_list_returns_list():
    expected = type(list())
    actual = type(api.get_list_of_environments())
    assert expected == actual


def test_environment_list_returns_unique_list_of_environments():
    expected = ['aquatic', 'arctic', 'cave', 'coast', 'desert', 'dungeon', 'forest',
                'grassland', 'mountain', 'planar', 'ruins', 'swamp', 'underground', 'urban']
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
    expected = ["Aberration", "Beast", "Celestial", "Construct", "Dragon", "Elemental",
                "Fey", "Fiend", "Giant", "Humanoid", "Monstrosity", "Ooze", "Plant", "Undead"]
    actual = api.get_list_of_monster_types()
    assert expected == actual


def test_cr_list_returns_list():
    expected = type(list())
    actual = type(api.get_list_of_challenge_ratings())
    assert expected == actual


def test_cr_list_returns_unique_list_of_challenge_ratings():
    expected = ['0', '1/8', '1/4', '1/2', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
                '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '30']
    actual = api.get_list_of_challenge_ratings()
    assert expected == actual


def test_source_list_returns_unique_list_of_sources():
    expected = ['Basic Rules v1',  'Curse of Strahd',  'Fifth Edition Foes',  'Hoard of the Dragon Queen',  'HotDQ supplement',  'Monster Manual',  'Monster Module',  'Monster-A-Day',  "Nerzugal's Extended Bestiary",  'Out of the Abyss',  "Player's Handbook",
                'Primeval Thule Campaign Setting',  "Primeval Thule Gamemaster's Companion",  'Princes of the Apocalypse',  'Princes of the Apocalypse Online Supplement v1.0',  'Rise of Tiamat',  "Storm King's Thunder",  'Tales from the Yawning Portal',  'Tome of Beasts',  "Volo's Guide to Monsters"]
    actual = api.get_list_of_sources()
    assert expected == actual


def test_alignment_list_returns_list():
    expected = type(list())
    actual = type(api.get_list_of_alignments())
    assert expected == actual


def test_alignment_list_returns_unique_list_of_alignments():
    expected = ['any', 'any chaotic', 'any evil', 'any good', 'any lawful', 'chaotic evil', 'chaotic good', 'chaotic neutral', 'lawful evil',
                'lawful good', 'lawful good', 'lawful neutral', 'neutral', 'neutral evil', 'neutral good', 'neutral good ', 'non-good', 'non-lawful', 'unaligned']
    actual = api.get_list_of_alignments()
    assert expected == actual
