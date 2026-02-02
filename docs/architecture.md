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
- **Session-basierte Authentifizierung:** 
  Nach Login wird `session["user_id"]` gesetzt; ein `login_required` Decorator schützt Routes.
- **Validation über WTForms:** `form.validate_on_submit()` → Jegliche Eingaben werden serverseitig geprüft.
- **Multi-Tenancy (WG-Scoping) über `wg_id` [(kritische Designentscheidung)]({{ site.baseurl }}/design_decisions.html):**  
  Alle relevanten Datenobjekte hängen an einer WG; **jede** Query/Änderung wird auf `current_user.wg_id` begrenzt → verhindert Cross-WG Datenzugriffe.

### High-Level Visualisierung des allgemeinen Flows mit externen Akteuren:
![SimpleFlow](assets/images/architecture/HappyWG%20SSR%20App%20ICS%20Flow-2026-02-02-094043.png)

### Visualisierung der Architektur
![AppArchitectureVisual](assets/images/architecture/HappyWG%20SSR%20App%20ICS%20Flow-2026-02-02-101303.png)





{: .fs-2 }
Last build: {{ site.time | date: '%d %b %Y, %R%:z' }}