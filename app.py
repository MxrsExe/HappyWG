from flask import Flask, render_template
import db
import os

app = Flask(__name__)

@app.route('/')

def index():
    return "Hello, World!"

@app.route("/lists/")
def lists():
    return render_template("list.html", list = list) 

@app.route("/lists/<int:id>")
def list(id):
    return f"Todo: This is the lists page for a list with id {id}."


