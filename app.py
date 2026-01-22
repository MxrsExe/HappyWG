from os import name
from random import random
from sqlite3 import IntegrityError
import string
from tempfile import template
from flask import Flask, current_app, flash, jsonify, redirect, render_template,request, url_for,session, Response, abort
from datetime import timezone
from flask_migrate import Migrate
from sqlalchemy import func, text
from sqlalchemy.orm import joinedload
import random
from datetime import datetime
from datetime import timezone
from functools import wraps


from db import Activity, CleaningTask, CleaningTemplate, Idea, Idea_Comment, Idea_Like, ShoppingItem,db, User, Wg
from werkzeug.security import check_password_hash, generate_password_hash

from docs.forms import ActivityForm, CommentForm, EinkaufsplanForm, InnovationForm, PutzplanForm, RegisterForm, LoginForm

def generate_unique_code(length=6):
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

        if not Wg.query.filter_by(invite_code=code).first():
            return code
    

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

 #bevor eine route ausgeführt wird, prüfen ob der User eingeloggt ist!   
def login_required(f):
    @wraps(f)                                   #f ist die Funktion die geschützt werden soll
    def decorated_function(*args, **kwargs):    #neue Funktion läuft statt der alten
        if 'user_id' not in session:
            flash("Bitte zuerst einloggen", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
    
 #login-Funktion   
@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()              #Username + Passwort

    #Nach Login submit wird der Name geprüft, ob in DB vorhanden
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

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
@login_required
def create_or_join_wg():
    
    user = User.query.get(session['user_id'])

    if not user:
        session.clear()
        return redirect(url_for("login"))


    return render_template("welcome.html", username=user.username)

@app.route("/welcome/create_wg/", methods=['GET', 'POST'])
@login_required
def create_wg():

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
@login_required
def join_wg():

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
        if not user:
            session.clear()
            return redirect(url_for("login"))

        user.wg_id = wg.wg_id
        db.session.commit()  

        flash(f"Du bist der WG '{wg.name}' erfolgreich beigetreten!", "success")
        return redirect(url_for('dashboard'))

    return render_template("join_wg.html")


@app.route("/dashboard/", methods=['GET'])
@login_required
def dashboard():

    user = User.query.get(session['user_id'])
    if not user or not user.wg_id:
        return redirect(url_for('create_or_join_wg'))
    if not user:
        session.clear()
        return redirect(url_for("login"))

    wg = Wg.query.get(user.wg_id)



    offene_putzaufgaben_count = CleaningTask.query.filter_by(assigned_to=user.user_id, status='open').count()
    
    neue_ideen_count = Idea.query.filter_by(wg_id=wg.wg_id).count()
    
    kommende_events = Activity.query.filter(Activity.wg_id==wg.wg_id, Activity.date >= datetime.now()).count()

    einkauf_count = ShoppingItem.query.filter_by(wg_id=wg.wg_id, assigned_to=user.user_id).count()

    counting_boxes = {
        'putzaufgaben': max(offene_putzaufgaben_count, 0),
        'ideen': max(neue_ideen_count, 0),
        'events': max(kommende_events, 0),
        'einkauf': max(einkauf_count, 0)
    }
    #Hinweis-Box
    wichtige_hinweise = {
        "putz": [],
        "einkauf": [],
        "events": []
    }

    putz_tasks = CleaningTask.query.filter_by(assigned_to=user.user_id, status="open").all()
    for t in putz_tasks:
        wichtige_hinweise ["putz"].append(t.template.name)

    offene_einkaufs_items = ShoppingItem.query.filter(ShoppingItem.wg_id == wg.wg_id).all()
    for item in offene_einkaufs_items:
        wichtige_hinweise["einkauf"].append(item.name)

    kommende_events_list = Activity.query.filter(Activity.wg_id==wg.wg_id, Activity.date >= datetime.now()).order_by(Activity.date.asc()).limit(5).all()
    for e in kommende_events_list:
        wichtige_hinweise["events"].append({
            "title": e.title,
            "date": e.date
        })

    if not wichtige_hinweise:
        wichtige_hinweise = ["Momentan gitbt es keine offenen Aufgaben oder Hinweise!"]


    #Activity-Box
    letzte_aktivitaeten = []

    erledigte_putzaufgaben = CleaningTask.query.filter_by(assigned_to=user.user_id, status="completed").order_by(CleaningTask.completed_at.desc()).limit(10).all()
    for t in erledigte_putzaufgaben:
        letzte_aktivitaeten.append({"zeitpunkt": t.completed_at, "text": f"<strong>{t.assigned_user.username}</strong> hat {t.template.name} geputzt", "typ": "putz"})

    neue_einkaufs_items = ShoppingItem.query.filter(ShoppingItem.wg_id == wg.wg_id).order_by(ShoppingItem.created_at.desc()).limit(10).all()
    for ein in neue_einkaufs_items:
        letzte_aktivitaeten.append({"zeitpunkt": ein.created_at, "text": f"<strong>{ein.added_by_user.username}</strong>  hat '{ein.name}' zur Einkaufsliste hinzugefügt", "typ": "einkauf"})

    letzte_ideen = Idea.query.filter_by(wg_id=wg.wg_id).order_by(Idea.created_at.desc()).limit(10).all()
    for i in letzte_ideen:
        letzte_aktivitaeten.append({"zeitpunkt": i.created_at, "text": f"<strong>{i.creator.username}</strong> hat eine Idee hinzugefügt: '{i.title}'", "typ": "idee"})

    kommende_events_list = Activity.query.filter(Activity.wg_id == wg.wg_id, Activity.date >= datetime.now()).order_by(Activity.date.asc()).limit(5).all()
    for e in kommende_events_list:
        letzte_aktivitaeten.append({"zeitpunkt": e.created_at or e.date, "text": f"<strong>{e.creator.username}</strong> hat ein Event hinzugefügt: " f"'{e.title}' am {e.date.strftime('%d.%m.%Y')}", "typ": "event"})
    
    if not letzte_aktivitaeten:
        letzte_aktivitaeten.append({"zeitpunkt": None, "text": "Momentan gibt es keine Aktivitäten"})

    letzte_aktivitaeten.sort(key=lambda x: x.get("zeitpunkt") or datetime.min, reverse=True) #Quelle: ChatGPT
    letzte_aktivitaeten = letzte_aktivitaeten[:10]

    wg_mitglieder = User.query.filter_by(wg_id=wg.wg_id).all()

    heute = datetime.now().strftime("%A, %d.%m.%Y")
    
    return render_template("dashboard.html", active_page="dashboard", username=user.username, wg_name=wg.name, heute=heute, counting_boxes=counting_boxes, wichtige_hinweise=wichtige_hinweise, letzte_aktivitaeten=letzte_aktivitaeten, wg_mitglieder=wg_mitglieder)



@app.route("/putzplan/", methods=["GET", "POST"])
@login_required
def putzplan():
    
    #aktuellen User laden
    user = User.query.get(session["user_id"])

    #Wenn kein User -> weiterleiten (sollte nicht passieren)
    if not user:
        session.clear()
        return redirect(url_for("login"))

    form = PutzplanForm() 
    #Alle WG-Mitglieder laden für das Dropdown im Formular (Zuständigkeit auswählen im Modal)
    all_users = User.query.filter_by(wg_id=user.wg_id).all()

    #POST: Neue Putzplan-Aufgabe erstellen
    if request.method == "POST":
        if form.validate_on_submit():
            zustaendig_name = request.form.get("zustaendig", "").strip() #Name des zuständigen WG-Mitglieds aus dem Formular holen

            #Zuständigen User aus der DB laden
            assigned_user = User.query.filter_by(
                wg_id=user.wg_id,
                username=zustaendig_name
            ).first()

            #Fehlermeldung, falls der User nicht existiert (sollte nicht passieren, da aus Dropdown gewählt wird)
            if not assigned_user:
                flash("WG-Mitglied existiert nicht", "error")
                return redirect(url_for("putzplan"))
            #Neue Vorlage und Task erstellen, falls noch nicht vorhanden 
        
            else:
                new_template = CleaningTemplate(
                    wg_id=user.wg_id,
                    name=form.aufgabe.data,
                    description=f"KW {form.woche.data}: {form.von_datum.data} bis {form.bis_datum.data}",
                    frequency="weekly", #nicht implementiert
                    is_active=True
                )
                db.session.add(new_template)
                #flush() = vorübergehendes Speichern, aber noch kein Commit
                db.session.flush() #Damit new_template.template_id verfügbar ist, bevor commit() aufgerufen wird (für Task)

                #Neuen Task erstellen mithilfe von der soeben erstellten Vorlage
                new_task = CleaningTask(
                    template_id=new_template.template_id,
                    assigned_to=assigned_user.user_id,
                    status="open",
                    notes="Zuständig"
                )
                #Commiten der Änderungen in der DB
                db.session.add(new_task)
                db.session.commit()

                flash("Eintrag erfolgreich erstellt!", "success")
                return redirect(url_for("putzplan"))

    putzplan_eintraege = (CleaningTemplate.query
                          .filter_by(wg_id=user.wg_id, is_active=True)  #Filtern nach wg_id und is_active = True, damit nur aktive Einträge direkt angezeigt werden (standard)
                          .order_by(CleaningTemplate.template_id.desc()) #Sortieren nach template_id absteigend
                          .all()) #Alle Einträge der WG holen

    tasks = (CleaningTask.query
             .join(CleaningTemplate) # Join mit CleaningTemplate für wg_id
             .filter(CleaningTemplate.wg_id == user.wg_id)  # Filtern nach wg_id
             .all())    #Alle Tasks holen
    
    #Berechnung des Fortschritts
    total_tasks = len(tasks)
    #Anzahl der abgeschlossenen Tasks berechnen
    completed_tasks = sum(1 for t in tasks if t.status == "completed")
    #Fortschritt in Prozent berechnen, wenn keine gibt, dann 0% und Progressbar bleibt leer
    progress = int((completed_tasks / total_tasks) * 100) if total_tasks else 0

    return render_template(
        "putzplan.html",
        form=form,
        all_users=all_users,
        putzplan=putzplan_eintraege,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        progress=progress
    )


@app.route("/putzplan/task/<int:task_id>/toggle", methods=["POST"])
@login_required
def toggle_cleaning_task(task_id):
    #task_id aus der URL holen
    task = CleaningTask.query.get_or_404(task_id)

    #Status umschalten
    if task.status == "completed":
        task.status = "open"
        task.completed_at = None
    else:
        task.status = "completed"
        task.completed_at = datetime.now()

    #Speichern in der DB
    db.session.commit()
    return redirect(url_for("putzplan"))

@app.route("/putzplan/task/<int:template_id>/delete", methods=["POST"])
def delete_cleaning_task(template_id):
    user_id = session.get("user_id")
    template = CleaningTemplate.query.get_or_404(template_id)
    
    #Task
    task = template.tasks[0] if template.tasks else None
    if not task:
        flash("Kein Task gefunden.", "error")
        return redirect(url_for("putzplan"))

    if task.assigned_to != user_id:
        flash("Nur die zuständige Person kann diese Aufgabe löschen.", "error")
        return redirect(url_for("putzplan"))
    
    db.session.delete(template)
    db.session.commit()
    flash("Aufgabe erfolgreich gelöscht.", "success")
    return redirect(url_for("putzplan"))


@app.route("/innovationboard/", methods=['GET', 'POST'])
@login_required
def innovation_board():
    user_id = int(session["user_id"])
    
    form = InnovationForm()
    #aktuellen User laden
    user = User.query.filter_by(user_id=user_id).first()

    all_users = User.query.all()
    #POST: Neue Idee erstellen
    if request.method == 'POST':
        #Wenn das Formular valide ist, erstelle neue Idee (Instanz), Abrufen der Formulardaten
        if form.validate_on_submit():
                flash("Innovation erfolgreich eingereicht!", "success")
                
                new_idea = Idea(
                    wg_id=user.wg_id,
                    created_by=user.user_id,
                    title=form.title.data,
                    description=form.description.data,
                    color=form.color.data or "#ffffff",
                    created_at=db.func.now()
                
                )
                #Hinzufügen und Speichern in der DB
                db.session.add(new_idea)
                db.session.commit()

                return redirect(url_for("innovation_board"))
        else:
            flash("Fehler beim Einreichen der Innovation. Bitte überprüfen Sie die Eingaben.", "error")
    #Ideen anzeigen, nach WG filtern, mit User-Relationen laden, absteigend sortieren, alle holen, joinedload(...) für weniger Queries und richtiges Laden der Relationen
    ideas = (Idea.query
             .filter_by(wg_id=user.wg_id)   
             .options(joinedload(Idea.creator)) 
             .order_by(Idea.created_at.desc())
             .all())
    
    return render_template("innovationboard.html", form=form, all_users=all_users,ideas=ideas, comment_form=CommentForm())

#post route, da das Formular data ändert (löschen)
@app.route("/innovation_board/idea/<int:idea_id>/delete", methods=["POST"])
@login_required
def delete_idea(idea_id):

    #aktuellen User laden und konkrete Idee laden, prüfen ob der User der Ersteller der Idee ist, wenn nicht -> 403 und Flashmeldung
    #Bezug auf creator: Beziehung in Idea Model
    idea = Idea.query.get_or_404(idea_id)
    user_id = int(session["user_id"])
    if idea.created_by != user_id:
        flash("Sie können nur Ihre eigenen Ideen löschen.", "error")
        return redirect(url_for("innovation_board"))
    
    #Idee löschen
    db.session.delete(idea) 
    db.session.commit()
    flash("Idee erfolgreich gelöscht.", "success")
    return redirect(url_for("innovation_board"))

#post route, da das Formular data ändert (aktualisiert)
@app.route("/ideas/<int:idea_id>/like", methods=["POST"])
@login_required
def toggle_like(idea_id):

    #User_id holen und Guard-Klausel: Sicherstellen, dass der User eingeloggt ist
    user_id = int(session["user_id"])  
    if 'user_id' not in session:
        return redirect(url_for('login'))
    #Überprüfen, ob der User die Idee bereits geliked hat
    existing = Idea_Like.query.filter_by(idea_id=idea_id, user_id=user_id).first() #first() gibt None zurück, wenn kein Eintrag gefunden wurde

    #Wenn ja, Like entfernen, sonst Like hinzufügen
    if existing:
        db.session.delete(existing)   # unlike
    else:
        db.session.add(Idea_Like(idea_id=idea_id, user_id=user_id))  # like
    #Commit changes to the database
    try:
        db.session.commit()
    #IntegrityError abfangen (z.B. bei doppeltem Like, sollte nicht passieren durch obige Logik)
    except IntegrityError:
        db.session.rollback()

    return redirect(url_for("innovation_board"))

#Post route, da das Formular data ändert (neuer Kommentar erstellen)
@app.route("/ideas/<int:idea_id>/comment", methods=["POST"])
@login_required
def post_comment(idea_id):
   
    user_id = int(session["user_id"])

    #Formular initialisieren
    form = CommentForm()
    #POST: Kommentar speichern    
    if request.method == "POST":
        #Wenn das Formular valide ist, erstelle neuen Kommentar (Instanz), Abrufen der Formulardaten
        if form.validate_on_submit():
            #content aus dem Formular holen (was in dem Feld steht, aus html name="content")
            content = (request.form.get("content") or "").strip()

            #Nur speichern, wenn content in der Kommentar-Box nicht leer ist
            if content:
                new_comment = Idea_Comment(
                    idea_id=idea_id,
                    user_id=user_id,  
                    content=content,
                    created_at=db.func.now()
                )
                #Kommentar in die Datenbank speichern
                db.session.add(new_comment)
                db.session.commit()
                flash("Kommentar hinzugefügt.", "success")
            else:
                flash("Kommentar darf nicht leer sein.", "error")
        

    return redirect(url_for("innovation_board"))

#Get und Post route, da das Formular data abruft und ändert (neue Aktivität erstellen) 
@app.route("/activityboard/", methods=["GET", "POST"])
@login_required
def activity_board():

    #aktuellen User laden
    user = User.query.get(session["user_id"])
    #Wenn kein User oder keine WG -> weiterleiten (sollte nicht passieren)
    if not user or not user.wg_id:
        return redirect(url_for("create_or_join_wg"))

    # aktuelle WG ID vom User für new_activity
    wg_id = user.wg_id
    form = ActivityForm()

    #POST: Neue Aktivität erstellen
    if request.method == "POST":
        #Wenn das Formular valide ist, erstelle neue Aktivität (Instanz), Abrufen der Formulardaten
        if form.validate_on_submit():
            new_activity = Activity(
                wg_id=wg_id,
                created_by=user.user_id,
                title=form.title.data,
                description=form.description.data,
                date=form.date.data,
                updated_at=form.updated_at.data,
                location=form.location.data,
                max_participants=form.max_participants.data,
                created_at=db.func.now()
            )
            #Hinzufügen und Speichern in der DB
            db.session.add(new_activity)
            db.session.commit()
            return redirect(url_for("activity_board"))
    #Aktivitäten anzeigen, nach WG filtern, mit User-Relationen laden, absteigend sortieren, alle holen, joinedload(...) für weniger Queries und richtiges Laden der
    #Relationen
    activities = (Activity.query
        .filter_by(wg_id=wg_id)
        .options(joinedload(Activity.creator), joinedload(Activity.participants))
        .order_by(Activity.created_at.desc())
        .all())

    #Rendern der Seite mit Formular und Aktivitäten
    return render_template(
        "activityboard.html",
        form=form,
        activities=activities,
        current_user_id=user.user_id
    )
 
#post route, da das Formular data ändert (aktualisiert)
@app.route("/activity/<int:activity_id>/join_activity", methods=["POST"])
@login_required
def join_activity(activity_id):

    #aktuelle user_id holen und User und Aktivität laden
    user_id = int(session["user_id"])  
   
    user = User.query.get(user_id)  
    activity = Activity.query.get_or_404(activity_id)

    # Prüfen, ob der User bereits Teilnehmer ist, damit er/sie nicht doppelt beitreten kann
    if user in activity.participants:
        flash("Du nimmst bereits teil.", "error")
        return redirect(url_for("activity_board"))

    # Prüfen, ob die maximale Teilnehmerzahl erreicht ist, len(activity.participants) gibt die aktuelle Anzahl der Teilnehmer zurück
    if activity.max_participants and len(activity.participants) >= activity.max_participants:
        flash("Die Aktivität ist bereits voll.", "error")
        return redirect(url_for("activity_board"))

    # User zur Teilnehmerliste hinzufügen
    activity.participants.append(user)
    db.session.commit()
    flash("Du bist beigetreten!", "success")    

    return redirect(url_for("activity_board"))

#post route, da das Formular data ändert (aktualisiert) 
@app.route("/activity/<int:activity_id>/leave_activity", methods=["POST"])
@login_required
def leave_activity(activity_id):
    #Guard Klausel: Sicherstellen, dass der User eingeloggt ist (sollte nicht passieren.)
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    #aktuelle user_id holen
    user_id = int(session["user_id"])  
    
    #User aus user_id und Aktivität laden
    user = User.query.get(user_id)  
    activity = Activity.query.get_or_404(activity_id)

    # Prüfen, ob der User tatsächlich Teilnehmer ist
    if user not in activity.participants:
        flash("Du nimmst nicht teil.", "error")
        return redirect(url_for("activity_board"))

    # User aus der Teilnehmerliste entfernen
    activity.participants.remove(user)
    db.session.commit()
    flash("Du hast die Aktivität verlassen.", "success")    
    #existing_participant = Activity_Participant.query.filter_by(activity_id=activity_id, user_id=user_id).first()

    #if existing_participant:
        #db.session.delete(existing_participant)
        #db.session.commit()
        #flash("Erfolgreich ausgetreten!", "success")

    return redirect(url_for("activity_board"))

@app.route("/activity/<int:activity_id>/delete_activity", methods=["POST"])
@login_required
def delete_activity(activity_id):
    
    #aktuellen User laden und konkrete Aktivität laden
    current_user_id = int(session["user_id"])
    activity = Activity.query.get_or_404(activity_id)
    # Prüfen, ob der aktuelle User der Ersteller der Aktivität ist, creator ist die Beziehung in Activity Model
    if activity.created_by != current_user_id:
        flash("Sie können nur Ihre eigenen Aktivitäten löschen.", "error")
        
        return redirect(url_for("activity_board"))
    # Aktivität löschen
    db.session.delete(activity)
    db.session.commit()
    flash("Aktivität erfolgreich gelöscht.", "success")
    return redirect(url_for("activity_board"))


@app.route("/einkaufsplan/", methods=["GET", "POST"])
@login_required
def einkaufsplan():
    
    #Formular initialisieren aus forms.py
    form = EinkaufsplanForm()

    #Aktuellen User laden
    user_id = int(session["user_id"])
    current_user = User.query.get(user_id) if user_id else None
    #Fallback: User aus der DB laden
    if not current_user:
        current_user = User.query.filter_by(user_id=user_id).first()

    #Falls es den user noch nicht gibt -> abbrechen/Fehlermeldung (sollte nicht passieren)
    if not current_user:
        flash("User fehlt", "error")
        return render_template("einkaufsplan.html", form=form, shopping_items=[])
    
    #  aktuelle WG ID für new_item
    wg_id = current_user.wg_id 

    # POST: Item speichern 
    if request.method == "POST":

        if form.validate_on_submit():
            # random zuständig aus der WG (fallback: current_user)
            u = User.query.filter_by(wg_id=wg_id).order_by(func.random()).first() #random() ist aus sqlalchemy, nicht random modul

            #Random WG-Member wird ein Produkt zugewiesen, falls kein User in der WG ist, wird der aktuelle User zugewiesen
            assigned_to = u.user_id if u else current_user.user_id

            #Neues Einkaufs-Item erstellen (Instanz)
            new_item = ShoppingItem(
                wg_id=wg_id,
                added_by=current_user.user_id,
                #name, quantity aus Formular
                name=form.item.data,
                quantity=form.quantity.data,
                assigned_to=assigned_to
            )
            #Hinzufügen und Speichern in der DB
            db.session.add(new_item)
            db.session.commit()

            #Flashmeldung und Weiterleitung
            flash("Artikel erfolgreich hinzugefügt!", "success")
            return redirect(url_for("einkaufsplan"))
        else:
            flash("Fehler beim Hinzufügen. Bitte Eingaben prüfen.", "error")

    #Items anzeigen, nach WG filtern, mit User-Relationen laden, absteigend sortieren, alle holen, .options(joinedload(...)) für weniger Queries
    shopping_items = (ShoppingItem.query
        .filter_by(wg_id=wg_id)
        .options(
            joinedload(ShoppingItem.assigned_to_user),
            joinedload(ShoppingItem.added_by_user)
        )
        .order_by(ShoppingItem.item_id.desc())
        .all()
    )

    #Rendern der Seite mit Formular und Items
    return render_template("einkaufsplan.html", form=form, shopping_items=shopping_items)
     
# Delete Einkaufs Item
@app.route("/einkaufsplan/item/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_shopping_item(item_id):
    #Guard Klausel: Sicherstellen, dass der User eingeloggt ist (sollte nicht passieren.)
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Laden des Items
    item = ShoppingItem.query.get_or_404(item_id)
    #aus der DB löschen und commiten
    db.session.delete(item)
    db.session.commit()
    flash("Artikel erfolgreich gelöscht.", "success")
    return redirect(url_for("einkaufsplan"))

from urllib.parse import urlencode

# Google Calendar URL erstellen
def google_calendar_url(title, start_dt, end_dt, details="", location=""):
    #In UTC umwandeln
    fmt = "%Y%m%dT%H%M%S" #ICS Format
    dates = f"{start_dt.strftime(fmt)}/{end_dt.strftime(fmt)}" #Start/Ende

    #Parameter für die URL, was soll sie enthalten
    params = {
        "action": "TEMPLATE",
        "text": title,
        "dates": dates,
        "details": details,
        "location": location,
    }
    return "https://calendar.google.com/calendar/render?" + urlencode(params)

# Datum/Zeit in ICS Format umwandeln
def dt_to_ics(dt):
    # am besten UTC
    dt_utc = dt.replace(tzinfo=timezone.utc)
    return dt_utc.strftime("%Y%m%dT%H%M%SZ")

# ICS-Datei erstellen
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


# App route für ICS Export für Activities
@app.route("/activities/<int:activity_id>/ics", methods=["POST"])
@login_required
def activity_ics(activity_id):

    # Sicherstellen, dass der User eingeloggt ist (Guard Klausel, sollte nicht passieren.)
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Aktivität laden
    activity = Activity.query.get_or_404(activity_id)

    # ICS erstellen (instanzieren)
    ics = build_ics(
        uid=f"activity-{activity.activity_id}@wgplanner",
        title=activity.title,
        start_dt=activity.date,     # oder activity.time
        end_dt=activity.updated_at,       # ggf. + timedelta(hours=2)
        description=activity.description or "",
        location=activity.location or "",
    )
    # ICS als Download zurückgeben
    return Response(
        ics,
        mimetype="text/calendar",
        headers={"Content-Disposition": f'attachment; filename="activity-{activity_id}.ics"'}
    )

#wg Daten als JSON exportieren
@app.route("/export/wg.json", methods=["GET"])
def export_wg_json():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    wg = Wg.query.get(user.wg_id)
    members = User.query.filter_by(wg_id=wg.wg_id).all()
    # Daten für JSON Export
    data = {
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        },
        "members": [
            {
                "user_id": member.user_id,
                "username": member.username,
                "email": member.email,
                "role": member.role
            }
            for member in members
        ],
        "wg": {
            "wg_id": wg.wg_id,
            "name": wg.name,
            "invite_code": wg.invite_code
        },
        "activities": [
            {
                "activity_id": activity.activity_id,
                "title": activity.title,
                "description": activity.description,
                "date": activity.date,
                "location": activity.location,
                "max_participants": activity.max_participants
            }
            for activity in wg.activities
        ],
        "ideas": [
            {
                "idea_id": idea.idea_id,
                "title": idea.title,
                "description": idea.description,
                "status": idea.status,
                "color": idea.color
            }
            for idea in wg.ideas
        ],
        "shopping_items": [
            {
                "item_id": item.item_id,
                "name": item.name,
                "quantity": item.quantity
            }
            for item in wg.shopping_items
        ],
        "cleaning_tasks": [
            {
                "task_id": task.task_id,
                "template_name": task.template.name,
                "assigned_to": task.assigned_to,
                "status": task.status
                
            }
            for template in wg.cleaning_templates
            for task in template.tasks
        ],

        "exported_at": datetime.now().isoformat()
    }

    return jsonify(data)

#run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # erstellt alle Tabellen in der Datenbank
    app.run(debug=True)

