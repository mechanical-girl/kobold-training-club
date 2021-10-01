# -*- coding: utf-8 -*-
import json
import os

from flask import Flask, jsonify, render_template, request

try:
    import api  # type: ignore
    import converter  # type: ignore
except ModuleNotFoundError:
    from ktc import api  # type: ignore
    from ktc import converter  # type: ignore

version = "v0.4.0"

app = Flask(__name__)
path_to_database = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir, "data/monsters.db"))

db_location = path_to_database


@app.route("/", methods=["GET", "POST", "PUT"])
def home():
    return render_template("index.html", version=version)


@app.route("/index.html", methods=["GET", "POST", "PUT"])
def index():
    return render_template("index.html", version=version)


@app.route("/about.html", methods=["GET", "POST", "PUT"])
def about_page():
    return render_template("about.html")


@app.route("/api/environments", methods=["GET"])
def get_environments():
    return jsonify(api.get_list_of_environments())


@app.route("/api/sizes", methods=["GET"])
def get_sizes():
    return jsonify(api.get_list_of_sizes())


@app.route("/api/crs", methods=["GET"])
def get_crs():
    return jsonify(api.get_list_of_challenge_ratings())


@app.route("/api/sources", methods=["GET"])
def get_sources():
    return jsonify(api.get_list_of_sources())


@app.route("/api/types", methods=["GET"])
def get_types():
    return jsonify(api.get_list_of_monster_types())


@app.route("/api/alignments", methods=["GET"])
def get_alignments():
    return jsonify(api.get_list_of_alignments())


@app.route("/api/monsters", methods=["GET", "POST"])
def get_monsters():
    try:
        monster_parameters_string = request.values["params"]
        monster_parameters = json.loads(
            monster_parameters_string)
    except:
        monster_parameters = {}
    return jsonify(api.get_list_of_monsters(monster_parameters))


@app.route("/api/expthresholds", methods=["GET", "POST"])
def get_exp_thresholds():
    party = json.loads(request.values["party"])
    return jsonify(api.get_party_thresholds(party))


@app.route("/api/encounterxp", methods=["GET", "POST"])
def get_encounter_xp():
    monsters = json.loads(request.values["monsters"])
    return jsonify(api.get_encounter_xp(monsters))


@app.route("/api/unofficialsources", methods=["GET"])
def get_unofficial_sources():
    return jsonify(api.get_unofficial_sources())


@app.route("/api/processCSV", methods=["GET", "POST"])
def process_csv():
    csv_string = json.loads(request.values["csv"])
    key = json.loads(request.values["key"])
    source_name = api.ingest_custom_csv_string(csv_string, db_location, key)
    return jsonify({"name": source_name})


@app.route("/api/checksource", methods=["GET", "POST"])
def check_if_key_processed():
    key = json.loads(request.values["key"])
    result = api.check_if_key_processed(key)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
