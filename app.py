
from random import random
from sqlite3 import IntegrityError
import string
from flask import Flask, flash, jsonify, redirect, render_template,request, url_for,session, Response, abort
from datetime import timezone
from sqlalchemy import func
from sqlalchemy.orm import joinedload
import random
from datetime import datetime
from datetime import timezone
from functools import wraps


from db import Activity, CleaningTask, CleaningTemplate, Idea, Idea_Comment, Idea_Like, ShoppingItem,db, User, Wg
from werkzeug.security import check_password_hash, generate_password_hash

from forms import ActivityForm, CommentForm, EinkaufsplanForm, InnovationForm, PutzplanForm, RegisterForm, LoginForm


app = Flask(__name__)

#Quellen: ChatGPT (nach Debug: "es steht tatsächlich 0", "er zeigt trotzdem noch 0 einträge, wieso") + 
#https://hwrberlin.github.io/fswd/fswd-intro.html#5-bonus-deliver-json-instead-of-html-to-the-web-server
app.config['SECRET_KEY'] = 'HappyWG_Project_SecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///happywg.sqlite'

db.init_app(app)

#----------------------------------------------------------------------------------------------------------------
#Quelle: https://hwrberlin.github.io/fswd/fswd-intro.html#5-bonus-deliver-json-instead-of-html-to-the-web-server
@app.cli.command()
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        print("Database initialized!")

#----------------------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
#Quelle: https://hwrberlin.github.io/fswd/fswd-intro.html#5-bonus-deliver-json-instead-of-html-to-the-web-server
def index():

    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))
#----------------------------------------------------------------------------------------------------------------
#Quellen: Angelehnt an: GeeksforGeeks, "Generate random string of given length", (Zugriff 10.01.2026).,
#ChatGPT (Prompt: Hier ist meine aktuelle Code-Generierung:...Was müsste ich ändern, damit ich zufällige, eindeutige Invite-Codes erstelle, die nicht in der Datenbank existieren?)
def generate_unique_code(length=6):
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

        if not Wg.query.filter_by(invite_code=code).first():
            return code

#----------------------------------------------------------------------------------------------------------------
# Quelle: Lehrmaterial Full Stack Web Development, HWR Berlin, 
# "Python - Part 2", https://hwrberlin.github.io/fswd/python-pt2.html, Zugriff am 10.01.2026.
 #bevor eine Route ausgeführt wird, prüfen ob der User eingeloggt ist!   
def login_required(f):
    @wraps(f)                                   #f ist die Funktion die geschützt werden soll
    def decorated_function(*args, **kwargs):    #neue Funktion läuft statt der alten
        if 'user_id' not in session:
            flash("Bitte zuerst einloggen", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

#----------------------------------------------------------------------------------------------------------------
#Quelle: Angelehnt an: Lehrmaterial Full Stack Web Development, HWR Berlin, 
# "User Interfaces", https://hwrberlin.github.io/fswd/user-interfaces.html, Zugriff am 08.01.2026.
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

#----------------------------------------------------------------------------------------------------------------
#Quelle: Stack Overflow, "How do I clear a flask session?", (Zugriff: 13.01.2026)   
@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for('login'))

#----------------------------------------------------------------------------------------------------------------
#Quelle: ChatGPT (Prompt: Hier ist mein bisheriger Code für die Registrierungsroute, was fehlt noch?: ...)
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

#----------------------------------------------------------------------------------------------------------------
#Quelle: ChatGPT (Prompt: Ich habe die Route für die Welcome-Seite nach dem Login oder Register: Welche Funktionen sind wichtig?...)
@app.route("/welcome/", methods=['GET', 'POST'])
@login_required
def create_or_join_wg():
    
    user = User.query.get(session['user_id'])

    return render_template("welcome.html", username=user.username)

#----------------------------------------------------------------------------------------------------------------
#Quelle:
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

#----------------------------------------------------------------------------------------------------------------
#Quelle: ChatGPT (Prompt: Wie kann ich in Flask prüfen, ob ein POST-Request erfolgt ist, und gleichzeitig das Formularfeld invite_code auslesen, auf Leerwert prüfen und eine Flash-Meldung ausgeben?)
@app.route("/welcome/join_wg/", methods=['GET', 'POST'])
@login_required
def join_wg():

    if request.method == 'POST':
        invite_code = request.form.get('invite_code', '').strip().upper()

        if not invite_code:
            flash("Bitte gib einen Einladungscode ein.", "danger")
            return redirect(url_for('join_wg'))

        wg = Wg.query.filter_by(invite_code=invite_code).first()

        user = User.query.get(session['user_id'])
    
        user.wg_id = wg.wg_id
        db.session.commit()  

        flash(f"Du bist der WG '{wg.name}' erfolgreich beigetreten!", "success")
        return redirect(url_for('dashboard'))

    return render_template("join_wg.html")


@app.route("/dashboard/", methods=['GET'])
@login_required
def dashboard():

    user = User.query.get(session['user_id'])

    wg = Wg.query.get(user.wg_id)

#Quellen: Angelehnt an: ChatGPT (Prompt: Ich möchte auf meiner Dashboard-Seite für einen Nutzer verschiedene Zähler anzeigen: offene Aufgaben, neue Ideen, kommende Events und Einkäufe. Wie kann ich die Anzahl der passenden Einträge aus der Datenbank mit SQLAlchemy abrufen?)
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
    
#Quelle: Lehrmaterial Full Stack Web Development, HWR Berlin, 
# "Python, Part 1, u.a. Data Structures", https://hwrberlin.github.io/fswd/python.html, Zugriff am 14.01.2026.
    #Hinweis-Box
    wichtige_hinweise = {
        "putz": [],
        "einkauf": [],
        "events": []
    }

    putz_tasks = CleaningTask.query.filter_by(assigned_to=user.user_id, status="open").all()
    for t in putz_tasks:
        wichtige_hinweise ["putz"].append(t.template.name)

    offene_einkaufs_items = ShoppingItem.query.filter_by(wg_id=wg.wg_id, assigned_to=user.user_id).all()
    for item in offene_einkaufs_items:
        wichtige_hinweise["einkauf"].append(item.name)

    kommende_events_list = Activity.query.filter(Activity.wg_id==wg.wg_id, Activity.date >= datetime.now()).order_by(Activity.date.asc()).limit(5).all()
    for e in kommende_events_list:
        wichtige_hinweise["events"].append({
            "title": e.title,
            "date": e.date
        })

    if not wichtige_hinweise:
        wichtige_hinweise = ["Momentan gibt es keine offenen Aufgaben oder Hinweise!"]


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
#----------------------------------------------------------------------------------------------------------------  
    #Quelle: ChatGPT (Prompt: Ich habe ja eine Liste von Aktivitäten mit Zeitpunkten. Wie kann ich sie so sortieren, dass die neuesten zuerst stehen, und danach nur die letzten 10 Elemente behalten?)
    letzte_aktivitaeten.sort(key=lambda x: x.get("zeitpunkt") or datetime.min, reverse=True) 
    letzte_aktivitaeten = letzte_aktivitaeten[:10]

    wg_mitglieder = User.query.filter_by(wg_id=wg.wg_id).all()

    heute = datetime.now().strftime("%A, %d.%m.%Y")
    
    return render_template("dashboard.html", active_page="dashboard", username=user.username, wg_name=wg.name, heute=heute, counting_boxes=counting_boxes, wichtige_hinweise=wichtige_hinweise, letzte_aktivitaeten=letzte_aktivitaeten, wg_mitglieder=wg_mitglieder)

@app.route("/putzplan/", methods=["GET", "POST"])
@login_required
def putzplan():
    #--------------------------------------------------------------------------------------------------------
    #aktuellen User laden
    #Quellen: ChatGPT (Prompt: Bugfix: AttributeError 'NoneType' object has no attribute 'wg_id')
    user = User.query.get(session["user_id"])
    #--------------------------------------------------------------------------------------------------------
    #Wenn kein User -> weiterleiten (sollte nicht passieren)
    if not user:
        session.clear()
        return redirect(url_for("login"))

    form = PutzplanForm() 
#--------------------------------------------------------------------------------------------------------------
    #Alle WG-Mitglieder laden für das Dropdown im Formular (Zuständigkeit auswählen im Modal)
    #Quellen: ChatGPT (Prompt: Bugfix AttributeError 'NoneType' object has no attribute 'wg_id')
    all_users = User.query.filter_by(wg_id=user.wg_id).all()
#--------------------------------------------------------------------------------------------------------------
    #POST: Neue Putzplan-Aufgabe erstellen
    if request.method == "POST":
        if form.validate_on_submit():
        #--------------------------------------------------------------------------------------------------------------
            #Quellen: ChatGPT (Prompt/Debug: validate_on_submit False)
            zustaendig_name = request.form.get("zustaendig", "").strip() #Name des zuständigen WG-Mitglieds aus dem Formular holen
        #--------------------------------------------------------------------------------------------------------------
            #Zuständigen User aus der DB laden (nur aus derselben WG!)
            #Quellen: ChatGPT (Prompt: "Zuständig kommt aus einem datalist-input – wie finde ich den User dazu")
            assigned_user = User.query.filter_by(
                wg_id=user.wg_id,
                username=zustaendig_name
            ).first()
        #--------------------------------------------------------------------------------------------------------------

            #Fehlermeldung, falls der User nicht existiert (sollte nicht passieren, da aus Dropdown gewählt wird)
            #Quellen: ChatGPT (Prompt: "wieso packt er nicht die aufgabe auf die seite, die ich erstellt habe") 
            if not assigned_user:
                flash("WG-Mitglied existiert nicht", "danger")
                return redirect(url_for("putzplan"))
            #Neue Vorlage und Task erstellen, falls noch nicht vorhanden 

            else:
                #------------------------------------------------------------------------------------------------------
                #Isocalendar & Umrechnung, Quelle: https://docs.python.org/3/library/datetime.html
                #Kalenderwoche aus dem von_datum-Feld holen
                kw = form.von_datum.data.isocalendar().week  
                #------------------------------------------------------------------------------------------------------
                #Template erstellen (Plan/Zeitraum), zum Lernen
                #Quellen: ChatGPT (Prompt: (1) "wieso packt er nicht die aufgabe auf die seite, die ich erstellt habe")
                """Man musste natürlich eine Instanz der Klasse erstellen, damit die init-Methode ausgeführt wird und die template_id generiert wird,
                die man für die Erstellung des Tasks braucht. 
                Das war der Hauptgrund, warum es nicht funktioniert hat. (Bei den anderen Seiten dann selber umgesetzt.)"""

                new_template = CleaningTemplate(
                    wg_id=user.wg_id,
                    name=form.aufgabe.data,
                    description=f"KW {kw}: {form.von_datum.data.strftime('%d.%m.%Y')} bis {form.bis_datum.data.strftime('%d.%m.%Y')}",
                    frequency = "weekly",
                    is_active=True
                )
                db.session.add(new_template)
            #--------------------------------------------------------------------------------------------------------------
                #flush() = vorübergehendes Speichern, aber noch kein Commit
                #Quellen: ChatGPT (Prompt-Kontext: Template + Task erstellen; Hinweis zu flush())
                db.session.flush() #Damit new_template.template_id verfügbar ist, bevor commit() aufgerufen wird (für Task)

            #--------------------------------------------------------------------------------------------------------------
                #Neuen Task erstellen mithilfe von der soeben erstellten Vorlage
                #Quellen: ChatGPT (Prompt: (2) "wieso packt er nicht die aufgabe auf die seite, die ich erstellt habe")
                #-> Task speichern (Zuständig = assigned_to)
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
    
    #--------------------------------------------------------------------------------------------------------------------
    #Quellen: Autocomplete in VS Code + Eigenleistung + ChatGPT-Hilfe
    #ChatGPT (Prompt: "Wie filtere ich CleaningTemplate nach wg_id")
    putzplan_eintraege = (CleaningTemplate.query
                          .filter_by(wg_id=user.wg_id, is_active=True)  #Filtern nach wg_id und is_active = True, damit nur aktive Einträge direkt angezeigt werden (standard)
                          .order_by(CleaningTemplate.template_id.desc()) #Sortieren nach template_id absteigend
                          .all()) #Alle Einträge der WG holen
    #--------------------------------------------------------------------------------------------------------------------
    #Quellen: ChatGPT (Prompt: "CleaningTemplate hat kein status attribut, aber CleaningTask hat, was soll ich jetzt machen?")
    tasks = (CleaningTask.query
             .join(CleaningTemplate) # Join mit CleaningTemplate für wg_id
             .filter(CleaningTemplate.wg_id == user.wg_id)  # Filtern nach wg_id
             .all())    #Alle Tasks holen
    
    #---------------------------------------------------------------------------
    #Quellen: ChatGPT (Prompt: HTML-Skript für Fortschrittsbalken)
    #Berechnung des Fortschritts
    total_tasks = len(tasks)
    #Anzahl der abgeschlossenen Tasks berechnen
    completed_tasks = sum(1 for t in tasks if t.status == "completed")
    #Fortschritt in Prozent berechnen, wenn keine gibt, dann 0% und Progressbar bleibt leer
    progress = int((completed_tasks / total_tasks) * 100) if total_tasks else 0

    #---------------------------------------------------------------------------

    return render_template(
        "putzplan.html",
        form=form,
        all_users=all_users,
        putzplan=putzplan_eintraege,
        #Quellen für die unteren 3 Variablen: ChatGPT(Prompt: HTML-Skript für Fortschrittsbalken)
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        progress=progress 
    )

#-----------------------------------------------------------------------------
@app.route("/putzplan/task/<int:task_id>/toggle", methods=["POST"])
@login_required
def toggle_cleaning_task(task_id):
    #task_id aus der URL holen
    task = CleaningTask.query.get_or_404(task_id)
    user = User.query.get(session['user_id'])

    #Sicherstellen, dass der Task zur WG des Users gehört
    if task.template.wg_id != user.wg_id:
        abort(404)

    #--------------------------------------------------------------------------------------------------------------
    #Quellen: ChatGPT (Prompt: warum zeigt er mir completed_at nicht an?)
    #-> completed_at beim Toggle setzen (completed -> datetime.now, open -> None)
    #Status umschalten
    if task.status == "completed":
        task.status = "open"
        task.completed_at = None
    else:
        task.status = "completed"
        task.completed_at = datetime.now()
    #--------------------------------------------------------------------------------------------------------------
    #Speichern in der DB
    db.session.commit()
    return redirect(url_for("putzplan"))

@app.route("/putzplan/task/<int:template_id>/delete", methods=["POST"])
def delete_cleaning_task(template_id):
    #---------------------------------------------------------------------------------------------
    #Quellen: ChatGPT (Prompt: "ich will einfach den eintrag löschen können und ihn von der seite weghaben")
    #-> Problem: Seite rendert aus CleaningTemplate; nur Task löschen lässt Card evtl. bestehen, daher Template löschen (cascade delete in DB sorgt dafür, dass auch Task gelöscht wird)
    user_id = session.get("user_id")
    template = CleaningTemplate.query.get_or_404(template_id)
    user = User.query.get(user_id)
    if template.wg_id != user.wg_id:
        abort(404)
    #---------------------------------------------------------------------------------------------
    #Task
    task = template.tasks[0] if template.tasks else None
    if not task:
        flash("Kein Task gefunden.", "danger")
        return redirect(url_for("putzplan"))
    #---------------------------------------------------------------------------------------------
    # Quellen: (Delete-Policy im Verlauf diskutiert: "nur Zuständiger darf löschen" als Option)
    if task.assigned_to != user_id:
        flash("Nur die zuständige Person kann diese Aufgabe löschen.", "danger")
        return redirect(url_for("putzplan"))
    #---------------------------------------------------------------------------------------------
    db.session.delete(template)
    db.session.commit()
    flash("Aufgabe erfolgreich gelöscht.", "success")
    return redirect(url_for("putzplan"))

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

# Quellen-Kontext:
# - Like-Feature (Route/Toggle + Template-Hinweise) entstand aus Prompt: "ich würde gerne auch likes hinzufügen, wie geht das?"
#   
# - Kommentare/CommentForm + CSRF Debug/Hidden-Tag aus Prompts: CSRF token missing + "kommentarspalte größer machen wie geht das?"
#   
# - Delete-Route + Owner-Check + Button/Delete-Idee aus: (Delete Button + "optional: nur Ersteller darf löschen")

@app.route("/innovationboard/", methods=['GET', 'POST'])
@login_required
def innovation_board():
    user_id = int(session["user_id"])
    
    form = InnovationForm()
    #aktuellen User laden
    user = User.query.filter_by(user_id=user_id).first()

    all_users = User.query.filter_by(wg_id=user.wg_id).all()
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
            flash("Fehler beim Einreichen der Innovation. Bitte überprüfen Sie die Eingaben.", "danger")

    #----------------------------------------------------------------------------------------------------------------------
    #Ideen anzeigen, nach WG filtern, mit User-Relationen laden, absteigend sortieren, alle holen, joinedload(...) für weniger Queries und richtiges Laden der Relationen
    #Quelle: ChatGPT-Verlauf (Query mit joinedload für Creator + optional Comments->User)
    ideas = (Idea.query
             .filter_by(wg_id=user.wg_id)   
             .options(joinedload(Idea.creator)) 
             .order_by(Idea.created_at.desc())
             .all())
    #---------------------------------------------------------------------------------------------------------------------
    return render_template("innovationboard.html", form=form, all_users=all_users,ideas=ideas, comment_form=CommentForm())

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

#post route, da das Formular data ändert (löschen)
@app.route("/innovation_board/idea/<int:idea_id>/delete", methods=["POST"])
@login_required
def delete_idea(idea_id):

    #--------------------------------------------------------------------------------------------------------------
    #aktuellen User laden und konkrete Idee laden, prüfen ob der User der Ersteller der Idee ist, wenn nicht -> 403 und Flashmeldung
    #Bezug auf creator: Beziehung in Idea Model
    #Quelle: ChatGPT-Verlauf (Delete-Route, Owner-Check: "optional: nur Ersteller darf löschen")
    idea = Idea.query.get_or_404(idea_id)
    user_id = int(session["user_id"])
    user = User.query.get(user_id)

    if idea.wg_id != user.wg_id:
        abort(404)

    #Owner-Regel: Nur der Ersteller der Idee darf sie löschen
    if idea.created_by != user_id:
        flash("Sie können nur Ihre eigenen Ideen löschen.", "danger")
        return redirect(url_for("innovation_board"))
    
    #--------------------------------------------------------------------------------------------------------------
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
    #Überprüfen, ob der User die Idee bereits geliked hat
    existing = Idea_Like.query.filter_by(idea_id=idea_id, user_id=user_id).first() #first() gibt None zurück, wenn kein Eintrag gefunden wurde
    user = User.query.get(user_id)
    idea = Idea.query.get_or_404(idea_id)
    if idea.wg_id != user.wg_id:
        abort(404)

    #-------------------------------------------------------------------------------------------------------------------------------------
    #Quelle: ChatGPT-Verlauf (Prompt: "ich würde gerne auch likes hinzufügen, wie geht das?" -> Toggle-Route + Logik)
    #Standard-Toggle: existiert -> unlike, sonst like, plus IntegrityError rollback
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

    #--------------------------------------------------------------------------------------------------------------

    return redirect(url_for("innovation_board"))

#Post route, da das Formular data ändert (neuer Kommentar erstellen)
@app.route("/ideas/<int:idea_id>/comment", methods=["POST"])
@login_required
def post_comment(idea_id):

    #--------------------------------------------------------------------------------------------------------------
    #Quellen: ChatGPT-Verlauf+ Autocomplete zu Anfang (Umstieg auf echtes WTForms CommentForm + validate_on_submit + form.content.data)
    user_id = int(session["user_id"])
    user = User.query.get(user_id)
    idea = Idea.query.get_or_404(idea_id)
    if idea.wg_id != user.wg_id:
        abort(404)
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
                flash("Kommentar darf nicht leer sein.", "danger")
        

    return redirect(url_for("innovation_board"))

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

#Get und Post route, da das Formular data abruft und ändert (neue Aktivität erstellen) 
@app.route("/activityboard/", methods=["GET", "POST"])
@login_required
def activity_board():

    #aktuellen User laden
    user = User.query.get(session["user_id"])

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
                date_to=form.date_to.data,
                location=form.location.data,
                max_participants=form.max_participants.data,
                created_at=db.func.now()
            )
            #Hinzufügen und Speichern in der DB
            db.session.add(new_activity)
            db.session.commit()
            return redirect(url_for("activity_board"))
    #---------------------------------------------------------------------------------------------------------------
    #Aktivitäten anzeigen, nach WG filtern, mit User-Relationen laden, absteigend sortieren, alle holen, joinedload(...) für weniger Queries und richtiges Laden der
    #Relationen
    # Quellen: ChatGPT (Prompt: "ich sehe die user nicht, die beigetreten sind")
        #+ (Prompt: "wie zeige ich hier richtige alle namen der activity participants an")
        #-> Lösung: participants/creator sauber eager-loaden, damit Template Teilnehmerliste zuverlässig rendern kann.
    activities = (Activity.query
        .filter_by(wg_id=wg_id)
        .options(joinedload(Activity.creator), joinedload(Activity.participants))
        .order_by(Activity.created_at.desc())
        .all())
    
    #----------------------------------------------------------------------------------------------------------------
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

    # Sicherstellen, dass die Aktivität zur WG des Users gehört
    if activity.wg_id != user.wg_id:
        abort(404)

    #----------------------------------------------------------------------------------------------------------------
    #Prüfen, ob der User bereits Teilnehmer ist, damit er/sie nicht doppelt beitreten kann
    #Quellen: ChatGPT (Prompt: "ich sehe die user nicht, die beigetreten sind")
    if user in activity.participants:
        flash("Du nimmst bereits teil.", "danger")
        return redirect(url_for("activity_board"))
    
    #----------------------------------------------------------------------------------------------------------------
    #Prüfen, ob die maximale Teilnehmerzahl erreicht ist, len(activity.participants) gibt die aktuelle Anzahl der Teilnehmer zurück
    #Quellen: ChatGPT (Prompt: "wie würde ich rangehen, wenn ich ein optionales maximale teilnehmer zahl feld einfügen möchte")
    if activity.max_participants and len(activity.participants) >= activity.max_participants:
        flash("Die Aktivität ist bereits voll.", "danger")
        return redirect(url_for("activity_board"))
    
    #----------------------------------------------------------------------------------------------------------------
    #User zur Teilnehmerliste hinzufügen
    #Quellen: ChatGPT (Prompt: "kann man das auch ohne activityParticipant machen?")
    """Antwort: Liste benutzen, da Beziehung in Activity Model als participants definiert ist, was eine Liste von User-Objekten zurückgibt, die an der Aktivität teilnehmen"""
    activity.participants.append(user)

#----------------------------------------------------------------------------------------------------------------
    db.session.commit()
    flash("Du bist beigetreten!", "success")    

    return redirect(url_for("activity_board"))

#post route, da das Formular data ändert (aktualisiert) 
@app.route("/activity/<int:activity_id>/leave_activity", methods=["POST"])
@login_required
def leave_activity(activity_id):

    #aktuelle user_id holen
    user_id = int(session["user_id"])  
    
    #User aus user_id und Aktivität laden
    user = User.query.get(user_id)  
    activity = Activity.query.get_or_404(activity_id)

    if activity.wg_id != user.wg_id:
        abort(404)
#----------------------------------------------------------------------------------------------------------------
    #Prüfen, ob der User tatsächlich Teilnehmer ist
    #Quellen: ChatGPT (Prompt: "wie kann ich nur die activities leaven, in denen ich drin bin?")
    if user not in activity.participants:
        flash("Du nimmst nicht teil.", "danger")
        return redirect(url_for("activity_board"))

    # User aus der Teilnehmerliste entfernen
    activity.participants.remove(user)
#----------------------------------------------------------------------------------------------------------------
    db.session.commit()
    flash("Du hast die Aktivität verlassen.", "success")    

    return redirect(url_for("activity_board"))

@app.route("/activity/<int:activity_id>/delete_activity", methods=["POST"])
@login_required
def delete_activity(activity_id):
    
    #aktuellen User laden und konkrete Aktivität laden
    current_user_id = int(session["user_id"])
    activity = Activity.query.get_or_404(activity_id)

    #----------------------------------------------------------------------------------------------------------------
    # Prüfen, ob der aktuelle User der Ersteller der Aktivität ist, creator ist die Beziehung in Activity Model
    # Quellen: ChatGPT (Prompt: "wie mache ich, dass der user nur seine eigenen aktivitäten löschen kann?")
    if activity.created_by != current_user_id:
        flash("Sie können nur Ihre eigenen Aktivitäten löschen.", "danger")
        return redirect(url_for("activity_board"))
    #----------------------------------------------------------------------------------------------------------------
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
    
    #  aktuelle WG ID für new_item
    wg_id = current_user.wg_id 

    # POST: Item speichern 
    if request.method == "POST":

        if form.validate_on_submit():

        #------------------------------------------------------------------------------------------------------------------------
            # Quellen: ChatGPT (Prompt: "u.user_id (user_id ist \"any\") (Bugfix)
            assigned_to = current_user.user_id
        #------------------------------------------------------------------------------------------------------------------------
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
            flash("Fehler beim Hinzufügen. Bitte Eingaben prüfen.", "danger")
    #------------------------------------------------------------------------------------------------------------------
    #Quelle: Auto-Completion + ChatGPT Prompt: "mach bitte dass es funktioniert" (Bugfix)
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
    #------------------------------------------------------------------------------------------------------------------
    #Rendern der Seite mit Formular und Items
    return render_template("einkaufsplan.html", form=form, shopping_items=shopping_items)
     

# Delete Einkaufs Item
@app.route("/einkaufsplan/item/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_shopping_item(item_id):

    # Laden des Items
    item = ShoppingItem.query.get_or_404(item_id)
    user = User.query.get(session['user_id'])
    user_id = int(session["user_id"])

    current_user = User.query.get(user_id) if user_id else None
    if item.wg_id != user.wg_id:
        abort(404)

    if item.assigned_to != current_user.user_id:
        flash("Nur die zuständige Person kann diesen Artikel löschen.", "danger")
        return redirect(url_for("einkaufsplan"))
    
    #aus der DB löschen und commiten
    db.session.delete(item)
    db.session.commit()
    flash("Artikel erfolgreich gelöscht.", "success")
    return redirect(url_for("einkaufsplan"))

#------------------------------------------------------------------------------------------------------------------------------------
#Quelle: ChatGPT (Prompt: "wie würde eine funktion aussehen, die das datum in google calendar oder apple calendar macht?")

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
    user = User.query.get(session['user_id'])
    # Aktivität laden
    activity = Activity.query.get_or_404(activity_id)
    if activity.wg_id != user.wg_id:
        abort(404)

    # ICS erstellen (instanzieren)
    ics = build_ics(
        uid=f"activity-{activity.activity_id}@wgplanner",
        title=activity.title,
        start_dt=activity.date,     # oder activity.time
        end_dt=activity.date_to,       # ggf. + timedelta(hours=2)
        description=activity.description or "",
        location=activity.location or "",
    )
    # ICS als Download zurückgeben
    return Response(
        ics,
        mimetype="text/calendar",
        headers={"Content-Disposition": f'attachment; filename="activity-{activity_id}.ics"'}
    )

#---------------------------------------------------------------------------------------------------------------------------------------------

#Quellen: Autocomplete (Eigenleistung) + Anlehnung an: https://hwrberlin.github.io/fswd/fswd-intro.html#5-bonus-deliver-json-instead-of-html-to-the-web-server
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


