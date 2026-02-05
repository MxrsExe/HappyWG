---
layout: default
title: Design Decisions
parent: Technical Docs
nav_order: 4
---


# Design Decisions

---

<details open markdown="block">
{: .text-delta }
<summary>Inhaltsverzeichnis</summary>
+ ToC
{: toc }
</details>

---

## 01: Zentrales WG-basiertes Datenmodell

Status: **Entschieden, obsolete** 

Updated: 05-02-2026

### Problemstellung

Die Anwendung ist für Wohngemeinschaften (WGs) konzipiert. Funktionen wie Einkaufslisten, Aktivitäten, Ideen oder Putzpläne sollen **von allen Mitgliedern einer WG gemeinsam genutzt** werden, gleichzeitig aber **klar von anderen WGs getrennt** bleiben.

Zu Beginng des Projekts stellte sich daher die Frage, **wie wir die Daten logisch strukturiert werden sollen**:
- Sollen Daten direkt einzelnen Nutzer:innen gehören?
- Oder braucht es eine zentrale Struktur, die gemeinsam Daten zusammenfasst?

Wichtig war dabei:
- eine klare Trennung der Daten zwischen verschiedenen WGs
- ein Modell, welches sich später gut erweitern lässt

---

### Entscheidung

Wir haben uns dafür entschieden, die **WG** als zentrales Kernelement des Datenmodells zu verwenden.
- Eine WG dient als übergeordneter Container für fast alle Daten.
- Nutzer:innen gehören jeweils zu **einer WG**. 
- Zentrale Tabellen wie Activity, Idea, ShoppingItem oder CleaningTemplate enthalten einen Fremdschlüssel (`wg_id`), über den sie eindeutig einer WG zugeordnet sind.

Durch diese Entscheidung ist klar geregelt:
- welche Daten zu welcher WG gehören
- welche Nutzer:innen auf welche Daten zugreifen dürfen
- dass Daten verschiedener WGs strikt getrennt bleiben.

Diese Struktur entspricht außerdem gut der realen Nutzung der App.

---

### Betrachtete Alternativen

### Option 1: Nutzerzentriertes Datenmodell
Alle Daten sind direkt einzelnen Nutzer:innen zugeordnet, ohne eigene WG-Entität.

### Vorteile
+ einfacheres Modell zu Beginn
+ weniger Tabellenbeziehungen

### Nachteile
+ gemeinsame Nutzung von Daten nur schwer abbildbar
+ kompliziertere Zugriffslogik
+ schlechte Erweiterbarkeit (z.B. Rollen, mehrere Nutzer pro Objekt)

--- 

### Option 2: WG-zentriertes Datenmodell (gewählt)
Gemeinsame Daten gehören immer zu einer WG, Nutzer:innen sind Mitglieder dieser WG.

### Vorteile
+ klare Trennung zwischen verschiedenen WGs
+ gemeinschaftliche Nutzung von Daten logisch abgebildet
+ einfache Filterung und Zugriffsprüfung über `wg_id`
+ gut erweiterbar (z.B. Rollen)

### Nachteile
+ etwas komplexeres Datenmodell
+ zusätzliche Joins bei Datenbankabfragen

| Kriterium | **Nutzerzentriert** | **WG-zentriert** |
| --- | --- | --- |
| Datentrennung | unklar | klar |
| Gemeinsame Nutzung | eingeschränkt | vorgesehen |
| Erweiterbarkeit | gering | gut |
| Verständlichkeit | einfach | realitätsnah |

---

## 02: Authorization-Modell - Wer darf was?

Status:**Entschieden, obsolete**

**Updated:** 05.02.2026

### Problemstellung

In HappyWG gibt es mehrere Features (Activities, Putzplan, Ideas, Einkaufsliste), bei denen User Daten ändern oder löschen können.
Daher müssen wir festlegen, **wer welche Aktionen** durchführen darf (z.B. löschen, Status ändern, beitreten/abmelden), wegen diesen Regeln:

- die Sicherheitslogik in den Routes bestimmen (Backend),
- die UI bestimmen (Buttons anzeigen/ausblenden),
- und spätere Änderungen sehr teuer machen (viele Endpoints + Templates betroffen)

Wie gestalten wir die Experience so, dass jedes WG-Mitglied gleichberechtigt ist und klare Aufgaben & das immaterielle Eigentum der Mitglieder nicht verletzt werden?

---

### Entscheidung

Wir nutzen ein **feature-spezifisches** Ownership-Modell:

- **Activites:** Nur `created_by` darf löschen.
- **Cleaning Tasks/Templates:** Nur die zuständige Person (`assigned_to`) darf löschen bzw. erledigen (je nach Policy)
- **Ideas:** Nur der Ersteller (`created_by`) darf löschen; WG-Mitglieder dürfen liken/kommentieren.
- **Allgemein:** Zugriff ist zusätzlich immer über `wg_id` begrenzt (siehe [01: Zentrales WG-basiertes Datenmodell](#01-zentrales-wg-basiertes-datenmodell))

---

### Betrachtete Alternativen

### Option 1: Nur Owner darf alles (einheitlich)

#### Vorteile 
+ Einfach zu implementieren
+ Weniger Sonderfälle in Routes & Templates

#### Nachteile
+ Passt nicht zur Realität einer WG und unserer Philosophie
+ Unflexibel: "Zuständigkeit" als Konzept bringt wenig, wenn Owner alles steuert.
+ Kann zu schlechter UX führen (zuständige Person kann Aufgabe nicht als erledigt markieren, wenn sie nicht Owner ist (**!**))

### Option 2: WG-weit darf jeder alles (maximal einfach, aber sehr unsicher)
- Alle WG-Mitglieder dürfen von anderen WG-Mitgliedern alles wie z.B. löschen.

#### Vorteile
+ Minimaler Implementationsaufwand: fast keine Ownership-Checks
+ Sehr schnell fürs MVP

#### Nachteile
+ Unsere Philosophie ist, dass jedes WG-Mitglied gleichberechtigt sein & nicht über andere Mitglieder und deren Zuständigkeiten & Aufgaben bestimmen sollen, dies geschieht aber über diese Option.
+ **Sicherheits-/Vertrauensprobleme:** Jeder darf alles löschen/verändern: Chaos, nicht gut für eine WG.
+ Konflikte innerhalb der WG (z.B. "Wer hat mein Event gelöscht?" oder "Ich weiß nicht mehr, welche Reinigungsaufgabe ich habe!")
+ Spätere Korrektur ist teuer, da man nachträglich Checks + UI-Logik einbauen muss.

### Option 3 (gewählt): Feature-spezifische Regeln (Owner vs. zuständig)
- Wer was machen kann wird pro Feature entschieden

#### Vorteile
+ Realistische Regeln pro Feature (Activites: Activity Owner, Cleaning: assigned_to; Ideas: Owner; Like/Comment: WG)
+ Bessere UX: Flash messages nach einem Button-Klick weisen den unberechtigen User drauf hin, dass er nicht berechtigt ist.
+ Gute Basis für späteres Rollenmodell (z.B. Admin als Erweiterung)

#### Nachteile
+ Etwas mehr Komplexität: pro Feature andere Checks
+ Policy-Änderung würden mehrere Endpoints/Templates betreffen.
  
### Option 4 Rollenmodell:
- Es gibt durch z.B. `role="admin"` (_später implementierbar_) einen Administrator, der alles verändern kann.

#### Vorteile
+ Klar skalierbar: Admin kann moderieren/aufräumen.
+ Gut für Missbrauchsfälle

#### Nachteile
+ Mehr Modell/UI-Aufwand (Rollenpflege, Admin-UI, Tests)
+ Für unser MVP overkill
+ Man muss trotzdem definieren, was Member dürfen (landet wieder bei Option 3 + Admin-Override)

### 02: Konsequenzen
- Backend-Routen müssen vor Änderungen immer prüfen: `current_user.wg_id` == `object.wg_id` und getroffene Ownership-Regel zum Feature.
- Nicht zugewiesene oder unberechtige User können die Objekte anderer WG-Mitglieder nicht anfassen.
- Spätere Einführung von Admin-Rollen möglich, erfordert aber konsistente Anpassung vieler Endpoints.


## 03: Putzplan-Datenmodell - Cleaning Template vs. nur Cleaning Task (Plan vs. Ausführung)

**Meta**

**Status:** On Hold, relevant

**Updated:** 05.02.2026

### Problemstellung

Wir wollten ursprünglich einen Putzplan abbilden, bei dem Aufgaben
- wiederkehrend geplant werden können (z.B. _weekly_) (_nicht implementiert_)
- einzelnen WG-Mitgliedern zugewiesen werden können
- einen Status (open/completed) + Zeitstempel tragen,
- **ggf.** als _späteres Feature_ Historie, Rotation oder Statistiken ermöglichen

Die Frage ist: Modellieren wir das als eins oder trennen wir Vorlage (Plan) und Ausführung (Task)?

### Vorläufige Entscheidung

Wir trennen in:
- `CleaningTemplate` = Plan/Vorlage (Name, Beschreibung, Frequenz, wg_id, is_active)
- `CleaningTask` = konkrete Ausführung/Instanz (assigned_to, status, completed_at, template_id)

**Grund**: Potentiell wollen wir die App privat erweitern und neue Features einfügen, die dadurch ermöglicht werden. Für andere Devs könnte diese Design-Entscheidung ebenfalls eine Hilfestellung für neue Features sein.

---

### Betrachtete Alternativen

#### Option 1: Eine gemeinsame CleaningTask Tabelle
- Task-Card enthält alles

#### Vorteile
- Einfacher Start: nur ein Objekt-Modell, weniger Joins
- CRUD-Ops schneller zu bauen

#### Nachteile
- Änderungen am Plan könnten alte Einträge betreffen

### Option 2: Template + Task getrennt (chosen)

#### Vorteile
- Saubere Domänentrennung
- Ideal für spätere Features (_geplant zu implementieren, aus Zeit- und Scopegründen nicht geschafft_)
- Weniger Daten-Duplikation

#### Nachteile
- Mehr Joins/Relationships in Queries/Templates
- Beim Erstellen in der App immer 2 Schritte
- Klare Policy benötigt

### Option 3: Template + automatisch generierte Tasks (Scheduler/Cron)
#### Vorteile
+ "Echte" Wiederkehr: systematisch jede Woche neue Tasks
+ Sehr gute Basis für Historie/Rotation (neue Features) ohne manuelles Erstellen

#### Nachteile
+ Mehr Infrastruktur/Komplexität (Scheduler, Background Jobs etc.)
+ Zu viel Aufwand 
+ Fehleranfälliger

---

### Konsequenzen

- Es ist möglich, später neue Features einfach hinzuzufügen.
- **Queries/Joins notig:** Für die Anzeige/Filterung wird häufiger über Relationships gearbeitet (`template.tasks`, Join auf Template für wg_id Scoping)
- Gerade ohne diese Features kein Nutzen, aber da vorher so geplant, haben wir es drin gelassen.

## 04: Hard Delete vs Soft Delete (Daten löschen oder deaktivierebn)

**Meta**

**Status:** Entschieden, obsolet

**Updated:** 05.02.2026

### Problemstellung
Bei Löschfunktionen (z.B. Idee löschen, Putzplan-Template löschen, Einkaufsitem löschen etc.) stellt sich die Frage:
  - Sollen diese Datensätze wirklich aus der DB entfernt werden (**Hard Delete**)?
  - Oder nur als "gelöscht/deaktiviert" markiert werden (**Soft Delete**)?
Das beeinflusst nicht nur die Datenintegrität, sondern auch spätere Anforderungen wie History, Wiederherstellung und, insbesondere für Devs, das Debugging.

---

### Entscheidung

Für unser jetziges MVP verwenden wir **Hard Delete** für echte Löschaktionen (z.B. `db.session.delete(...)).
Für die Putzplan-Templates existiert zusätzlich ein **Soft-Delete** Feature `is_active`, mit dem Einträge aus der Standardansicht ausgeblendet bzw. durchgestrichen werden können.

---

### Betrachtete Alternativen

### Option 1: Hard Delete direkt aus der DB (chosen)
#### Vorteile
+ Sehr simpel (einfach mit `db.session.delete(...)`)
+ Keine "gelöscht-Filter" in allen Queries nötig
+ Weniger Datenballast & Sonderlogik

#### Nachteile
+ Keine Wiederherstellung der Daten möglich, da irreversibel gelöscht
+ Keine History (z.B. wer hat wann was gelöscht?)
+ Cascades können mehr löschen als erwartet (z.B. Template → Tasks), Vorsicht ist geboten

### Option 2: Soft Delete (mit Variable deleted_at)
#### Vorteile
+ Wiederherstellen möglich (durch Archiv oder Undo)
+ History möglich
+ Besser für 1) WG: Transparenz in Gruppen, 2) Dev: Debugging

#### Nachteile
+ Jede Query muss "nicht gelöscht" irgendwie filtern, wodurch mehr Fehlerquellen entstehen könnten
+ UI muss Archiv implementieren
+ Mehr Felder + mehr Tests

### Option 3: Hybrid (manche Entities soft, andere hard)
#### Vorteile
+ Flexibilität: Man kann wichtige Daten behalten, unwichtige löschen
+ Guter Kompromiss zwischen Aufwand und Nutzen.

#### Nachteile
+ Inkonsistent: Entwickler müssen pro Entity wissen, was gilt.
+ Mehr Denkaufwand + Doku nötig
+ Verwirrungsgefahr

---

### Konsequenzen

- MVP bleibt simpel
- Spätere Anforderungen wie "Wiederherstellen" erfordern Umstellung auf Soft Delete.
- Soft Delete bedeutet: **alle** relevanten Queries **müssen** "nur nicht gelöschte Datensätze" filtern.

## 05: Many-to-Many Activities - Association Table (`ACTIVITY_PARTICIPANTS`)

**Meta**

**Status:** Entschieden

**Updated:** 05.02.2026

### Problemstellung

In HappyWG sollen WG-Mitglieder Aktivitäten (Events) beitreten oder verlassen können. Eine Aktivität kann dabei viele Teilnehmer haben, und ein User kann an vielen Aktivitäten teilnehmen. Somit entsteht eine klassische **Many-to-Many-Beziehung** zwischen `User` und `Activity`

Wir müssen entscheiden, wie wir diese Beziehung im Datenmodell abbilden, sodass:

- **Join/Leave** effizient möglich ist (ohne komplizierte SQL-Logik),
- Duplikate verhindert werden (ein User soll nicht doppelt beitreten)
- (Modell erweiterbar bleibt)

---

### Entscheidung

Wir nutzen eine **Association Table (Join Tabelle)** `ACTIVITY_PARTICIPANTS` als reine Zuordnungstabelle:
- Primärschlüssel ist ein **Composite Key** aus (`activity_id`,`user_id`), was die doppelte Teilnahme verhindert.
- SQLAlchemy Many-to-Many Mapping über `secondary = activity_participants`:
  - `Activity.participants`
  - `User.joined_activities`
  
Beispiel aus HappyWG-Code:
`activity.participants.append(user)` (Aktivität beitreten) bzw. `activity.participants.remove(user)` (Aktivität verlassen)

---

### Betrachtete Alternativen

### Option 1: Association Table (pure join table) (chosen)
- Einfaches n:m Mapping über eine Join-Tabelle mit zwei FKs und Composite PK

#### Vorteile
- Relational korrekt für Many-to-Many (Normalisierung)
- Einfaches **ORM-Handling** (siehe obiges Beispiel)
- Keine Duplikate durch Composite PK 
- Gute Performance bei typischen Abfragen; Eager Loading (`joinedLoad(Activity.participants)`) funktioniert damit gut
- Wenig Code bzw. kein zusätzliches Model, keine extra CRUD

#### Nachteile
- Schwierig zu ändern, ggf. Migration auf Option 2 nötig

### Option 2: Association Object (eigenes Model)
- z.B. `ActivityParticipant`

#### Vorteile

- Maximal erweiterbar, man kann neue Felder speichern
- Flexiblere Queries

#### Nachteile

- Mehr Implementierungsaufwand, da zusätzliches Model mit ggf. eigener CRUD-Logik
- **ORM-Zugriff** ist etwas komplexer
- Wir brauchen nur beitreten und verlassen, deswegen overkill

---

### Konsequenzen

- Saubere Logik
- Kein doppeltes Beitreten derselben Activity
- Beitreten & verlassen ist simpel
- Performante Abfragen möglich








{: .fs-2 }
Last build: {{ site.time | date: '%d %b %Y, %R%:z' }}

[def]: assets/images/innoboard/deleteideareference.png


