from os import name
from flask import Flask, flash, redirect, render_template,request, url_for

from db import CleaningTask, CleaningTemplate,db, User
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

from flask import request, redirect, url_for, flash, render_template

from flask import request, redirect, url_for, flash, render_template

@app.route("/putzplan/", methods=["GET", "POST"])
def putzplan():

    form = PutzplanForm()
    
    if request.method == "POST":
        print("POST angekommen")
        print("form.validate_on_submit():", form.validate_on_submit())
        print("form.errors:", form.errors)
        print("zustaendig raw:", request.form.get("zustaendig"))

    
    all_users = User.query.all()

    if form.validate_on_submit():
        zustaendig_name = request.form.get("zustaendig", "").strip()
        user = User.query.filter_by(username=zustaendig_name).first()

        if not user:
            flash("WG-Mitglied existiert nicht", "error")
        else:
            new_template = CleaningTemplate(
                wg_id=1,
                name=form.aufgabe.data,
                description=f"KW {form.woche.data}: {form.von_datum.data} bis {form.bis_datum.data}",
                frequency="weekly",
                is_active=True
            )
            db.session.add(new_template)
            db.session.flush()  # template_id ist jetzt da

            new_task = CleaningTask(
                template_id=new_template.template_id,
                assigned_to=user.user_id,
                status="open",
                notes="Zuständig"
            )
            db.session.add(new_task)

            db.session.commit()
            flash("Eintrag erfolgreich erstellt!", "success")
            return redirect(url_for("putzplan"))

    putzplan_eintraege = (CleaningTemplate.query
                          .filter_by(wg_id=1, is_active=True)
                          .order_by(CleaningTemplate.template_id.desc())
                          .all())
    
    tasks = (CleaningTask.query
         .join(CleaningTemplate)
         .filter(CleaningTemplate.wg_id == 1)
         .all())
    
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.status == "completed")
    progress = int((completed_tasks / total_tasks) * 100) if total_tasks else 0

    return render_template("putzplan.html", form=form, putzplan=putzplan_eintraege, all_users=all_users,
                           total_tasks=total_tasks, completed_tasks=completed_tasks, progress=progress)

@app.route("/putzplan/task/<int:task_id>/toggle", methods=["POST"])
def toggle_cleaning_task(task_id):
    task = CleaningTask.query.get_or_404(task_id)
    task.status = "completed" if request.form.get("done") == "on" else "open"
    db.session.commit()
    return redirect(url_for("putzplan"))


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


