---
layout: default
title: Individual Contributions
parent: Team Evaluation
nav_order: 3
---

# Individual Contributions

**(!)** Auskunft über die Funktionen in [Reference]({{ site.baseurl }}/technical-docs/reference.html).

## Marcel (github.com/MxrsExe): 
- Host von dieser GitHub Repository (Happy WG)
- Putzplan
  - Ganze `putzplan.html`
  - in `app.py` - für den Putzplan zuständige Funktionen & Routes 
    - `putzplan()` 
    - `toggle_cleaning_task(task_id)` 
    - `delete_cleaning_task(template_id)` 
- InnovationBoard
  - Ganze `innovationboard.html`
  - in `app.py` - für das InnovationBoard zuständige Funktionen & Routes 
    - `innovation_board()` 
    - `delete_idea()` 
    - `toggle_like()` 
    - `post_comment()` 
- ActivityBoard
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
- Einkaufsliste
  - Ganze `einkaufplan.html`
  - in `app.py` - für die Einkaufsliste zuständige Funktionen & Routes
    - `einkaufsplan()`
    - `delete_shopping_item(item_id)`
- Im Dashboard Button "WG-Daten-Exportieren" (WG JSON-Export)
  - Im `dashboard.html` Zeilen 20-22
  - in `app.py` - für den WG Datenexport zuständige Funktion & Route 
  - `export_wg_json()`
- `instance/run_sql.py` & die restlichen .sql Files
- In Database `db.py` folgende Spalten:
  - `Activitiy`: `participants`
  - `User`: `joined_activities`
  - Association Table: `activity_participants`
- `forms.py` (Zeilen 50-84): 
  - `PutzplanForm(FlaskForm)`
  - `InnovationForm(FlaskForm)`
  - `CommentForm(FlaskForm)`
  - `ActivityForm(FlaskForm)`
  - `Einkaufsform(FlaskForm)`
- `design_decisions.md` (nur geschrieben, zusammen entschieden)

## Susann

- **Database (DB)**

