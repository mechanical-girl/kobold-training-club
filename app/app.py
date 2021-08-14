from flask import Flask

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST', 'PUT'])
def home():
    return "Hello, world"


app.run(debug=True)
