# -*- coding: utf-8 -*-
from ktc.main import diff_calc, cr_calc, get_encounter_difficulty, get_monster_cr


class TestDifficultyCalculator:
    def test_diff_calculator_returns_str(self):
        result = diff_calc([(4, 4)], 1250)
        assert type(result) == type("string")

    def test_diff_calculator_returns_correct_diff_for_one_level_party(self):
        assert diff_calc([(2, 5)], 10) == "trifling"
        assert diff_calc([(8, 4)], 1500) == "easy"
        assert diff_calc([(4, 1)], 200) == "medium"
        assert diff_calc([(11, 9)], 17601) == "hard"
        assert diff_calc([(1, 20)], 13000) == "deadly"

    def test_diff_calculator_returns_correct_diff_for_multi_level_party(self):
        assert diff_calc([(4, 3), (1, 4)], 1000) == "medium"
        assert diff_calc([(4, 3), (1, 4)], 2099) == "hard"
        assert diff_calc([(4, 3), (1, 4)], 2100) == "deadly"


class TestCrCalculator:
    def test_cr_calculator_returns_int(self):
        result = cr_calc(["1"], [1])
        assert type(result) == type(100)

    def test_cr_calculator_returns_correct_value_for_single_monsters(self):
        assert cr_calc(["5"], [1]) == 1800
        assert cr_calc(["1/2"], [1]) == 100

    def test_cr_calculator_returns_correct_value_for_multiple_identical_monsters(self):
        assert cr_calc(["5"], [2]) == 5400
        assert cr_calc(["3"], [5]) == 7000
        assert cr_calc(["7"], [9]) == 65250
        assert cr_calc(["4"], [14]) == 46200
        assert cr_calc(["0"], [20]) == 800

    def test_cr_calculator_returns_correct_value_for_multiple_dissimilar_monsters(self):
        assert cr_calc(["5", "3"], [3, 2]) == 13600


class TestGetMonsterCr:
    def test_get_tarrasque_cr(self):
        assert get_monster_cr("Tarrasque") == "30"


class TestGetEncounterDifficulty:
    def test_encounter_difficulty_single_level_single_monster(self):
        party = [(4, 3)]
        monsters = [("Air Elemental", 1)]
        assert get_encounter_difficulty(party, monsters) == (1800, "deadly")

    def test_encounter_difficulty_multiple_levels_single_monster(self):
        party = [(4, 3), (1, 4)]
        monsters = [("Air Elemental", 1)]
        assert get_encounter_difficulty(party, monsters) == (1800, "hard")

    def test_encounter_difficulty_multiple_levels_multiple_monsters_single_cr(self):
        party = [(4, 5), (1, 6)]
        monsters = [("Air Elemental", 2)]
        assert get_encounter_difficulty(party, monsters) == (5400, "hard")

    def test_encounter_difficulty_multiple_levels_multiple_monsters_multiple_cr(self):
        party = [(4, 5), (1, 6)]
        monsters = [("Air Elemental", 2), ("Allosaurus", 1)]
        assert get_encounter_difficulty(party, monsters) == (8100, "deadly")
