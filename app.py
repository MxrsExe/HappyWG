from flask import Flask, redirect, render_template,request, url_for
from werkzeug.security import check_password_hash
from db import db, User 
import os

app = Flask(__name__)
#Flask bekommt DB-Zugriff
app.config['SECRET_KEY'] = 'HappyWG_Project_SecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///happywg.sqlite'

db.init_app(app)

@app.route('/', methods=['GET', 'POST'])

def index():

    if request.method == 'POST':
        return "This is a POST request"
    return "Hello, World! Get Request Received"

 #login-Funktion   
@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')

        if not username or not password:
            return "Bitte Benutzername und Passwort eingeben", 400
        
        user = User.query.filter_by(username=username).first()

        if not user:
            return "Benutzer nicht gefunden", 401

        if not check_password_hash(user.password_hash, password):
            return "Falsches Passwort", 401

        print(f"User {username} erfolgreich eingeloggt")
        return redirect(url_for("create_or_join_wg"))

    return render_template("login.html")
    

@app.route("/welcome/", methods=['GET', 'POST'])
def create_or_join_wg():
    if request.method == 'POST':
       
        return redirect(url_for("create_wg"))
    return render_template("welcome.html")

@app.route("/welcome/create_wg/", methods=['GET', 'POST'])
def create_wg():
    if request.method == 'POST':
        print("WG erstellt")
        return redirect(url_for("create_or_join_wg"))
    return render_template("create_wg.html")

@app.route("/welcome/join_wg/", methods=['GET', 'POST'])
def join_wg():
    if request.method == 'POST':
        print("WG beigetreten")
        return redirect(url_for("dashboard"))
    return render_template("join_wg.html")

@app.route("/dashboard/", methods=['GET'])
def dashboard():
    if request.method == 'GET':
        return redirect(url_for("dashboard"))
    return render_template("dashboard.html")

@app.route("/putzplan/", methods=['GET'])
def putzplan():
    if request.method == 'GET':
        return redirect(url_for("putzplan"))
    return render_template("putzplan.html")

@app.route("/create_cleaning_object/", methods=['GET'])
def create_cleaning_object():
    if request.method == 'GET':
        return redirect(url_for("create_cleaning_object"))
    return render_template("create_cleaning_object.html")


@app.route("/innovationboard/", methods=['GET'])
def innovation_board():
    if request.method == 'GET':
        return redirect(url_for("innovation_board"))
    return render_template("innovationboard.html")

@app.route("/new_innovation/", methods=['GET', 'POST'])
def create_innovation():
    if request.method == 'POST':
        print("Innovation erstellt")
        return redirect(url_for("innovation_board"))

    print("Das ist später die neue Innovation erstellen Seite")
    return render_template("create_inno.html")

@app.route("/activityboard/", methods=['GET'])
def activity_board():
    if request.method == 'GET':
        return redirect(url_for("activity_board"))
    return render_template("activityboard.html")

@app.route("/new_activity/", methods=['GET', 'POST'])
def create_activity():
    if request.method == 'POST':
        print("Aktivität erstellt")
        return redirect(url_for("activityboard"))
    print("Das ist später die neue Aktivitäten Seite")
    return render_template("create_activity.html")


@app.route("/einkaufsplan/", methods = ["GET", "POST"])
def einkaufsplan():
    if request.method == 'GET':
        return redirect(url_for("einkaufsplan"))
    return render_template("einkaufsplan.html")


