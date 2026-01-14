from os import name
from random import random
from sqlite3 import IntegrityError
from flask import Flask, flash, redirect, render_template,request, url_for,session, Response
from datetime import timezone
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.orm import joinedload
import random
#from flask_mail import Mail, Message
from datetime import datetime
from datetime import timezone


from db import Activity, CleaningTask, CleaningTemplate, Idea, Idea_Comment, Idea_Like, ShoppingItem,db, User, Wg
from werkzeug.security import check_password_hash, generate_password_hash

from docs.forms import ActivityForm, CommentForm, EinkaufsplanForm, InnovationForm, PutzplanForm, RegisterForm, LoginForm

def generate_unique_code(length=6):
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

        if not Wg.query.filter_by(invite_code=code).first():
            return code
    
def login_required():
    if 'user_id' not in session:
        return False
    return True

app = Flask(__name__)
#session
app.secret_key = "super-secret-key"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HappyWG_Project_SecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///happywg.sqlite'

db.init_app(app)
migrate = Migrate(app, db)   #brauch man um neue Spalten zu erstellten Tabellen hinzuzufügen

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

def generate_unique_code(length=6):
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

        if not Wg.query.filter_by(invite_code=code).first():
            return code
    
def login_required():
    if 'user_id' not in session:
        return False
    return True
    
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
        flash("Erfolgreich eingeloggt!", "success")
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
            flash("Benutzername existiert bereits", "danger")
            return render_template("register.html", form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash("Email existiert bereits", "danger")
            return render_template("register.html", form=form)

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
        flash("Registrierung erfolgreich! Willkommen!", "success")
        return redirect(url_for('create_or_join_wg'))

    return render_template("register.html", form=form)


@app.route("/welcome/", methods=['GET', 'POST'])
def create_or_join_wg():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])

    return render_template("welcome.html", username=user.username)


@app.route("/welcome/create_wg/", methods=['GET', 'POST'])
def create_wg():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        wg_name = request.form.get("wg_name").strip()
    
        if not wg_name:
            flash("Bitte einen WG-Namen eingeben", "danger")
            return redirect(url_for("create_wg"))

        invite_code = generate_unique_code()

        new_wg = Wg(name=wg_name, invite_code=invite_code)

        db.session.add(new_wg)
        db.session.commit()

        flash(f"WG '{wg_name}' erstellt! Dein Einladungscode: {invite_code}", "success")
        return redirect(url_for("join_wg"))
    
    return render_template("create_wg.html")

@app.route("/welcome/join_wg/", methods=['GET', 'POST'])
def join_wg():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        invite_code = request.form.get('invite_code', '').strip().upper()

        if not invite_code:
            flash("Bitte gib einen Einladungscode ein.", "danger")
            return redirect(url_for('join_wg'))

        wg = Wg.query.filter_by(invite_code=invite_code).first()
        if not wg:
            flash("Ungültiger Einladungscode.", "danger")
            return redirect(url_for('join_wg'))

        user = User.query.get(session['user_id'])
        user.wg_id = wg.wg_id
        db.session.commit()  

        flash(f"Du bist der WG '{wg.name}' erfolgreich beigetreten!", "success")
        return redirect(url_for('dashboard'))

    return render_template("join_wg.html")

@app.route("/dashboard/", methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user or not user.wg_id:
        return redirect(url_for('create_or_join_wg'))

    wg = Wg.query.get(user.wg_id)



    offene_putzaufgaben_count = CleaningTask.query.filter_by(assigned_to=user.user_id, status='offen').count()
    neue_ideen_count = Idea.query.filter_by(wg_id=wg.wg_id).count()
    kommende_events = Activity.query.filter(Activity.wg_id==wg.wg_id, Activity.date >= datetime.now()).count()
    einkauf_count = ShoppingItem.query.filter_by(wg_id=wg.wg_id, assigned_to=None).count()

    counting_boxes = {
        'putzaufgaben': max(offene_putzaufgaben_count, 0),
        'ideen': max(neue_ideen_count, 0),
        'events': max(kommende_events, 0),
        'einkauf': max(einkauf_count, 0)
    }
    #Hinweis-Box
    wichtige_hinweise = []

    putz_tasks = CleaningTask.query.filter_by(assigned_to=user.user_id, status="offen").all()
    if putz_tasks:
        wichtige_hinweise += [f"Denk noch an deine Putzaufgabe: {t.template.name}"for t in putz_tasks]

    offene_einkaufs_items = ShoppingItem.query.filter_by(wg_id=wg.wg_id, assigned_to=None).all()
    if offene_einkaufs_items:
        wichtige_hinweise += ["Folgende Einkaufsitems müssen noch besorgt werden:"]
        for item in offene_einkaufs_items:
            wichtige_hinweise.append(f"-{item.name}")

    kommende_events_list = Activity.query.filter(Activity.wg_id==wg.wg_id, Activity.date >= datetime.now()).order_by(Activity.date.asc()).limit(5).all()
    if kommende_events_list:
        wichtige_hinweise += [f"Kommendes Event: {e.title} am {e.date.strftime('%d.%m.%Y')}" for e in kommende_events_list] 

    if not wichtige_hinweise:
        wichtige_hinweise = ["Momentan gitbt es keine offenen Aufgaben oder Hinweise!"]

    #Activity-Box
    letzte_aktivitaeten = []

    erledigte_putzaufgaben = CleaningTask.query.filter_by(assigned_to=user.user_id, status="erledigt").order_by(CleaningTask.completed_at.desc()).limit(10).all()
    letzte_aktivitaeten += [f"{t.user.username} hat {t.template.name} geputzt" for t in erledigte_putzaufgaben]

    neue_einkaufs_items = ShoppingItem.query.filter(ShoppingItem.wg_id == wg.wg_id,).order_by(ShoppingItem.item_id.desc()).limit(10).all()
    letzte_aktivitaeten += [f"{i.added_by_user.username} hat '{i.name}' zur Einkaufsliste hinzugefügt" for i in neue_einkaufs_items]

    letzte_ideen = Idea.query.filter_by(wg_id=wg.wg_id).order_by(Idea.created_at.desc()).limit(10).all()
    letzte_aktivitaeten += [f"{i.creator.username} hat eine Idee hinzugefügt: '{i.title}'" for i in letzte_ideen]

    kommende_events_list = Activity.query.filter(Activity.wg_id == wg.wg_id, Activity.date >= datetime.now()).order_by(Activity.date.asc()).limit(5).all()
    letzte_aktivitaeten += [f"{e.creator.username} hat ein Event hinzugefügt: '{e.title}' am {e.date.strftime('%d.%m.%Y')}" for e in kommende_events_list]
    
    if not letzte_aktivitaeten:
        letzte_aktivitaeten.append("Momentan gibt es keine Aktivitäten")


    wg_mitglieder = User.query.filter_by(wg_id=wg.wg_id).all()

    heute = datetime.now().strftime("%A, %d.%m.%Y")

    return render_template("dashboard.html", active_page="dashboard", username=user.username, wg_name=wg.name, heute=heute, counting_boxes=counting_boxes, wichtige_hinweise=wichtige_hinweise, letzte_aktivitaeten=letzte_aktivitaeten, wg_mitglieder=wg_mitglieder)



@app.route("/putzplan/", methods=["GET", "POST"])
def putzplan():
    if 'user_id' not in session:
        return redirect(url_for('login'))

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

    return render_template("putzplan.html", form=form, all_users=all_users,putzplan=putzplan_eintraege,
                           total_tasks=total_tasks, completed_tasks=completed_tasks, progress=progress)

@app.route("/putzplan/task/<int:task_id>/toggle", methods=["POST"])
def toggle_cleaning_task(task_id):
    task = CleaningTask.query.get_or_404(task_id)
    task.status = "completed" if request.form.get("done") == "on" else "open"
    db.session.commit()
    return redirect(url_for("putzplan"))

@app.route("/putzplan/task/<int:template_id>/delete", methods=["POST"])
def delete_cleaning_task(template_id):
    #current_user_id = session.get("user_id")
    #if idea.creator.user_id != current_user_id:
     #   flash("Sie können nur Ihre eigenen Tasks löschen.", "error")
        #abort(403)
    template = CleaningTemplate.query.get_or_404(template_id)
    db.session.delete(template)
    db.session.commit()
    flash("Aufgabe erfolgreich gelöscht.", "success")
    return redirect(url_for("putzplan"))



@app.route("/innovationboard/", methods=['GET', 'POST'])
def innovation_board():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
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
                    color=form.color.data or "#ffffff",
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
    return render_template("innovationboard.html", form=form, all_users=all_users,ideas=ideas, comment_form=CommentForm())

@app.route("/innovation_board/idea/<int:idea_id>/delete", methods=["POST"])
def delete_idea(idea_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

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
    if 'user_id' not in session:
        return redirect(url_for('login'))
    #user_id = session.get("user_id")
    #if not user_id:
        #flash("Bitte zuerst einloggen.", "error")
        #return redirect(url_for("login"))

    existing = Idea_Like.query.filter_by(idea_id=idea_id, user_id=1).first() #To be replaced with idea_id=idea_id, user_id=user_id

    if existing:
        db.session.delete(existing)   # unlike
    else:
        db.session.add(Idea_Like(idea_id=idea_id, user_id=1))  # like #TODO: To be replaced with user_id=user_id

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

    return redirect(url_for("innovation_board"))

@app.route("/ideas/<int:idea_id>/comment", methods=["POST"])
def post_comment(idea_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = CommentForm()
    #user_id = session.get("user_id")               #TODO: get user_id from session
    #if not user_id:
        #flash("Bitte zuerst einloggen.", "error")
        #return redirect(url_for("login"))

        
    if request.method == "POST":
        print("Kommentar POST angekommen")
        print("form.validate_on_submit():", form.validate_on_submit())
        print("form.errors:", form.errors)

        if form.validate_on_submit():
            content = (request.form.get("content") or "").strip()

            if content:
                new_comment = Idea_Comment(
                    idea_id=idea_id,
                    user_id=1,  #To be replaced with user_id=user_id 
                    content=content,
                    created_at=db.func.now()
                )
                db.session.add(new_comment)
                db.session.commit()
                flash("Kommentar hinzugefügt.", "success")
            else:
                flash("Kommentar darf nicht leer sein.", "error")
        

    return redirect(url_for("innovation_board"))

@app.route("/activityboard/", methods=['GET', 'POST'])
def activity_board():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = ActivityForm()

    all_users = User.query.all()

    if request.method == "POST":
        print("Aktivität hinzufügen POST angekommen")
        print("form.validate_on_submit():", form.validate_on_submit())
        print("form.errors:", form.errors)

        if form.validate_on_submit():
            flash("Aktivität erfolgreich hinzugefügt!", "success")

            user = User.query.filter_by(username="testuser").first()  # To be replaced with current_user() or session user
            new_activity = Activity(
                wg_id=1,  # wg_id = user.wg_id
                created_by=user.user_id,
                title=form.title.data,
                description=form.description.data,
                date=form.date.data,
                updated_at=form.updated_at.data,
                location=form.location.data,
                
                max_participants=form.max_participants.data,
                created_at=db.func.now()
            )
            db.session.add(new_activity)
            db.session.commit()

            return redirect(url_for("activity_board"))
        else:
            flash("Fehler beim Hinzufügen der Aktivität. Bitte überprüfen Sie die Eingaben.", "error")

    activities = (Activity.query
                  .filter_by(wg_id=1)  # wg_id = user.wg_id
                  .options(joinedload(Activity.creator), joinedload(Activity.participants))
                  .order_by(Activity.created_at.desc())
                  .all())

    return render_template("activityboard.html", form=form, activities=activities, all_users=all_users, current_user_id=1)  #To be replaced with current_user().user_id

@app.route("/activity/<int:activity_id>/join_activity", methods=["POST"])
def join_activity(activity_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session.get("user_id",1)  #Temporary set to 1 for testing
    #if not user_id:
        #flash("Bitte zuerst einloggen.", "error")
        #return redirect(url_for("login"))
    user = User.query.get(user_id)  #To be replaced with user_id=user_id
    activity = Activity.query.get_or_404(activity_id)
    #existing_participant = Activity_Participant.query.filter_by(activity_id=activity_id, user_id=user_id).first()

    if user in activity.participants:
        flash("Du nimmst bereits teil.", "error")
        return redirect(url_for("activity_board"))

    if activity.max_participants and len(activity.participants) >= activity.max_participants:
        flash("Die Aktivität ist bereits voll.", "error")
        return redirect(url_for("activity_board"))

    activity.participants.append(user)
    db.session.commit()
    flash("Du bist beigetreten!", "success")    
    #if not existing_participant:
        #db.session.add(Activity_Participant(activity_id=activity_id, user_id=user_id))
        #db.session.commit()
        #flash("Erfolgreich teilgenommen!", "success")

    return redirect(url_for("activity_board"))

@app.route("/activity/<int:activity_id>/leave_activity", methods=["POST"])
def leave_activity(activity_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session.get("user_id",1)  #Temporary set to 1 for testing
    #if not user_id:
        #flash("Bitte zuerst einloggen.", "error")
        #return redirect(url_for("login"))
    user = User.query.get(user_id)  #To be replaced with user_id=user_id
    activity = Activity.query.get_or_404(activity_id)

    if user not in activity.participants:
        flash("Du nimmst nicht teil.", "error")
        return redirect(url_for("activity_board"))

    activity.participants.remove(user)
    db.session.commit()
    flash("Du hast die Aktivität verlassen.", "success")    
    #existing_participant = Activity_Participant.query.filter_by(activity_id=activity_id, user_id=user_id).first()

    #if existing_participant:
        #db.session.delete(existing_participant)
        #db.session.commit()
        #flash("Erfolgreich ausgetreten!", "success")

    return redirect(url_for("activity_board"),)

@app.route("/activity/<int:activity_id>/delete_activity", methods=["POST"])
def delete_activity(activity_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    #current_user_id = session.get("user_id")
    #if activity.creator.user_id != current_user_id:
     #   flash("Sie können nur Ihre eigenen Aktivitäten löschen.", "error")
        #abort(403)

    activity = Activity.query.get_or_404(activity_id)
    db.session.delete(activity)
    db.session.commit()
    flash("Aktivität erfolgreich gelöscht.", "success")
    return redirect(url_for("activity_board"))


from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload

@app.route("/einkaufsplan/", methods=["GET", "POST"])
def einkaufsplan():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = EinkaufsplanForm()

    # --- Fake current_user: Session -> sonst testuser ---
    user_id = session.get("user_id")
    current_user = User.query.get(user_id) if user_id else None
    if not current_user:
        current_user = User.query.filter_by(username="testuser").first()

    # Falls es den testuser noch nicht gibt -> abbrechen/Fehlermeldung
    if not current_user:
        flash("Testuser fehlt. Bitte einmal anlegen (username='testuser', wg_id=1).", "error")
        return render_template("einkaufsplan.html", form=form, shopping_items=[])

    wg_id = current_user.wg_id or 1

    # --- POST: Item speichern ---
    if request.method == "POST":
        print("Einkaufsplan POST angekommen")
        print("form.validate_on_submit():", form.validate_on_submit())
        print("form.errors:", form.errors)

        if form.validate_on_submit():
            # random zuständig aus der WG (fallback: current_user)
            u = User.query.filter_by(wg_id=wg_id).order_by(func.random()).first()
            assigned_to = u.user_id if u else current_user.user_id

            new_item = ShoppingItem(
                wg_id=wg_id,
                added_by=current_user.user_id,
                name=form.item.data,
                quantity=form.quantity.data,
                assigned_to=assigned_to
            )
            db.session.add(new_item)
            db.session.commit()

            flash("Artikel erfolgreich hinzugefügt!", "success")
            return redirect(url_for("einkaufsplan"))
        else:
            flash("Fehler beim Hinzufügen. Bitte Eingaben prüfen.", "error")

    # --- GET (oder POST mit Fehlern): Items anzeigen ---
    shopping_items = (ShoppingItem.query
        .filter_by(wg_id=wg_id)
        .options(
            joinedload(ShoppingItem.assigned_to_user),
            joinedload(ShoppingItem.added_by_user)
        )
        .order_by(ShoppingItem.item_id.desc())
        .all()
    )

    return render_template("einkaufsplan.html", form=form, shopping_items=shopping_items)


  #wg_id = user.wg_id  #Temporary set to 1 for testing
     

@app.route("/einkaufsplan/item/<int:item_id>/delete", methods=["POST"])
def delete_shopping_item(item_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    item = ShoppingItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Artikel erfolgreich gelöscht.", "success")
    return redirect(url_for("einkaufsplan"))

from urllib.parse import urlencode

def google_calendar_url(title, start_dt, end_dt, details="", location=""):
    #In UTC umwandeln
    fmt = "%Y%m%dT%H%M%S"
    dates = f"{start_dt.strftime(fmt)}/{end_dt.strftime(fmt)}"

    params = {
        "action": "TEMPLATE",
        "text": title,
        "dates": dates,
        "details": details,
        "location": location,
    }
    return "https://calendar.google.com/calendar/render?" + urlencode(params)


def dt_to_ics(dt):
    # am besten UTC
    dt_utc = dt.replace(tzinfo=timezone.utc)
    return dt_utc.strftime("%Y%m%dT%H%M%SZ")

def build_ics(uid, title, start_dt, end_dt, description="", location=""):
    return "\r\n".join([
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//WG Planner//DE",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTART:{dt_to_ics(start_dt)}",
        f"DTEND:{dt_to_ics(end_dt)}",
        f"SUMMARY:{title}",
        f"DESCRIPTION:{description}",
        f"LOCATION:{location}",
        "END:VEVENT",
        "END:VCALENDAR",
        ""
    ])

@app.route("/activities/<int:activity_id>/ics")
def activity_ics(activity_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    activity = Activity.query.get_or_404(activity_id)

    ics = build_ics(
        uid=f"activity-{activity.activity_id}@wgplanner",
        title=activity.title,
        start_dt=activity.date,     # oder activity.time
        end_dt=activity.updated_at,       # ggf. + timedelta(hours=2)
        description=activity.description or "",
        location=activity.location or "",
    )

    return Response(
        ics,
        mimetype="text/calendar",
        headers={"Content-Disposition": f'attachment; filename="activity-{activity_id}.ics"'}
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # erstellt alle Tabellen in der Datenbank
    app.run(debug=True)

