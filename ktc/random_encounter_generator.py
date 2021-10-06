# -*- coding: utf-8 -*-
import random
from fractions import Fraction

try:
    import api  # type: ignore
    import main  # type: ignore
except ModuleNotFoundError:
    from ktc import api  # type: ignore
    from ktc import main  # type: ignore


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

    monster_rarity += taldorei_type_rarity_modifiers[monster[3].lower()]
    if monster_rarity > 3:
        monster_rarity = 3

    if rarities[monster_rarity] in encounter_rarity:
        return True
    return False


def randomise(monsters):
    random_monsters = []
    crs = [monster[1] for monster in monsters]
    crs = list(set(crs))
    crs.sort(key=lambda x: float(Fraction(x)))
    for cr in crs[::-1]:
        cr_monsters = [monster for monster in monsters if monster[1] == cr]
        random.shuffle(cr_monsters)
        random_monsters += cr_monsters

    return random_monsters


rarities = ["common", "uncommon", "rare", "very rare"]
rarity_thresholds = [7, 15, 22]

taldorei_type_rarity_modifiers = {"aberration": 1, "beast": 0, "celestial": 2, "construct": 1, "dragon": 1, "elemental": 1,
                                  "fey": 1, "fiend": 2, "giant": +1, "humanoid": 0, "monstrosity": 1, "ooze": 1, "plant": 1, "undead": 0}

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

# select all creatures in environment, filter to only those matching rarity
possible_monsters = api.get_list_of_monsters(
    {"environments": ["_forest", "_mountain", "_no environment specified"],
     "sources": ['_Basic Rules v1',
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
                 '_Waterdeep: Dungeon of the Mad Mage'], })["data"]

monsters = [monster for monster in possible_monsters if fits_rarity(
    monster, encounter_rarity)]
random.shuffle(monsters)
# Sort by difficulty ascending
monsters.sort(key=lambda x: float(Fraction(x[1])))
monsters = monsters[::-1]  # Sort by difficulty descending
monsters = randomise(monsters)

# add creatures by descending CR until desired encounter difficulty is reached
party = [(5, 11)]
thresholds = main.party_thresholds_calc(party)
upper_xp = thresholds[3]
lower_xp = thresholds[2]


# Add a beginning monster
while True:
    monster = random.choice(monsters)
    quantity = random.randint(1, 3)
    if main.cr_calc([monster[1]], [quantity]) < upper_xp:
        encounter_monsters = [monster[0]]
        encounter_quantities = [quantity]
        encounter_monster_crs = [monster[1]]
        break

encounter_xp = 0
for monster in monsters:
    if upper_xp > main.cr_calc(encounter_monster_crs+[monster[1]], encounter_quantities + [1]):
        if monster[0] in encounter_monsters:
            encounter_quantities[encounter_monsters.index(monster[0])] += 1
        else:
            encounter_monsters.append(monster[0])
            encounter_monster_crs.append(monster[1])
            encounter_quantities.append(1)
        if main.cr_calc(encounter_monster_crs, encounter_quantities) > lower_xp:
            break
        continue


print(encounter_monsters)
print(encounter_quantities)
