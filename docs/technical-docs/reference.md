---
layout: default
title: Reference
parent: Technical documentation
nav_order: 3
---

# Reference Documentation

---

Diese Seite sammelt die wichtigsten internen Funktionen und Routen der Flask-Webanwendung HappyWG.

<details open markdown="block">
{: .text-delta }
<summary>Inhaltsverzeichnis</summary>
+ ToC
{: toc }
</details>

---

## Interne Hilfsfunktionen

---

### `generate_unique_code(length=6)`

**Route:** keine (interne Funktion)

**Methods:** -

**Purpose:** Generiert einen zufälligen Einladungscode für eine WG. Stellt sicher, dass der Code eindeutig ist, indem überprüft wird, ob er bereits in der Datenbank existiert.

**Sample output:** String (z.B. A9F3KQ)

<img src="{{ site.baseurl }}/assets/images/wg_creation_or_join/generatecodereference.png" alt="generate_unique_code sample" width="400" height= "400">

---

### `login_required(f)`

**Route:** keine (Decorator)

**Methods:** -

**Purpose:** Decorator-Funktion zum Schutz von Routen.
Stellt sicher, dass nur eingeloggte Nutzer auf bestimmte Seiten zugreifen können. Falls kein Nutzer eingeloggt ist, erfolgt eine Weiterleitung zur Login-Seite.

**Sample output:** Weiterleitung zu Login-Seite oder Ausführung der geschützten Route.

---

## Routen

---

### `login()`

**Route:** `/login/`

**Methods:** `GET`, `POST`

**Purpose:** Authentifiziert einen Benutzer mithilfe von Benutzername und Passwort.
Überprüft die Zugangsdaten gegen die Datenbank und erstellt bei Erfolg eine User-Session.

**Sample output:** Erfolgreicher Login -> Weiterleitung zur Willkommensseite. 
Fehler -> Anzeige einer Fehlermeldung in der Login-Seite.


<img src="{{ site.baseurl }}/assets/images/login_register/loginreference.png" alt="login sample" width="400">

<img src="{{ site.baseurl }}/assets/images/login_register/erfolgreicherloginreference.png" alt="login sample" width="400">

---

### `logout()`

**Route:** `/logout/`

**Methods:** `GET`

**Purpose:** Meldet den Benutzer ab indem die aktuelle Session gelöscht wird.

**Sample output:** Weiterleitung zur Login-Seite.

---

### `register()`

**Route:** `/register/`

**Methods:** `GET`, `POST`

**Purpose:** Registriert einen neuen Benutzer. Das Passwort wird gehasht in der Datenbank gespeichert. Nach erfolgreicher Registrierung wird der Benutzer automatisch eingeloggt. Wenn der Nutzer bereits existiert oder Passwörter nicht übereinstimmen bekommt er eine Fehlermeldung.

**Sample output:** 

<img src="{{ site.baseurl }}/assets/images/login_register/registerfehlgeschlagenreference.png" alt="login sample" width="400" height= "400">

---

### `create_or_join_wg()`

**Route:** `/welcome/`

**Methods:** `GET`, `POST`

**Purpose:** Willkommensseite nach dem Login. Zeigt Option zum Erstellen oder Beitreten einer WG an. Zugriff nur für eingeloggte Nutzer erlaubt.

**Sample output** 

![create_or_join_wg() sample]({{ site.baseurl}}/assets/images/wg_creation_or_join/wg_create_or_join.png)


---

### `create_wg()`

**Route:** `/welcome/create_wg/`

**Methods:** `GET`, `POST`

**Purpose:** Erstellt eine neue WG mit Namen und eindeutigem Einladungscode. Der Einladungscode kann später von anderen Nutzern verwendet werden, um der WG beizutreten.

**Sample output:** Erfolgsmeldung mit Einladungscode und Weiterleitung zur Join-Seite.

<img src="{{ site.baseurl}}/assets/images/wg_creation_or_join/generatecodereference.png" alt="create_wg sample" width="400" height= "400">

---

### `join_wg()`

**Route:** `/welcome/join_wg/`

**Methods:** `GET`, `POST`

**Purpose:** Ermöglicht einem Nutzer, einer bestehenden WG über einen Einladungscode beizutreten. Der Nutzer wird mit der WG in der Datenbank verknüpft.

**Sample output:** Weiterleitung zum Dashboard der WG nach erfolgreichem Beitritt.

![join_wg() sample]({{ site.baseurl}}/assets/images/wg_creation_or_join/invitation_code_eingabe.png)

---

### `dashboard()`

**Route:** `/dashboard/`

**Methods:** `GET`, `POST`

**Purpose:** Zentrale Übersichtsseite der WG. Zeigt Statistiken, offene Aufgaben, Einkaufsliste, kommende Events, letzte Aktivitäten sowie alle WG-Mitglieder an. Alle Daten werden anhand der wg_id gefiltert, um Mandantentrennung sicherzustellen.

**Sample output:** 

![dashboard() sample]({{ site.baseurl}}/assets/images/dashboard/dashboardreference.png)

---

### `putzplan()`

**Route:** `/putzplan/`

**Methods:** `GET`, `POST`

**Purpose:** Zeigt den Putzplan der WG an und erlaubt das Erstellen neuer Putzaufgaben. Bei einem POST-Request wird eine neue Putzaufgabe inklusive Vorlage (Cleaning-Template) und zugehörigem Task (CleaningTask) erstellt.

**Sample output:** 

![putzplan() sample]{{ site.baseurl}}/assets/images/putzplan/putzplanreference.png)

---

### `toggle_cleaning_task(task_id)`

**Route:** `/putzplan/task/<int:task_id>/toggle`

**Methods:** `POST`

**Purpose:** Wechselt den Status einer Putzaufgabe zwischen `open` und `completed`. Beim Abschließen wird zusätzlich das Abschlussdatum gespeichert.

**Sample output:** Kein direkter Output - Statusänderung sichtbar im Putzplan (Checkbox/Fortschrittsbalken).

---

### `delete_cleaning_task(template_id)`

**Route:** `/putzplan/task/<int:template_id>/delete`

**Methods:** `POST`

**Purpose:** Löscht eine Putzaufgabe inklusive ihrer Vorlage. Nur der zuständige Benutzer darf die Aufgabe löschen.

**Sample output:** 

![delete_cleaning_task(template_id) sample]({{ site.baseurl}}/assets/images/putzplan/deletecleaningtaskreference.png)

---

### `innovation_board()`

**Route:** `/innovationboard/`

**Methods:** `GET`, `POST`

**Purpose:** Zeigt alle Ideen der WG an und ermöglicht das Erstellen neuer Ideen. Ideen werden farblich dargestellt und dem Ersteller zugeordnet.

**Sample output:** 

![innovation_board() sample]({{ site.baseurl}}/assets/images/innoboard/innovationboardreference.png)

---

### `delete_idea(idea_id)`

**Route:** `/innovation_board/idea/<int:idea_id>/delete`

**Methods:** `POST`

**Purpose:** Löscht eine Idee. Nur der Ersteller der Idee darf diese löschen.

**Sample output:** 

![delete_idea(idea_id) sample]({{ site.baseurl}}/assets/images/innoboard/deleteideareference.png)

---

### `post_comment(idea_id)`

**Route:** `/ideas/<int:ieda_id>/comment`

**Methods:** `POST`

**Purpose:** Erstellt einen neuen Kommentar zu einer Idee. Neues Kommentar erscheint unter der Idee.

**Sample output:** 

<img src="{{ site.baseurl}}/assets/images/innoboard/commentideareference.png" alt="post_comment sample" width="400" height= "400">

---

### `activity_board()`

**Route:** `/activityboard/`

**Methods:** `GET`, `POST`

**Purpose:** Zeigt alle Aktivitäten der WG an und ermöglicht das Erstellen neuer Aktivitäten (Events). Aktivitäten enthalten Datum, Ort und maximale Teilnahmerzahl.

**Sample output:** 

![activity_board() sample]({{ site.baseurl}}/assets/images/activityboard/activityreference.png)

---

### `join_activity(activity_id)`

**Route:** `/activity/<int:activity_id>/join_activity`

**Methods:** `POST`

**Purpose:** Fügt den eingeloggten Benutzer als Teilnehmer einer Aktivität hinzu, sofern noch Plätze frei sind.

**Sample output:** 

![activity_board() sample]({{ site.baseurl}}/assets/images/activityboard/activitybeigetretenreference.png)

---

### `leave_activity(activity_id)`

**Route:** `/activity/<int:activity_id>/leave_activity`

**Methods:** `POST`

**Purpose:** Entfernt den eingeloggten Benutzer als Teilnehmer einer Aktivität.

**Sample output:**

<img src="{{ site.baseurl}}/assets/images/activityboard/leaveactivityreference.png" alt="post_comment sample" width="400">

<img src="{{ site.baseurl}}/assets/images/activityboard/leftactivityreference.png" alt="post_comment sample" width="400">

---

### `delete_activity(activity_id)`

**Route:** `/activity/<int:activity_id>/delete_activity`

**Methods:** `POST`

**Purpose:** Löscht eine Aktivität. Nur der Ersteller der Aktivität darf diese löschen.

**Sample output:** 

![activity_board() sample]({{ site.baseurl}}/assets/images/activityboard/activityloeschenreference.png)

---

### `einkaufsplan()`

**Route:** `/einkaufsplan/`

**Methods:** `GET`, `POST`

**Purpose:** Zeigt die Einkaufsliste der WG an und ermöglicht das Hinzufügen neuer Artikel. Der Artikel wird dem jeweiligen Ersteller zugewiesen.

**Sample output:** 

![einkaufsplan() sample]({{ site.baseurl}}/assets/images/putzplan/einkaufslistereference.png)

---

### `delete_shopping_item(item_id)`

**Route:** `/einkaufsplan/item/<int:item_id>/delete`

**Methods:** `POST`

**Purpose:** Löscht einen Eintrag aus der Einkaufsliste.

**Sample output:** 

![delete_shopping_item(item_id) sample]({{ site.baseurl}}/assets/images/putzplan/artikelgeloeschtreference.png)

---

## Export & Kalender

---

### `activity_ics(activity_id)`

**Route:** `/activities/<int:activity_id>/ics`

**Methods:** `POST`

**Purpose:** Erstellt eine ICS-Datei für eine Aktivität, die in einen externen Kalender (z.B. Google Calendar) importiert werden kann.

**Sample output:** Download einer `.ics`-Datei.

---

### `export_wg_json()`

**Route:** `/export/wg.json`

**Methods:** `GET`

**Purpose:** Exportiert alle relevanten WG-Daten (User, Aktivitäten, Ideen, Einkaufen, Putzaufgaben) als JSON-Datei.

**Sample output:** 

![export_wg_json() sample]({{ site.baseurl}}/assets/images/dashboard/jsondateireference.png)

---

## Hilfsfunktionen (ohne Route)

---

### `google_calendar_url(...)`

**Purpose:** Erstellt eine Google-Calendar-URL für eine Aktivität mit Titel, Datum, Beschreibung und Ort.

**Sample output:** URL-String für Google Calendar.

---

### `build_ics(...)`

**Purpose:** Erstellt den Inhalt einer ICS-Kalenderdatei für den Export von Aktivitäten.

**Sample output:** Text im ICS-Format.

---

## WTForms Klassen (ohne Routen) in `forms.py`

### `class UserExistsValidator`

**Purpose:** Validiert serverseitig, dass ein eingegebener Benutzername in der Datenbank existiert. Wird z. B. im Putzplan genutzt, um sicherzustellen, dass nur reale WG-Mitglieder als "zuständig" eingetragen werden können. Bei fehlendem User wird eine ValidationError mit einer klaren Fehlermeldung ausgelöst.

**Sample output: - (siehe PutzplanForm)**

---

### `class LoginForm(FlaskForm)`

**Purpose:** Definiert das Login-Formular (Benutzername + Passwort) inklusive Validierung (Pflichtfelder, Längenbegrenzung). Dient als zentrale Eingabeschicht für die Login-Route, bevor Credentials in der Datenbank geprüft werden.

**Sample output:** 

![LoginForm]({{ site.baseurl }}/assets/images/login_register/loginForm.png)

---

### `class RegisterForm(FlaskForm)`

**Purpose:** Definiert das Registrierungsformular mit Username, E-Mail und Passwort-Validierungen. Enthält zusätzlich `confirm_password` mit `EqualTo`, um sicherzustellen, dass beide Passwörter übereinstimmen. Ermöglicht konsistente serverseitige Eingabeprüfung vor dem Erstellen eines neuen Users.

**Sample output:** 
![RegisterForm]({{ site.baseurl }}/assets/images/login_register/registerForm.png)

---

### `class PutzplanForm(FlaskForm)`

**Purpose:** Formular zum Erstellen einer neuen Putzaufgabe. Validiert Aufgabe, zuständige Person und Datumsbereich. Nutzt UserExistsValidator, damit "Zuständig" nur ein existierender User sein kann (und dadurch keine ungültigen Zuweisungen entstehen).

**Sample output:**
![onlyWgMemberTaskForm]({{ site.baseurl }}/assets/images/putzplan/flaskForm_onlyWGmember.png)

---

### `class InnovationForm(FlaskForm)`

**Purpose:** Formular für das Innovationboard: erstellt neue Ideen mit Titel, Beschreibung und Farbe. Validierungen stellen sicher, dass Felder nicht leer sind und die maximale Textlänge eingehalten wird. Das Farbfeld ist als `type="color"` für eine Farbauswahl im Browser gedacht.

**Sample output:**
![InnovationForm]({{ site.baseurl }}/assets/images/innoboard/innoForm.png)

---

### `class CommentForm(FlaskForm)`

**Purpose:** Formular zum Posten von Kommentaren auf Ideen. Sichert ab, dass Kommentare nicht leer sind und eine maximale Länge nicht überschreiten. Dadurch bleiben Inhalte strukturiert und UI/Layout stabil.

**Sample output:**
![CommentForm]({{ site.baseurl }}/assets/images/innoboard/commentForm.png)

---

### `class ActivityForm(FlaskForm)`

**Purpose:** Formular zum Erstellen einer Aktivität (Event) inklusive Zeitraum (`date` bis `date_to`), Beschreibung, Ort und optionaler maximaler Teilnehmerzahl. Nutzt `DateTimeLocalField` für browserfreundliche Datum/Uhrzeit-Eingabe und validiert serverseitig alle Pflichtfelder.

**Sample output:**
![ActivityForm]({{ site.baseurl }}/assets/images/activityboard/activityForm.png)

---

### `class EinkaufsplanForm(FlaskForm)`

**Purpose:** Formular zum Hinzufügen von Einkaufsartikeln mit Artikelname und Menge. Validiert Pflichtfelder und Längenbereich, damit Einträge konsistent sind und nicht leer/zu lang werden.

**Sample output:**
![EinkaufsplanForm]({{ site.baseurl }}/assets/images/einkaufsliste/einkaufsplanForm.png)


{: .fs-2 }
Last build: {{ site.time | date: '%d %b %Y, %R%:z' }}

[def]: {{ site.baseurl}}/assets/images/innoboard/deleteideareference.png