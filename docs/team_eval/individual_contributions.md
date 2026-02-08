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
- `app.py`: Zeilen: 290-997 (Ende)
- **Putzplan**
  - Ganze `putzplan.html`
  - in `app.py` - für den Putzplan zuständige Funktionen & Routes 
    - `putzplan()` (Zeilen 288-405)
    - `toggle_cleaning_task(task_id)` (Zeilen 408-432)
    - `delete_cleaning_task(template_id)` (Zeilen 434-459)

- **InnovationBoard**
  - Ganze `innovationboard.html`
  - in `app.py` - für das InnovationBoard zuständige Funktionen & Routes 
    - `innovation_board()` (Zeilen 470-512)
    - `delete_idea()` (Zeilen 517-542)
    - `toggle_like()` (Zeilen 545-575)
    - `post_comment()` (Zeilen 578-614)

- **ActivityBoard**
  - Ganze `activityboard.html`
  - in `app.py` - für das ActivityBoard zuständige Funktionen & Routes 
    - `activity_board()` (Zeilen 619-668)
    - `join_activity(activity_id)` (Zeilen 671-709)
    - `leave_activity(activity_id)` (Zeilen 712-738)
    - `delete_activity(activity_id)` (Zeilen 740-759)
    - `google_calendar_url(title, start_dt, end_dt, details="", location="")` (Zeilen 851- 864)
    - `dt_to_ics(dt)` (Zeilen 867-870)
    - `build_ics(uid, title, start_dt, end_dt, description="", location="")` (873-888)
    - `activity_ics(activity_id)` (Zeilen 892-915)

- **Einkaufsliste**
  - Ganze `einkaufplan.html`
  - in `app.py` - für die Einkaufsliste zuständige Funktionen & Routes
    - `einkaufsplan()` (Zeilen 762-818)
    - `delete_shopping_item(item_id)` (Zeilen822-843)

- **Im Dashboard Button "WG-Daten-Exportieren" (WG JSON-Export)**
  - Im `dashboard.html` Zeilen 20-22
  - in `app.py` - für den WG Datenexport zuständige Funktion & Route 
  - `export_wg_json()` (Zeilen 921-995)

- `instance/run_sql.py` & die restlichen .sql Files

- **In Database `db.py` folgende Spalten:**
  - `Activitiy`: `participants` (Zeilen 112-116)
  - `User`: `joined_activities` (Zeilen 39-43)
  - Association Table: `activity_participants` (Zeilen 14-18)

- **In `forms.py` (Zeilen 54-87):**
  - `PutzplanForm(FlaskForm)` (Zeilen 54-60)
  - `InnovationForm(FlaskForm)` (Zeilen 64-68)
  - `CommentForm(FlaskForm)` (Zeilen 70-72)
  - `ActivityForm(FlaskForm)` (Zeilen 75-82)
  - `Einkaufsform(FlaskForm)` (Zeilen 84-87)

- **`design_decisions.md` (nur geschrieben, zusammen entschieden)**

---

## Susann (github.com/susi-hwr): 

- **Database (DB)**
  - Implementierung der Datenbank in `db.py` (Zeilen 1-152)
  - Außer die Spalten:
    - `Activitiy`: `participants` (Zeilen 112-116)
    - `User`: `joined_activities` (Zeilen 39-43)
    - Association Table: `activity_participants` (Zeilen 14-18)
  - Definition aller Datenbankmodelle (SQLAlchemy):
    - `User` (Zeilen 20-36)
    - `Wg` (Zeilen 45-57)
    - `ShoppingItem` (Zeilen 59-71)
    - `CleaningTemplate` (Zeilen 73-84)
    - `CleaningTask` (Zeilen 86-96)
    - `Activity` (Zeilen 98-118)
    - `Idea` (Zeilen 122-137)
    - `Idea_Comment` (Zeilen 139-148)
    - `Idea_Like` (Zeilen 150-157)
  - Umsetzung aller relevanten Beziehungen

- **Authentifizierung (Login/Logout)**
  - Ganze `login.html` 
  - Implementierung der Login- und Logout-Funktionalität in `app.py`
    - `login()` (Zeilen 74-98)
      - Benutzeranmeldung mit Formularvalidierung
      - Überprüfung von Benutzername und Passwort
      - Session-Handling über `session['user_id']`
    - `logout()` (Zeilen 102-105)
      - Abmelden durch Zurücksetzen der Session

- **Benutzerregistrierung**
  - Ganze `register.html`
  - in `app.py`: 
    - `register()` (Zeilen 109-139)
      - Registrierung neuer Benutzer über Formular
      - Prüfung auf eindeutigen Benutzernamen und E-Mail-Adresse
      - Passwort-Hashing vor Speicherung in der Datenbank
      - Automatisches Login durch Setzen der Session nach erfolgreicher Registrierung

- **WG-Erstellung & Beitritt**
  - Ganze `welcome.html` 
  - Ganze `create_wg.html` 
  - Ganze `join_wg.html` 
  - in `app.py`:
    - `create_or_join_wg()` (Zeilen 143-149)
      - Begrüßung des eingeloggten Benutzers
      - Anzeige des Benutzernames auf der Welcome-Seite
    - `create_wg()` (Zeilen 152-175)
      - Erstellung einer neuen WG mit eindeutiger Einladungscode-Generierung
      - Speicherung der WG in der Datenbank
      - Validierung des WG-Namens und Rückmeldung via Flash-Messages
    - `join_wg()` (Zeilen 179-200)
      - Beitritt zu einer bestehenden WG über Einladungscode
      - Prüfung zu einer bestehenden WG über Einladungscode
      - Speicherung der Änderung in der Datenbank und Rückmeldung via Flash-Messages

- **Dashboard**
  - `dashboard.html` (Zeilen 1-215, außer Zeilen 20-22)
  - in `app.py`:
    - `dashboard()` (Zeilen 203-225)
      - Anezeige personalisierter Übersichtsseite für eingeloggte Benutzer
      - Zählt offene Putzaufgaben, neue Ideen, kommende Events und Einkaufsposten
      - Generiert wichtige Hinweise für Aufgaben, Einkäufe und Events
      - Erstellt Activity-Box mit letzten Aktivitäten (Putzaufgaben, Einkaufsliste, Ideen, Events)
      - Anzeige aller WG-Mitglieder und aktuellem Datum
      - Übergabe aller Daten an `dashboard.html`zur dynamischen Darstellung

- **In `forms.py` (Zeilen 12-51)**
  - `UserExistsValidator` (Zeilen 12-19)
  - `LoginForm(FalskForm)` (Zeilen 21-30)
  - `RegisterForm(FlaskForm)` (Zeilen 32-51)
  - Zeilen 5-10 zusammen

{: .fs-2 }
Last build: {{ site.time | date: '%d %b %Y, %R%:z' }}