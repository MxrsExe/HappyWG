from flask import Flask, render_template,request

import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():

    if request.method == 'POST':
        return "This is a POST request"
    return "Hello, World! Get Request Received"
    
@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/welcome/")
def create_or_join_wg():
    return render_template("welcome.html")

@app.route("/welcome/create_wg/")
def create_wg():
    return render_template("create_wg.html")

@app.route("/welcome/join_wg/")
def join_wg():
    return render_template("join_wg.html")

@app.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/putzplan/")
def putzplan():
    return render_template("putzplan.html")

@app.route("/innovationboard/")
def innovationboard():
    return render_template("innovationboard.html")

@app.route("/activtyboard/")
def activityboard():
    return render_template("activityboard.html")

@app.route("/einkaufsliste/")
def einkaufsliste():
    return render_template("einkaufsliste.html")


