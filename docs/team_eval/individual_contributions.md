---
layout: default
title: Individual Contributions
parent: Team Evaluation
nav_order: 3
---

# Individual Contributions

---

**(!)** Auskunft über die Funktionen in [Reference]({{ site.baseurl }}/technical-docs/reference.html).

---

<details open markdown="block">
{: .text-delta }
<summary>Inhaltsverzeichnis</summary>
+ ToC
{: toc }
</details>

---

## Marcel (github.com/MxrsExe): 
- Host von dieser GitHub Repository (Happy WG)

- **Putzplan**
  - Ganze `putzplan.html`
  - in `app.py` - für den Putzplan zuständige Funktionen & Routes 
    - `putzplan()` 
    - `toggle_cleaning_task(task_id)` 
    - `delete_cleaning_task(template_id)` 

- **InnovationBoard**
  - Ganze `innovationboard.html`
  - in `app.py` - für das InnovationBoard zuständige Funktionen & Routes 
    - `innovation_board()` 
    - `delete_idea()` 
    - `toggle_like()` 
    - `post_comment()` 

- **ActivityBoard**
  - Ganze `activityboard.html`
  - in `app.py` - für das ActivityBoard zuständige Funktionen & Routes 
    - `activity_board()` 
    - `join_activity(activity_id)` 
    - `leave_activity(activity_id)` 
    - `delete_activity(activity_id)` 
    - `google_calendar_url(title, start_dt, end_dt, details="", location="")` 
    - `dt_to_ics(dt)`
    - `build_ics(uid, title, start_dt, end_dt, description="", location="")`
    - `activity_ics(activity_id)`

- **Einkaufsliste**
  - Ganze `einkaufplan.html`
  - in `app.py` - für die Einkaufsliste zuständige Funktionen & Routes
    - `einkaufsplan()`
    - `delete_shopping_item(item_id)`

- **Im Dashboard Button "WG-Daten-Exportieren" (WG JSON-Export)**
  - Im `dashboard.html` Zeilen 20-22
  - in `app.py` - für den WG Datenexport zuständige Funktion & Route 
  - `export_wg_json()`

- `instance/run_sql.py` & die restlichen .sql Files

- **In Database `db.py` folgende Spalten:**
  - `Activitiy`: `participants`
  - `User`: `joined_activities`
  - Association Table: `activity_participants`

- **In `forms.py` (Zeilen 50-84):**
  - `PutzplanForm(FlaskForm)`
  - `InnovationForm(FlaskForm)`
  - `CommentForm(FlaskForm)`
  - `ActivityForm(FlaskForm)`
  - `Einkaufsform(FlaskForm)`

- **`design_decisions.md` (nur geschrieben, zusammen entschieden)**

---

## Susann (github.com/susi-hwr): 

- **Database (DB)**
  - Implementierung der Datenbank in `db.py` (Zeilen 1-152)
  - Außer die Spalten:
    - `Activitiy`: `participants` (Zeilen 106-113)
    - `User`: `joined_activities` (Zeilen 34-38)
  - Definition aller Datenbankmodelle (SQLAlchemy):
    - `User`
    - `Wg`
    - `ShoppingItem`
    - `CleaningTemplate`
    - `CleaningTask`
    - `Activity`
    - `Idea`
    - `Idea_Comment`
    - `Idea_Like`
  - Umsetzung aller relevanten Beziehungen

- **Authentifizierung (Login/Logout)**
  - Ganze `login.html`(Zeilen 1-36)
  - Implementierung der Login- und Logout-Funktionalität in `app.py`
    - `login()`
      - Benutzeranmeldung mit Formularvalidierung
      - Überprüfung von Benutzername und Passwort
      - Session-Handling über `session['user_id']`
    - `logout()`
      - Abmelden durch Zurücksetzen der Session

- **Benutzerregistrierung**
  - Ganze `register.html`(Zeilen 1-91)
  - in `app.py`: 
    - `register()`
      - Registrierung neuer Benutzer über Formular
      - Prüfung auf eindeutigen Benutzernamen und E-Mail-Adresse
      - Passwort-Hashing vor Speicherung in der Datenbank
      - Automatisches Login durch Setzen der Session nach erfolgreicher Registrierung

- **WG-Erstellung & Beitritt**
  - Ganze `welcome.html` (Zeilen 1-72)
  - Ganze `create_wg.html` (Zeilen 1-34)
  - Ganze `join_wg.html` (Zeilen 1-47)
  - in `app.py`:
    - `create_or_join_wg()`
      - Begrüßung des eingeloggten Benutzers
      - Anzeige des Benutzernames auf der Welcome-Seite
    - `create_wg()`
      - Erstellung einer neuen WG mit eindeutiger Einladungscode-Generierung
      - Speicherung der WG in der Datenbank
      - Validierung des WG-Namens und Rückmeldung via Flash-Messages
    - `join_wg()`
      - Beitritt zu einer bestehenden WG über Einladungscode
      - Prüfung zu einer bestehenden WG über Einladungscode
      - Speicherung der Änderung in der Datenbank und Rückmeldung via Flash-Messages

- **Dashboard**
  - `dashboard.html` (Zeilen 1-215, außer Zeilen 20-22)
  - in `app.py`:
    - `dashboard()`
      - Anezeige personalisierter Übersichtsseite für eingeloggte Benutzer
      - Zählt offene Putzaufgaben, neue Ideen, kommende Events und Einkaufsposten
      - Generiert wichtige Hinweise für Aufgaben, Einkäufe und Events
      - Erstellt Activity-Box mit letzten Aktivitäten (Putzaufgaben, Einkaufsliste, Ideen, Events)
      - Anzeige aller WG-Mitglieder und aktuellem Datum
      - Übergabe aller Daten an `dashboard.html`zur dynamischen Darstellung

- **In `forms.py` (Zeilen 9-48)**
  - `UserExistsValidator`
  - `LoginForm(FalskForm)`
  - `RegisterForm(FlaskForm)`
  - Zeilen 1-7 zusammen

{: .fs-2 }
Last build: {{ site.time | date: '%d %b %Y, %R%:z' }}