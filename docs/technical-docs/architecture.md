---
layout: default
title: Architecture
parent: Technical documentation
nav_order: 1
---

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

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
- **Performance/Eager Loading:** Beispielsweise `.options(joinedload(Activity.creator), joinedload(Activity.participants))` → vermeidet [N+1](https://www.stefan-goebel.com/2018/was-ist-das-n1-query-problem/) Queries im Template (alle Daten werden mittels einer einzigen Query geladen).
- **Multi-Tenancy (WG-Scoping) über `wg_id` [(kritische Designentscheidung)]({{ site.baseurl }}/design_decisions.html):**  
  Alle relevanten Datenobjekte hängen an einer WG; **jede** Query/Änderung wird auf `current_user.wg_id` begrenzt → verhindert Cross-WG Datenzugriffe.
- **Session-basierte Authentifizierung:** 
  Nach Login wird `session["user_id"]` gesetzt; ein `login_required` Decorator schützt Routes.
- **Validation über WTForms:** `form.validate_on_submit()` → Jegliche Eingaben werden serverseitig geprüft.
- **Kalender-Export:** Activities lassen sich als **.ics** herunterladen (serverseitig generiert, `text/calendar`) und in gängige Kalender importieren.
- **Design:** Für das Design auf den Webseiten wird größtenteils Bootstrap (Klassen) genutzt. Im ActivityBoard gibt es zusätzlich custom CSS. 

### High-Level Visualisierung des allgemeinen Flows mit externen Akteuren (Mermaid):
![SimpleFlow]({{ site.baseurl }}/assets/images/architecture/HappyWG%20SSR%20App%20ICS%20Flow-2026-02-02-094043.png)

### Visualisierung der Architektur (Mermaid)
![AppArchitectureVisual]({{ site.baseurl }}/assets/images/architecture/HappyWG%20SSR%20App%20ICS%20Flow-2026-02-02-101303.png)

### Tech-Stack
- **Backend:** Python, Flask
- **Templating:** Jinja2
- **DB/ORM:** SQLite (dev) + SQLAlchemy 
- **Forms/Validation:** Flask-WTF / WTForms
- **UI:** Bootstrap (CSS), no-JS Interaktionen (POST + Redirect)
- **Kalenderexport:** iCalendar (.ics)

---

## Codemap

**High-Level Codemap-Visualisierung (Mermaid)**
![ComponentDiagram]({{ site.baseurl }}/assets/images/architecture/HappyWG%20SSR%20App%20ICS%20Flow-2026-02-02-122120.png)

**(Routes / Controllers)`app.py`** 

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

**Models & Persistenz: `db.py`** (siehe [DataModel]({{ site.baseurl }}/data_model.html))
- `Wg`, `User`
- Putzplan: `CleaningTemplate`, `Cleaning_Task`
- InnovationBoard: `Idea`, `Idea_Comment`, `Idea_Like`
- ActivityBoard: `Activity` + `ACTIVITY_PARTICIPANTS` (n zu m)
- Einkaufsliste: `ShoppingItem`

**WTForms: `docs/forms.py`**
- Forms and Eingabevalidierung:
  `LoginForm`, `RegisterForm`, `PutzplanForm`, `EinkaufsplanForm`, `ActivityForm`, `InnovationForm`, `CommentForm`

**Views: `templates/`**
- UI: Jinja2 Templates für alle Seiten (Login, Registrierung, Dashboard, Boards, Modals etc.)
- Geteiltes Layout besitzt Flash Messages und Content-Blocks aus `base.html`.
  
**`assets/`**
- Dokumentationsbilder und Data Model

---

## Cross-Cutting Concerns

### "Multi-tenancy" / Datenisolation (wg_id als Scope für alle Queries)
Wie bereits erwähnt, ist diese App dazu gedacht, dass es mehrere WGs ("tenants") geben darf. Alle Domain-Objekte müssen **einer** WG zugeordnet werden. Über die `wg_id` muss also der Zugriff durch `user.wg_id` begrenzt werden. Dies verhindert Cross-WG Datenlecks und stellt eine **[(kritische Designentscheidung)]({{ site.baseurl }}/design_decisions.html)** dar.

Praktische Regel:
-**Jede** CRUD-Operation muss sich zwangsläufig prüfen, ob das Objekt Teil der spezifischen WG ist.
- Sollte ein Objekt indirekt zu einem anderen Objekt gehören (Bsp. `CleaningTask -> CleaningTemplate -> wg_id`), sollte man einen Join- oder Relationship-Check ausführen.

![MultiTenancy]({{ site.baseurl }}/assets/images/architecture/HappyWG%20SSR%20App%20ICS%20Flow-2026-02-02-134844.png)

### Autorisierungsmodell (wer darf was ändern?)

Dies stellt eine [Designentscheidung]({{ site.baseurl }}/design_decisions.html#02-authorization-modell) dar.

Verschiedene Features haben unterschiedliche Ownership-Regeln:
- **Activities:** In der Regel darf nur created_by (Ersteller) eine Aktivität löschen.
- **Putzplan:** Nur die **zuständige Person** (`assigned_to`) darf Aufgaben löschen/abschließen (abhängig von der gewählten Policy)
- **Ideen:** Nur der Ersteller darf Ideen löschen; alle WG-Mitglieder dürfen liken & kommentieren.

Diese Regeln beeinflussen sowohl die Backend-Prüfungen in den Routes als auch welche UI-Buttons/Controls angezeigt werden.

### SSR + POST-Aktionen

Um Komplexität gering zu halten und die UX vorhersehbar zu machen:
- Die meisten Interaktionen laufen über einfache Formulare (`POST`) mit anschließendem Redirect zurück zur Listenansicht (PRG).
- **Bestätigungsflows** werden umgesetzt durch entweder
  - einen zweiten "Confirm"-Schritt
  - CSS-only Modals (z.B. Checkbox/Label Pattern)
  
### Performance: Laden von Relationships
Listen-Seiten zeigen häufig verknüpfte Daten an (z.B. Einkaufsitems inkl zuständigem User).
Da das N+1 Query-Problem vermieden werden soll, werden die Beziehungen "eager" geladen mit `joinedLoad()`.

### Flash-Messages Kategorien (Bootstrap-Mapping)
Bootstrap erwartet Kategorien wie `success`, `danger`, `warning`, `info`.
Wenn im Code Kategorien wie `error` verwendet werden, sollten sie im Template auf `danger` gemappt werden, damit die Alerts korrekt rot/grün oder eine andere Farbe angezeigt werden.

![FlashMsgRed]({{ site.baseurl }}/assets/images/architecture/danger_flash.png)

### Base Template
Base Template (`base.html`) als UI-Backbone: globale Styles (Außer `activityboard.html`) und Flash-Messages, Änderungen wirken auf alle Seiten.

### Kalender-Export (.ics)
Activities können als `.ics` exportiert werden.
Diese ICS-Route erstellt serverseitig ein gültiges iCalendar Format und liefert es als Download aus, sodass der User es in gängige Kalender (z.B. Outlook/Google/Apple) importieren kann.

### CSRF-Schutz (Formulare)
Alle `POST`-Forms müssen das CSRF-Token haben (in diesem Fall `form.hidden_tag()` [im jinja2-Template]).

![hiddentag]({{ site.baseurl }}/assets/images/architecture/hiddentag.png)






{: .fs-2 }
Last build: {{ site.time | date: '%d %b %Y, %R%:z' }}