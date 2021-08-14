from flask import Flask, render_template, jsonify
from ktc.api import get_list_of_environments  # type: ignore

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST', 'PUT'])
def home():
    return render_template("index.html")


@app.route("/api/environments", methods=["GET"])
def get_environments():
    return jsonify(get_list_of_environments())


if __name__ == "__main__":
    app.run(debug=True)
