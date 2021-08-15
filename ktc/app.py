from flask import Flask, render_template, jsonify
try:
    import api  # type: ignore
except ModuleNotFoundError:
    from ktc import api  # type: ignore


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST', 'PUT'])
def home():
    return render_template("index.html")


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


if __name__ == "__main__":
    app.run(debug=True)
