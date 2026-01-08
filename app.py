from flask import Flask, redirect, render_template,request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from db import db, User 
import os
from flask import session
from forms import LoginForm, RegisterForm
from flask import flash

def login_required():
    if 'user_id' not in session:
        return False
    return True

app = Flask(__name__)
#session
app.secret_key = "super-secret-key"
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
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data
        ).first()

        if not user:
            flash("Benutzername existiert nicht", "danger")
            return render_template("login.html", form=form)

        if not check_password_hash(
            user.password_hash,
            form.password.data
        ):
            flash("Falsches Passwort", "danger")
            return render_template("login.html", form=form)

        session['user_id'] = user.user_id
        flash("Erfolgreich eingeloggt", "success")
        return redirect(url_for("create_or_join_wg"))
    

    return render_template("login.html", form=form)
    
@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        if User.query.filter_by(username=form.username.data).first():
            return "Benutzername existiert bereits", 400
        
        if User.query.filter_by(email=form.email.data).first():
            return "Email existiert bereits", 400

        #Passwort hashen und User erstellen
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role='member' 
        )

        db.session.add(new_user)
        db.session.commit()

        #Session setzen -> direkt eingeloggt
        session['user_id'] =new_user.user_id
        return redirect(url_for('create_or_join_wg'))
    return render_template("register.html", form=form)


@app.route("/welcome/", methods=['GET', 'POST'])
def create_or_join_wg():
    if request.method == 'POST':
       
        return redirect(url_for("create_wg"))
   # if 'user_id' not in session:
    #    return redirect(url_for('login'))

    return render_template("welcome.html")

@app.route("/welcome/create_wg/", methods=['GET', 'POST'])
def create_wg():
    if request.method == 'POST':
        print("WG erstellt")
        return redirect(url_for("create_or_join_wg"))
    # if 'user_id' not in session:
    #    return redirect(url_for('login'))
    return render_template("create_wg.html")

@app.route("/welcome/join_wg/", methods=['GET', 'POST'])
def join_wg():
    if request.method == 'POST':
        print("WG beigetreten")
        return redirect(url_for("dashboard"))
    # if 'user_id' not in session:
    #    return redirect(url_for('login'))

    return render_template("join_wg.html")

@app.route("/dashboard/", methods=['GET'])
def dashboard():
    if request.method == 'GET':
        return redirect(url_for("dashboard"))
    # if 'user_id' not in session:
    #    return redirect(url_for('login'))
    return render_template("dashboard.html")

@app.route("/putzplan/", methods=['GET'])
def putzplan():
    if request.method == 'GET':
        return redirect(url_for("putzplan"))
    # if 'user_id' not in session:
    #    return redirect(url_for('login'))
    return render_template("putzplan.html")

@app.route("/create_cleaning_object/", methods=['GET'])
def create_cleaning_object():
    if request.method == 'GET':
        return redirect(url_for("create_cleaning_object"))
    # if 'user_id' not in session:
    #    return redirect(url_for('login'))
    return render_template("create_cleaning_object.html")


@app.route("/innovationboard/", methods=['GET'])
def innovation_board():
    if request.method == 'GET':
        return redirect(url_for("innovation_board"))
    # if 'user_id' not in session:
    #    return redirect(url_for('login'))
    return render_template("innovationboard.html")

@app.route("/new_innovation/", methods=['GET', 'POST'])
def create_innovation():
    if request.method == 'POST':
        print("Innovation erstellt")
    # if 'user_id' not in session:
    #    return redirect(url_for('login'))
        return redirect(url_for("innovation_board"))

    print("Das ist später die neue Innovation erstellen Seite")
    return render_template("create_inno.html")

@app.route("/activityboard/", methods=['GET'])
def activity_board():
    if request.method == 'GET':
        return redirect(url_for("activity_board"))
    # if 'user_id' not in session:
    #    return redirect(url_for('login'))
    return render_template("activityboard.html")

@app.route("/new_activity/", methods=['GET', 'POST'])
def create_activity():
    if request.method == 'POST':
        print("Aktivität erstellt")
        return redirect(url_for("activityboard"))
    print("Das ist später die neue Aktivitäten Seite")
    # if 'user_id' not in session:
    #    return redirect(url_for('login'))
    return render_template("create_activity.html")


@app.route("/einkaufsplan/", methods = ["GET", "POST"])
def einkaufsplan():
    if request.method == 'GET':
        return redirect(url_for("einkaufsplan"))
    # if 'user_id' not in session:
    #    return redirect(url_for('login'))
    return render_template("einkaufsplan.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # erstellt alle Tabellen in der Datenbank
    app.run(debug=True)

