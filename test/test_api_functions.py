from ktc.api import get_list_of_environments, get_list_of_sizes


def test_environment_list_returns_list():
    expected = type(list())
    actual = type(get_list_of_environments())
    assert expected == actual


def test_environment_list_returns_unique_list_of_environments():
    expected = ['aquatic', 'arctic', 'cave', 'coast', 'desert', 'dungeon', 'forest',
                'grassland', 'mountain', 'planar', 'ruins', 'swamp', 'underground', 'urban']
    actual = get_list_of_environments()
    assert expected == actual


def test_size_list_returns_list():
    expected = type(list())
    actual = type(get_list_of_sizes())
    assert expected == actual


def test_size_list_returns_unique_list_of_sizes():
    expected = ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"]
    actual = get_list_of_sizes()
    assert expected == actual
