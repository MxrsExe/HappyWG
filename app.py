from flask import Flask, redirect, render_template,request, url_for

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
    print("Das ist später Join WG")
    return render_template("join_wg.html")

@app.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/putzplan/")
def putzplan():
    print("Das ist später der Putzplan")
    return render_template("putzplan.html")


@app.route("/innovationboard/")
def innovation_board():
    return render_template("innovationboard.html")

@app.route("/new_innovation/", methods=['GET', 'POST'])
def create_innovation():
    if request.method == 'POST':
        print("Innovation erstellt")
        return redirect(url_for("innovation_board"))

    print("Das ist später die neue Innovation erstellen Seite")
    return render_template("create_inno.html")

@app.route("/activityboard/")
def activity_board():
    print("Das ist später das Activity Board")
    return render_template("activityboard.html")

@app.route("/new_activity/", methods=['GET', 'POST'])
def create_activity():
    if request.method == 'POST':
        print("Aktivität erstellt")
        return redirect(url_for("activityboard"))
    print("Das ist später die neue Aktivitäten Seite")
    return render_template("create_activity.html")


@app.route("/einkaufsplan/")
def einkaufsplan():
    print("Das ist später der Einkaufsplan")
    return render_template("einkaufsplan.html")


