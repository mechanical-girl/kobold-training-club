import unittest
from ktc.api import get_list_of_environments


class TestApiEnvironmentList(unittest.TestCase):
    def test_environment_list_returns_list(self):
        expected = type(list())
        actual = type(get_list_of_environments())
        self.assertEqual(expected, actual)

    def test_environment_list_returns_unique_list_of_environments(self):
        expected = ['aquatic', 'arctic', 'cave', 'coast', 'desert', 'dungeon', 'forest',
                    'grassland', 'mountain', 'planar', 'ruins', 'swamp', 'underground', 'urban']
        actual = get_list_of_environments()
        self.assertEqual(expected, actual)
