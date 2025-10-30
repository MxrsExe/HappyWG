from flask import Flask

app = Flask(__name__)

@app.route('/')

def index():
    return "Hello, World!"

@app.route("/lists/")
def lists():
    return "Todo: This is the lists page."

@app.route("/lists/<int:id>")
def list(id):
    return f"Todo: This is the lists page for a list with id {id}."



