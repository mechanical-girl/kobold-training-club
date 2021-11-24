# -*- coding: utf-8 -*-

"""The API module contains most of the important functions for KTC and wrappers for the rest"""

import contextlib
import sqlite3
from fractions import Fraction
from typing import Dict, List, Tuple

try:
    import converter  # type: ignore
    import main  # type: ignore
except ModuleNotFoundError:
    from ktc import main  # type: ignore
    from ktc import converter  # type: ignore

import os

path_to_database = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, "data/monsters.db")
)
db_location = path_to_database


def sort_sizes(size_list: List[str]) -> List[str]:
    """
    Given a list of sizes, sorts them by the size they describe

    Args:
        size_list (List[str]): Unordered list of sizes

    Returns:
        List[str]: Ordered list of sizes
    """
    to_return = []

    size_list = [size.lower() for size in size_list]

    if "tiny" in size_list:
        to_return.append("tiny")
    if "small" in size_list:
        to_return.append("small")
    if "medium" in size_list:
        to_return.append("medium")
    if "large" in size_list:
        to_return.append("large")
    if "huge" in size_list:
        to_return.append("huge")
    if "gargantuan" in size_list:
        to_return.append("gargantuan")

    to_return = [size.title() for size in to_return]
    return to_return


def get_list_of_environments() -> List[str]:
    """Returns a deduplicated list of environments from the monster table"""
    with contextlib.closing(sqlite3.connect(db_location)) as conn:
        cursor = conn.cursor()

        cursor.execute("""SELECT DISTINCT environment FROM monsters""")
        unique_environments = [item[0] for item in cursor.fetchall()]

    set_of_environments = set()
    for environment in unique_environments:
        for env in environment.split(","):
            set_of_environments.add(env.strip())

    environments = [env for env in list(
        set_of_environments) if env != ""]
    environments.sort()
    return environments


def get_list_of_sizes() -> List[str]:
    """Returns a unique list of monster sizes from the monster table"""
    with contextlib.closing(sqlite3.connect(db_location)) as conn:
        cursor = conn.cursor()

        cursor.execute("""SELECT DISTINCT size FROM monsters""")
        unique_types = [item[0] for item in cursor.fetchall()]

    size_list = sort_sizes(unique_types)
    return size_list


def get_list_of_monster_types() -> List[str]:
    """Returns a unique list of monster types from the monsters table"""
    with contextlib.closing(sqlite3.connect(db_location)) as conn:
        cursor = conn.cursor()

        cursor.execute("""SELECT DISTINCT type FROM monsters""")
        unique_types = [item[0] for item in cursor.fetchall()]

    unique_types.sort()
    return unique_types


def get_list_of_challenge_ratings() -> List[str]:
    """Returns a unique list of challenge ratings from the monsters table"""
    with contextlib.closing(sqlite3.connect(db_location)) as conn:
        cursor = conn.cursor()

        cursor.execute("""SELECT DISTINCT cr FROM monsters""")
        unique_crs = [item[0] for item in cursor.fetchall()]

    unique_crs.sort(key=Fraction)
    return unique_crs


def get_list_of_alignments() -> List[str]:
    """Returns a unique list of alignments from the monsters table"""
    with contextlib.closing(sqlite3.connect(db_location)) as conn:
        cursor = conn.cursor()

        cursor.execute("""SELECT DISTINCT alignment FROM monsters""")
        unique_alignments = [
            item[0].lower() for item in cursor.fetchall() if not " or " in item[0]
        ]

    unique_alignments = list(set(unique_alignments))
    unique_alignments.sort()

    return unique_alignments


# TODO: Rename to get_list_of_official_sources
def get_list_of_sources() -> List[str]:
    """
    Creates a deduplicated list of official sources

    Returns:
        List[str]: A list containing the names of all official source books in the DB
    """
    with contextlib.closing(sqlite3.connect(db_location)) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """SELECT DISTINCT name FROM sources WHERE official = 1 """)
        unique_sources = [item[0] for item in cursor.fetchall()]

    sources = list(unique_sources)
    sources.sort()
    return sources

# TODO Split paraneter sanitisation and query construction into separate functions


def get_list_of_monsters(parameters: Dict) -> Dict[str, List[List[str]]]:
    """Query the database for monsters matching the parameters passed and return a list

    Args:
        parameters (Dict): a dict of parameters, consisting of column names: [acceptable values]

    Returns:
        Dict[str, List[List[Any]]]: a dict where the value of "data" is the list of monster info
    """

    # Here we go through the parameters and split each into an individual variable
    # This improves readability and allows for the creation of empty lists if
    # no constraints are given
    try:
        environment_constraints = [
            param.split("_")[1] for param in parameters["environments"]
        ]
    except (KeyError, IndexError):
        environment_constraints = []

    try:
        size_constraints = [param.split("_")[1]
                            for param in parameters["sizes"]]
    except (KeyError, IndexError):
        size_constraints = []

    try:
        source_constraints = [param.split("_")[1]
                              for param in parameters["sources"]]
    except (KeyError, IndexError):
        source_constraints = get_list_of_sources()

    print(source_constraints)

    try:
        source_constraints += [param.split("_")[1]
                               for param in parameters["customSourcesUsed"]]
    except (KeyError, IndexError):
        pass

    try:
        type_constraints = [param.split("_")[1]
                            for param in parameters["types"]]
    except (KeyError, IndexError):
        type_constraints = []

    try:
        alignment_constraints = [
            param.split("_")[1] for param in parameters["alignments"]
        ]
    except (KeyError, IndexError):
        alignment_constraints = []

    try:
        challenge_rating_minimum = parameters["minimumChallengeRating"]
    except (KeyError, IndexError):
        challenge_rating_minimum = None
    try:
        challenge_rating_maximum = parameters["maximumChallengeRating"]
    except (KeyError, IndexError):
        challenge_rating_maximum = None

    try:
        if parameters["allowLegendary"] and parameters["allowLegendary"] == "false":
            allow_legendary = False
        else:
            allow_legendary = True
    except (KeyError, IndexError):
        allow_legendary = True

    try:
        if parameters["allowNamed"] and parameters["allowNamed"] == "false":
            allow_named = False
        else:
            allow_named = True
    except (KeyError, IndexError):
        allow_named = True

    # Oh, this is clumsy, I hate this
    where_requirements = ""
    query_arguments = []
    query_from = "monsters"
    # TODO: Refactor to store CRs as floats and convert to fractions
    possible_challenge_ratings = [
        "0",
        "1/8",
        "1/4",
        "1/2",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
    ]

    # SO
    # If we have size constraints, we construct a string of placeholders,
    # then put that into a IN subquery
    # and then append the constraints to the query_arguments list

    # Create a custom select with "environment like x or..." for every environment in constraints
    if environment_constraints != []:
        query_from = f"(SELECT * FROM {query_from} WHERE "
        for i, constraint in enumerate(environment_constraints):
            query_from += "environment LIKE ? OR "
            environment_constraints[i] = f"%{constraint}%"
        query_from = query_from[:-4]
        query_from += ")"
        query_arguments += environment_constraints

    # Create a custom select with "sourcehashes like x or", then get the source
    # hash for every specified source
    #
    # You need to do this because of wildcards surrounding the source name
    # Which makes me wonder if you need to be using those wildcards at all...
    if source_constraints != []:
        query_from = f"(SELECT * FROM {query_from} WHERE "
        constraint_hashes = []
        with contextlib.closing(sqlite3.connect(db_location, uri=True)) as conn:
            cursor = conn.cursor()
            for constraint in source_constraints:
                cursor.execute(
                    '''SELECT hash FROM sources WHERE name = ?''', (constraint,))
                constraint_hashes.append(f"%{cursor.fetchone()[0]}%")
                query_from += "sourcehashes LIKE ? OR "
        query_from = query_from[:-4]
        query_from += ")"
        query_arguments += constraint_hashes

    if alignment_constraints != []:
        query_from = f"(SELECT * FROM {query_from} WHERE "
        for i, constraint in enumerate(alignment_constraints):
            query_from += "alignment LIKE ? OR "
            alignment_constraints[i] = f"%{constraint}%"
        query_from = query_from[:-4]
        query_from += ")"
        query_arguments += alignment_constraints

    if size_constraints != []:
        size_query_placeholders = f"({', '.join(['?']*len(size_constraints))})"
        where_requirements += f"size IN {size_query_placeholders} AND "
        query_arguments += size_constraints

    if type_constraints != []:
        type_query_placeholders = f"({', '.join(['?']*len(type_constraints))})"
        where_requirements += f"type IN {type_query_placeholders} AND "
        query_arguments += type_constraints

    if challenge_rating_minimum is not None or challenge_rating_maximum is not None:
        if challenge_rating_minimum is None:
            min_cr = possible_challenge_ratings[0]
        else:
            min_cr = challenge_rating_minimum
        if challenge_rating_maximum is None:
            max_cr = possible_challenge_ratings[-1]
        else:
            max_cr = challenge_rating_maximum

        mindex = possible_challenge_ratings.index(min_cr)
        maxdex = possible_challenge_ratings.index(max_cr)+1
        no_of_placeholders = len(possible_challenge_ratings[mindex:maxdex])
        challenge_rating_placeholders = (
            f"({', '.join(['?']*no_of_placeholders)})"
        )
        where_requirements += f"cr IN {challenge_rating_placeholders} AND "
        query_arguments += possible_challenge_ratings[mindex:maxdex]

    if allow_legendary is not True:
        where_requirements += "legendary = 0 AND "

    if allow_named is not True:
        where_requirements += "named = 0 AND "

    # If there are requirements, we add a WHERE to the start
    if where_requirements != "":
        where_requirements = ("WHERE ") + where_requirements
    # Take of the trailing " and "
    if where_requirements.endswith(" AND "):
        where_requirements = where_requirements[:-5]

    cols = "name, cr, size, type, tags, section, alignment, sources, fid, hp, ac, init"
    query_string = f"""SELECT {cols} FROM {query_from} {where_requirements} ORDER BY name"""

    with contextlib.closing(sqlite3.connect(db_location)) as conn:
        cursor = conn.cursor()
        # conn.set_trace_callback(print)

        if query_arguments == []:
            cursor.execute(query_string)
        else:
            cursor.execute(query_string, (*query_arguments,))
        monster_list = cursor.fetchall()

    monster_data = []
    for monster in monster_list:
        modified_monster = list(monster)

        # convert sources with links to hrefs
        sources = monster[7].split(",")
        linked_sources = []
        for source in sources:
            (source_name, index) = converter.split_source_from_index(source)
            if "http" in index:
                linked_sources.append(
                    f"<a target='_blank' href='{index}''>{source_name}</a>")
            else:
                linked_sources.append(f"{source_name}: {index}")

        modified_monster[7] = ', '.join(linked_sources)

        # append modified monster data
        monster_data.append([str(prop).strip() for prop in modified_monster])

    return {"data": monster_data}


def get_party_thresholds(party: List[Tuple[int, int]]) -> List[int]:
    """
    Simply a wrapper around the main function

    Args:
        party (List[Tuple[int, int]]): A list of tuples [character quantity, character level]

    Returns:
        List[int]: [description]
    """
    return main.party_thresholds_calc(party)


def get_encounter_xp(monsters: List[Tuple[str, int]]) -> int:
    """
    Formats information for the cr_calc function and calls it

    Args:
        monsters (List[Tuple[str, int]]): A list of tuples [monster name, monster quantity]

    Returns:
        int: The total adjusted XP for this encounter
    """
    # TODO: refactor once corresponding main function is refactored

    crs = []
    quantities = []
    for monster_pair in monsters:
        (name, number) = monster_pair
        monster_cr = main.get_monster_cr(name)
        crs.append(monster_cr)
        quantities.append(int(number))

    adj_xp_total = main.cr_calc(crs, quantities)
    return adj_xp_total


def ingest_custom_csv_string(csv_string, db_location, url=""):
    """Simply a wrapper for the converter function"""
    return converter.ingest_data(csv_string, db_location, url)


def get_unofficial_sources() -> List[str]:
    """Returns a deduplicated list of unofficial sources

    Returns:
        List[str]: a deduplicated list of unofficial sources
    """
    with contextlib.closing(sqlite3.connect(db_location)) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """SELECT DISTINCT name FROM sources WHERE official = 0""")
        unique_sources = [item[0] for item in cursor.fetchall()]

    set_of_sources = set()
    for source_set in unique_sources:
        sources = source_set.split(",")
        for source in sources:
            set_of_sources.add(source.split(":")[0].strip())

    sources = [source for source in list(set_of_sources) if source != ""]
    sources.sort()
    return sources


def check_if_key_processed(key):
    """Simply a wrapper for the converter function"""
    return converter.check_if_key_processed(key)
