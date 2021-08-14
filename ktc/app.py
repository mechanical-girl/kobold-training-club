from flask import Flask, render_template, jsonify
from api import get_list_of_environments

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST', 'PUT'])
def home():
    return render_template("index.html")


@app.route("/api/environments", methods=["GET"])
def get_environments():
    return jsonify(api_get_list_of_environments())


app.run(debug=True)
