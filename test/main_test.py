import unittest
from app.main import diff_calc, cr_calc, get_encounter_difficulty, get_monster_cr


class TestDifficultyCalculator(unittest.TestCase):
    def setUp(self):
        self.diff_calc = diff_calc

    def test_diff_calculator_returns_str(self):
        result = self.diff_calc([(4, 4)], 1250)
        self.assertEqual(type(result), type("string"))

    def test_diff_calculator_returns_correct_diff_for_one_level_party(self):
        self.assertEqual(self.diff_calc([(2, 5)], 10), "trifling")
        self.assertEqual(self.diff_calc([(8, 4)], 1500), "easy")
        self.assertEqual(self.diff_calc([(4, 1)], 200), "medium")
        self.assertEqual(self.diff_calc([(11, 9)], 17601), "hard")
        self.assertEqual(self.diff_calc([(1, 20)], 13000), "deadly")

    def test_diff_calculator_returns_correct_diff_for_multi_level_party(self):
        self.assertEqual(self.diff_calc([(4, 3), (1, 4)], 1000), "medium")
        self.assertEqual(self.diff_calc([(4, 3), (1, 4)], 2099), "hard")
        self.assertEqual(self.diff_calc([(4, 3), (1, 4)], 2100), "deadly")


class TestCrCalculator(unittest.TestCase):
    def setUp(self):
        self.cr_calc = cr_calc

    def test_cr_calculator_returns_int(self):
        result = self.cr_calc(["1"], [1])
        self.assertEqual(type(result), type(100))

    def test_cr_calculator_returns_correct_value_for_single_monsters(self):
        self.assertEqual(self.cr_calc(["5"], [1]), 1800)
        self.assertEqual(self.cr_calc(["1/2"], [1]), 100)

    def test_cr_calculator_returns_correct_value_for_multiple_identical_monsters(self):
        self.assertEqual(self.cr_calc(["5"], [2]), 5400)
        self.assertEqual(self.cr_calc(["3"], [5]), 7000)
        self.assertEqual(self.cr_calc(["7"], [9]), 65250)
        self.assertEqual(self.cr_calc(["4"], [14]), 46200)
        self.assertEqual(self.cr_calc(["0"], [20]), 800)

    def test_cr_calculator_returns_correct_value_for_multiple_dissimilar_monsters(self):
        self.assertEqual(self.cr_calc(["5", "3"], [3, 2]), 13600)


class TestGetMonsterCr(unittest.TestCase):
    def setUp(self):
        self.get_monster_cr = get_monster_cr

    def test_get_tarrasque_cr(self):
        self.assertEqual(self.get_monster_cr("Tarrasque"), "30")


class TestGetEncounterDifficulty(unittest.TestCase):
    def setUp(self):
        self.get_encounter_difficulty = get_encounter_difficulty

    def test_encounter_difficulty_single_level_single_monster(self):
        party = [(4, 3)]
        monsters = [("Air Elemental", 1)]
        self.assertEqual(self.get_encounter_difficulty(
            party, monsters), (1800, "deadly"))

    def test_encounter_difficulty_multiple_levels_single_monster(self):
        party = [(4, 3), (1, 4)]
        monsters = [("Air Elemental", 1)]
        self.assertEqual(self.get_encounter_difficulty(
            party, monsters), (1800, "hard"))

    def test_encounter_difficulty_multiple_levels_multiple_monsters_single_cr(self):
        party = [(4, 5), (1, 6)]
        monsters = [("Air Elemental", 2)]
        self.assertEqual(self.get_encounter_difficulty(
            party, monsters), (5400, "hard"))

    def test_encounter_difficulty_multiple_levels_multiple_monsters_multiple_cr(self):
        party = [(4, 5), (1, 6)]
        monsters = [("Air Elemental", 2), ("Allosaurus", 1)]
        self.assertEqual(self.get_encounter_difficulty(
            party, monsters), (8100, "deadly"))
