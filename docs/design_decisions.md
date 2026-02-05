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
<summary>Table of contents</summary>
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







{: .fs-2 }
Last build: {{ site.time | date: '%d %b %Y, %R%:z' }}

[def]: assets/images/innoboard/deleteideareference.png


