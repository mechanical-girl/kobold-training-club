# -*- coding: utf-8 -*-
import random
from fractions import Fraction
from typing import Dict, List, Tuple

try:
    import api  # type: ignore
    import main  # type: ignore
except ModuleNotFoundError:
    from ktc import api  # type: ignore
    from ktc import main  # type: ignore


class Monster:
    """Just a simple monster object. Attributes & nothing else
    """

    def __init__(self, monster_as_list: List[str]):
        self.name = monster_as_list[0]
        self.cr = monster_as_list[1]
        self.size = monster_as_list[2]
        self.type = monster_as_list[3]
        self.tags = monster_as_list[4]
        self.section = monster_as_list[5]
        self.alignment = monster_as_list[6]
        self.sources = monster_as_list[7]


def fits_rarity(monster, encounter_rarity):
    monster_cr = float(Fraction(monster[1]))
    if monster_cr < rarity_thresholds[0]:
        monster_rarity = 0
    elif monster_cr < rarity_thresholds[1]:
        monster_rarity = 1
    elif monster_cr < rarity_thresholds[2]:
        monster_rarity = 2
    else:
        monster_rarity = 3

    try:
        # TODO allow user to define rarity modifiers
        monster_rarity += taldorei_type_rarity_modifiers[monster[3].lower()]
    except KeyError:
        monster_rarity = 3
    if monster_rarity > 3:
        monster_rarity = 3

    if rarities[monster_rarity] in encounter_rarity:
        return True
    return False


def randomise_within_cr(monsters: List[Monster]) -> List[List[Monster]]:
    monsters_by_cr = []
    crs = [monster.cr for monster in monsters]
    crs = list(set(crs))
    crs.sort(key=lambda x: float(Fraction(x)))
    for cr in crs[::-1]:
        cr_monsters = [monster for monster in monsters if monster.cr == cr]
        random.shuffle(cr_monsters)
        monsters_by_cr.append(cr_monsters)

    return monsters_by_cr


rarities = ["common", "uncommon", "rare", "very rare"]
rarity_thresholds = [7, 15, 22]

taldorei_type_rarity_modifiers = {"aberration": 1, "beast": 0, "celestial": 2, "construct": 1, "dragon": 1, "elemental": 1,
                                  "fey": 1, "fiend": 2, "giant": +1, "humanoid": 0, "monstrosity": 1, "ooze": 1, "plant": 1, "undead": 0}


def generate(params: Dict) -> List[Tuple[int, str]]:
    if "environments" in params:
        environments = params["environments"]
    else:
        environments = []

    if "sources" in params:
        sources = params["sources"]
    else:
        sources = ['_Basic Rules v1',
                   '_Curse of Strahd',
                   '_Explorer\'s Guide to Wildemount',
                   '_Ghosts of Saltmarsh',
                   "_Guildmasters' Guide to Ravnica",
                   '_Hoard of the Dragon Queen',
                   '_Icewind Dale: Rime of the Frost Maiden',
                   '_Into The Borderlands',
                   '_Monster Manual',
                   "_Mordenkainen's Tome of Foes",
                   '_Mythic Odysseys of Theros',
                   '_Out of the Abyss',
                   "_Player's Handbook",
                   '_Princes of the Apocalypse',
                   '_Rise of Tiamat',
                   "_Storm King's Thunder",
                   '_Tales from the Yawning Portal',
                   "_Volo's Guide to Monsters",
                   '_Waterdeep: Dragon Heist',
                   '_Waterdeep: Dungeon of the Mad Mage']

    if "difficulty" in params and params["difficulty"] in ["easy", "medium", "hard", "deadly"]:
        difficulty = params["difficulty"]
    else:
        difficulty = "hard"

    if "party" in params:
        party = params["party"]
    else:
        party = [(4, 1)]

    # roll d8 + d12 to determine creature rarities
    rarity_roll = random.randint(1, 9) + random.randint(1, 13)

    if rarity_roll < 4 or rarity_roll > 18:
        encounter_rarity = ["very rare"]
    elif rarity_roll == 4 or rarity_roll == 18:
        encounter_rarity = ["very rare", "rare"]
    elif rarity_roll < 7 or rarity_roll > 15:
        encounter_rarity = ["rare"]
    elif rarity_roll < 9 or rarity_roll > 13:
        encounter_rarity = ["uncommon"]
    else:
        encounter_rarity = ["common"]

    # Select all monsters matching environment and source constraints
    possible_monsters = api.get_list_of_monsters(
        {"environments": environments,
         "sources": sources,
         "allowLegendary": False,
         "allowNamed": False, })["data"]

    # Filter those monsters to match the required rarity
    ordered_monsters = [Monster(monster) for monster in possible_monsters if fits_rarity(
        monster, encounter_rarity)]

    # Calculate the CR range for the encounter
    thresholds = main.party_thresholds_calc(party)
    if difficulty == "trifling":
        upper_xp = thresholds[0]
        lower_xp = 0
    elif difficulty == "easy":
        upper_xp = thresholds[1]
        lower_xp = thresholds[0]
    elif difficulty == "medium":
        upper_xp = thresholds[2]
        lower_xp = thresholds[1]
    elif difficulty == "hard":
        upper_xp = thresholds[3]
        lower_xp = thresholds[2]
    else:
        upper_xp = thresholds[4]/2
        lower_xp = thresholds[3]

    while True:
        # Add a beginning monster
        # Specifically, this will be 1-3 monsters randomly selected
        # and the only check made here is that that selection doesn't
        # violate the encounter's upper difficulty constraint.
        # TODO: Fix this bloody encounter DS, for the love of god. Use a List[Tuple[str, int]]
        while True:
            monster = random.choice(ordered_monsters)
            quantity = random.randint(1, 3)
            if main.cr_calc([monster.cr], [quantity]) < upper_xp:
                encounter_monsters = [monster.name]
                encounter_quantities = [quantity]
                encounter_monster_crs = [monster.cr]
                break

        coherent_monsters = [
            mon for mon in ordered_monsters if mon.type == monster.type]

        # Sort monsters by CR ascending
        monsters_by_cr = randomise_within_cr(coherent_monsters)

        monsters_by_cr = randomise_within_cr(coherent_monsters)
        for challenge_rating in monsters_by_cr:
            # breakpoint()
            # We know the CR of all these monsters is the same, so all we need to do
            # is figure out how many of these CRs makes an encounter of the right difficulty
            proposed_crs = encounter_monster_crs + [challenge_rating[0].cr]
            proposed_quantities = encounter_quantities + [0]
            while upper_xp > main.cr_calc(proposed_crs, proposed_quantities) and proposed_quantities[-1] < 4:
                # Find the max number of this CR of monster we can add.
                # breakpoint
                proposed_quantities[-1] += 1
            # Loop breaks when we have one monster too many, so subtract one
            proposed_quantities[-1] -= 1

            # Append the new monsters to the encounter
            if proposed_quantities[-1] > 0:
                encounter_monster_crs = proposed_crs
                encounter_quantities = proposed_quantities
                # We want to avoid duplicating the random starter monster
                monster_index = 0
                while monster_index < len(challenge_rating)-1 and challenge_rating[monster_index].name in encounter_monsters:
                    monster_index += 1
                encounter_monsters.append(challenge_rating[monster_index].name)

        if lower_xp < main.cr_calc(encounter_monster_crs, encounter_quantities) < upper_xp:
            break

    # for i in range(len(encounter_quantities)):
    #    print(f"{encounter_quantities[i]}x {encounter_monsters[i]}")
    # print()

    encounter = []

    for i in range(len(encounter_monsters)):
        encounter.append((encounter_quantities[i], encounter_monsters[i]))

    return encounter


if __name__ == "__main__":
    generate({"party": [(4, 5)]})
