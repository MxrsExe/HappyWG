from flask import Flask, render_template,request

import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():

    if request.method == 'POST':
        return "This is a POST request"
    return "Hello, World! Get Request Received"
    

@app.route("/lists/")
def lists():
    return render_template("list.html", list = list) 

@app.route("/lists/<int:id>")
def list(id):
    return f"Todo: This is the lists page for a list with id {id}."



