from os import name
from sqlite3 import IntegrityError
from flask import Flask, flash, redirect, render_template,request, url_for,session
from sqlalchemy.orm import joinedload

from db import CleaningTask, CleaningTemplate, Idea, Idea_Comment, Idea_Like,db, User
from docs.forms import CommentForm, InnovationForm, PutzplanForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'HappyWG_Project_SecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///happywg.sqlite'

db.init_app(app)

#session["user_id"] = user.user_id
#session["wg_id"] = user.wg_id  

def current_user():
    uid = session.get("user_id")
    return User.query.get(uid) if uid else None


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



@app.route("/putzplan/", methods=["GET", "POST"])
def putzplan():

    form = PutzplanForm()

    #user_id = session.get("user_id")
    #if not user_id:
     #   flash("Bitte zuerst einloggen.", "error")
      #  return redirect(url_for("login"))

    #user = User.query.get(user_id)  
    #user = current_user()
    #if not user:
     #   flash("Bitte zuerst einloggen.", "error")
        #   return redirect(url_for("login"))
    
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
                wg_id=1, #wg_id = user.wg_id
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
                          .filter_by(wg_id=1, is_active=True) #wg_id = user.wg_id
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


@app.route("/innovationboard/", methods=['GET', 'POST'])
def innovation_board():
    form = InnovationForm()

    #user_id = session.get("user_id")
    #if not user_id:
     #   flash("Bitte zuerst einloggen.", "error")
      #  return redirect(url_for("login"))

    #user = User.query.get(user_id)  

    all_users = User.query.all()

    if request.method == 'POST':
        print("Innovation eingereicht")
        print("form.validate_on_submit():", form.validate_on_submit())
        print("form.errors:", form.errors)


        if form.validate_on_submit():
                flash("Innovation erfolgreich eingereicht!", "success")
                
                user = User.query.filter_by(username="testuser").first() #To be replaced with current_user() or session user
                new_idea = Idea(
                    wg_id=1, #wg_id = user.wg_id
                    created_by=user.user_id,
                    title=form.title.data,
                    description=form.description.data,
                    created_at=db.func.now()
                )
                db.session.add(new_idea)
                db.session.commit()

                return redirect(url_for("innovation_board"))
        else:
            flash("Fehler beim Einreichen der Innovation. Bitte überprüfen Sie die Eingaben.", "error")

    ideas = (Idea.query
             .filter_by(wg_id=1)   #wg_id = user.wg_id
             .options(joinedload(Idea.creator))
             .order_by(Idea.created_at.desc())
             .all())
    #ideas = Idea.query.filter_by(wg_id=user.wg_id).order_by(Idea.created_at.desc()).all()
    return render_template("innovationboard.html", form=form, all_users=all_users,ideas=ideas)

@app.route("/innovation_board/idea/<int:idea_id>/delete", methods=["POST"])
def delete_idea(idea_id):
    #current_user_id = session.get("user_id")
    #if idea.creator.user_id != current_user_id:
     #   flash("Sie können nur Ihre eigenen Ideen löschen.", "error")
        #abort(403)

    idea = Idea.query.get_or_404(idea_id)
    db.session.delete(idea)
    db.session.commit()
    flash("Idee erfolgreich gelöscht.", "success")
    return redirect(url_for("innovation_board"))

@app.route("/ideas/<int:idea_id>/like", methods=["POST"])
def toggle_like(idea_id):
    #user_id = session.get("user_id")
    #if not user_id:
        #flash("Bitte zuerst einloggen.", "error")
        #return redirect(url_for("login"))

    existing = Idea_Like.query.filter_by(idea_id=idea_id, user_id="testuser").first() #To be replaced with idea_id=idea_id, user_id=user_id

    if existing:
        db.session.delete(existing)   # unlike
    else:
        db.session.add(Idea_Like(idea_id=idea_id, user_id="testuser"))  # like

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

    return redirect(url_for("innovation_board"))

@app.route("/ideas/<int:idea_id>/comment", methods=["POST"])
def post_comment(idea_id):

    form = CommentForm()
    #user_id = session.get("user_id")
    #if not user_id:
        #flash("Bitte zuerst einloggen.", "error")
        #return redirect(url_for("login"))

    content = request.form.get("content", "").strip()
    if content:
        new_comment = Idea_Comment(
            idea_id=idea_id,
            user_id="testuser",  #To be replaced with user_id=user_id
            content=content,
            created_at=db.func.now()
        )
        db.session.add(new_comment)
        db.session.commit()
        flash("Kommentar hinzugefügt.", "success")
    else:
        flash("Kommentar darf nicht leer sein.", "error")

    return redirect(url_for("innovation_board"), anchor=f"idea-{idea_id}",form=form)

@app.route("/activityboard/", methods=['GET'])
def activity_board():
    return render_template("activityboard.html")

@app.route("/einkaufsplan/", methods=["GET", "POST"])
def einkaufsplan():
    if request.method == 'POST':
        
        pass
    return render_template("einkaufsplan.html")


