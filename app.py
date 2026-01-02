from os import name
from flask import Flask, flash, redirect, render_template,request, url_for

from db import CleaningTemplate,db, User
from docs.forms import PutzplanForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'HappyWG_Project_SecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///happywg.sqlite'

db.init_app(app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

@app.cli.command()
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        print("Database initialized!")

@app.cli.command()
def create_test_user():
    """Create initial users."""
    with app.app_context():
        existing_user = User.query.filter_by(username='testuser').first()
        if existing_user:
            print("Test user already exists.")
            return
    test_user = User(username='testuser', password_hash='hashedpassword',
                     email='testuser@example.com', role='member')
    db.session.add(test_user)
    db.session.commit()
    print("Test user created.")

@app.route('/', methods=['GET', 'POST'])

def index():

    if request.method == 'POST':
        return "This is a POST request"
    return "Hello, World! Get Request Received"
    
@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("Benutzer eingeloggt")
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

@app.route("/dashboard/", methods=['GET', 'POST'])
def dashboard():
    
    return render_template("dashboard.html")

@app.route("/putzplan/", methods=['GET', 'POST'])
def putzplan():
    form = PutzplanForm()
    all_users = User.query.all()
    for user in all_users:
        print(f"Benutzer: {user.username}")
    if form.validate_on_submit():
        new_eintrag = CleaningTemplate(
            wg_id=1,  # Get from session/logged-in user
            name=form.aufgabe.data,
            description=f"Week {form.woche.data}: {form.von_datum.data} to {form.bis_datum.data}",
            frequency="weekly"
        )
        db.session.add(new_eintrag)
        db.session.commit()

        flash('Eintrag erfolgreich erstellt!', 'success')
        return redirect(url_for("putzplan"))
    elif form.is_submitted():
        # Form submitted but validation failed
        if form.zustaendig.errors:
            flash('WG-Mitglied existiert nicht', 'error')
    putzplan_eintraege = CleaningTemplate.query.all()
    return render_template("putzplan.html", form=form, putzplan=putzplan_eintraege, all_users=all_users)


@app.route("/innovationboard/", methods=['GET'])
def innovation_board():
    return render_template("innovationboard.html")

@app.route("/activityboard/", methods=['GET'])
def activity_board():
    return render_template("activityboard.html")

@app.route("/einkaufsplan/", methods=["GET", "POST"])
def einkaufsplan():
    if request.method == 'POST':
        
        pass
    return render_template("einkaufsplan.html")


