---
layout: default
title: Architecture
parent: Technical Docs
nav_order: 1
---

# Architecture

## Overview

**HappyWG** ist eine Flask-Web-App für Wohngemeinschaften (WGs), die alltägliche Organisation an einem Ort bündelt: **Putzplan**, **Einkaufsliste**, **Activityboard** (Events) und ein **Innovationboard** (Ideen).  
Ziel ist ein leichtgewichtiger "WG-Hub", der ohne komplexes Frontend auskommt und trotzdem sauber strukturiert, sicher und erweiterbar mit neuen Features bleibt.

Aus **Entwicklerperspektive** fokussiert sich die Web-App auf **simple und robuste server-side Flows**.

Für die visuelle Orientierung in der App empfehlen wir die [Customer Journey]({{ site.baseurl }}/value_proposition.html#customer-journey).

### Was die Web-App macht
- **Login und Registrierung:** Account anlegen und sich mit diesem einloggen.
- **WG-Onboarding:** WG erstellen oder per zufallsgeneriertem **Invite-Code** beitreten.
- **Dashboard**: Überblick über letzte Aktivitäten innerhalb der WG, persönliche ToDos bzw. Erinnerungen, Anzahl offener Putzaufgaben, anstehende Aktivitäten, (neue) Ideen von WG-Mitgliedern und offene Einkäufe.
- **Putzplan:** Putzaufgaben anlegen, einem WG-Mitglied zuweisen, Status (*open/completed*) togglen bzw. durchstreichen und bestätigen und Fortschritt anzeigen.
- **Innovationboard:** Ideen posten, kommentieren, liken (leichtes Collaboration-Feature). 
- **Activityboard:** Events erstellen, beitreten/abmelden, maximale Teilnehmeranzahl prüfen, **.ics Export** für den Kalender-Import.
- **Einkaufsliste:** Items hinzufügen, optional zuständig zuweisen, transparent für die gesamte WG.


### Wie die Web-App das erreicht (Architektur & Design)
- **Server-side Rendering (SSR)** mit Flask + Jinja2:
  Interaktionen, beispielsweise create, toggle, join/leave, delete, laufen überwiegend über **POST + Redirect** (PRG Pattern)
- **SQLAlchemy ORM** als Datenzugriffsschicht:  
  Models bilden Tabellen/Beziehungen ab, Queries werden als Python-Objekte formuliert.
- **ORM-Instanzierung & Persistenz:** Anschließend zu **SQLAlchemy ORM:** beispielhafte Erstellung der Objekt-Instanzen durch `new_activity = Activity(...)`, dann `db.session.commit()`.
- **Performance/Eager Loading:** Beispielsweise `.options(joinedload(Activity.creator), joinedload(Activity.participants))` → vermeidet N+1 Queries im Template (alle Daten werden mittels einer einzigen Query geladen).
- **Multi-Tenancy (WG-Scoping) über `wg_id` [(kritische Designentscheidung)]({{ site.baseurl }}/design_decisions.html):**  
  Alle relevanten Datenobjekte hängen an einer WG; **jede** Query/Änderung wird auf `current_user.wg_id` begrenzt → verhindert Cross-WG Datenzugriffe.
- **Session-basierte Authentifizierung:** 
  Nach Login wird `session["user_id"]` gesetzt; ein `login_required` Decorator schützt Routes.
- **Validation über WTForms:** `form.validate_on_submit()` → Jegliche Eingaben werden serverseitig geprüft.
- **Kalender-Export:** Activities lassen sich als **.ics** herunterladen (serverseitig generiert, `text/calendar`) und in gängige Kalender importieren.
- **Design:** Für das Design auf den Webseiten wird größtenteils Bootstrap (Klassen) genutzt. Im ActivityBoard gibt es zusätzlich custom CSS. 

### High-Level Visualisierung des allgemeinen Flows mit externen Akteuren:
![SimpleFlow](assets/images/architecture/HappyWG%20SSR%20App%20ICS%20Flow-2026-02-02-094043.png)

### Visualisierung der Architektur
![AppArchitectureVisual](assets/images/architecture/HappyWG%20SSR%20App%20ICS%20Flow-2026-02-02-101303.png)

## Codemap

**`app.py`** (Routes / Controllers)

- Authorisierung & Session Flow: `login`, `register`, `logout`, Wrapper `login_required`
- WG Flow - WG erstellen: `create_or_join_wg`, `create_wg`, `generate_unique_code` & beitreten: `join_wg`
- Feature Routes:
  - `/dashboard/` - Zähler & Aggregationen
  - `/putzplan/` - Putzaufgabe erstellen + Aufgaben auflisten + Fortschritt
  - `/putzplan/task/<id>/toggle` - Aufgaben markieren bzw. durchstreichen, um sie als fertig oder offen zum markieren.
    - `/putzplan/task/<int:template_id>/delete` - Aufgabe löschen
  - `/innovationboard/` - create ideas, like, comment, delete
    - `/innovation_board/idea/<int:idea_id>/delete` - Idee löschen
    - `/ideas/<int:idea_id>/like` - Idee liken
    - `/ideas/<int:idea_id>/comment` - Idee kommentieren
  - `/activityboard/` - Aktivitäten erstellen, listen, (beitreten/verlassen, löschen)
    - `/activity/<int:activity_id>/join_activity`- Aktivität beitreten
    - `/activity/<int:activity_id>/leave_activity` - Aktivität verlassen
    - `/activity/<int:activity_id>/delete_activity` - Aktivität löschen
    - `/activities/<int:activity_id>/ics` - Aktivitäten als Kalender (`.ics`) exportieren.
  - `/einkaufsplan/` - Erstellen, auflisten und löschen von Einkaufsprodukten
    - `/einkaufsplan/item/<int:item_id>/delete` - Einkaufsprodukt löschen

**`db.py`** (Models & Persistenz, siehe [DataModel]({{ site.baseurl }}/data_model.html))
- `Wg`, `User`
- Putzplan: `CleaningTemplate`, `Cleaning_Task`
- InnovationBoard: `Idea`, `Idea_Comment`, `Idea_Like`
- ActivityBoard: `Activity` + `ACTIVITY_PARTICIPANTS` (n zu m)
- Einkaufsliste: `ShoppingItem`
- 
**`docs/forms.py` (WTForms)**
- Forms and Eingabevalidierung:
  `LoginForm`, `RegisterForm`, `PutzplanForm`, `EinkaufsplanForm`, `ActivityForm`, `InnovationForm`, `CommentForm`

**`templates/` (views)**
- Jinja2 Templates für alle Seiten (Login, Registrierung, Dashboard, Boards, Modals etc.)
- Geteiltes Layout besitzt Flash Messages und Content-Blocks aus `base.html`.
  
**`assets/`**
- Dokumentationsbilder und Data Model






{: .fs-2 }
Last build: {{ site.time | date: '%d %b %Y, %R%:z' }}