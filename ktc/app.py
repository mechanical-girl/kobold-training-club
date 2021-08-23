# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename

try:
    import api  # type: ignore
except ModuleNotFoundError:
    from ktc import api  # type: ignore

UPLOAD_FOLDER = 'ktc/uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


path_to_database = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir, "data/monsters.db"))

db_location = path_to_database


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@ app.route("/", methods=["GET", "POST", "PUT"])
def home():
    return render_template("index.html")


@ app.route("/index.html", methods=["GET", "POST", "PUT"])
def index():
    return render_template("index.html")


@ app.route("/about.html", methods=["GET", "POST", "PUT"])
def about_page():
    return render_template("about.html")


@ app.route("/api/environments", methods=["GET"])
def get_environments():
    return jsonify(api.get_list_of_environments())


@ app.route("/api/sizes", methods=["GET"])
def get_sizes():
    return jsonify(api.get_list_of_sizes())


@ app.route("/api/crs", methods=["GET"])
def get_crs():
    return jsonify(api.get_list_of_challenge_ratings())


@ app.route("/api/sources", methods=["GET"])
def get_sources():
    return jsonify(api.get_list_of_sources())


@ app.route("/api/types", methods=["GET"])
def get_types():
    return jsonify(api.get_list_of_monster_types())


@ app.route("/api/alignments", methods=["GET"])
def get_alignments():
    return jsonify(api.get_list_of_alignments())


@ app.route("/api/monsters", methods=["GET", "POST"])
def get_monsters():
    try:
        monster_parameters_string = request.values["params"]
        print(monster_parameters_string)
        monster_parameters = json.loads(
            monster_parameters_string.replace("'", '"'))
    except:
        monster_parameters = {}
    return jsonify(api.get_list_of_monsters(monster_parameters))


@ app.route("/api/expthresholds", methods=["GET", "POST"])
def get_exp_thresholds():
    party = json.loads(request.values["party"])
    return jsonify(api.get_party_thresholds(party))


@ app.route("/api/encounterxp", methods=["GET", "POST"])
def get_encounter_xp():
    monsters = json.loads(request.values["monsters"])
    return jsonify(api.get_encounter_xp(monsters))


@ app.route("/api/processCSV", methods=["GET", "POST"])
def process_csv():
    csv_string = json.loads(request.values["csv"])
    key = json.loads(request.values["key"])
    source_name = api.ingest_custom_csv_string(csv_string, db_location, key)
    return jsonify({"name": source_name})


@ app.route("/api/unofficialsources", methods=["GET"])
def get_unofficial_sources():
    return jsonify(api.get_unofficial_sources())


@ app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("/")
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == "__main__":
    app.run(debug=True)
