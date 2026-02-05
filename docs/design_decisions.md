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

Status: **Entschieden** 

Updated: 06-02-2026

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

Wir haben uns dafür entschieden, die **WG als zentrales Kernelement des Datenmodells zu verwenden.
- Eine WG dient als übergeordneter Container für fast alle Daten.
- Nutzer:innen gehören jeweils zu **einer WG** 
- Zentrale Tabellen wie Activity, Idea, ShoppingItem oder CleaningTemplate enthalten einen Fremdschlüssel (wg_id), über den sie eindeutig einer WG zugeordnet sind.

Durch diese Entscheidung ist klar geregt:
- welche Daten zu welcher WG gehören
- welche Nutzer:innen auf welche Daten zugreifen dürfen
- dass Daten verschiedener WGs strikt getrennt bleiben

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
+ einfache Filterung und Zugriffsprüfung über `wg_id``
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

{: .fs-2 }
Last build: {{ site.time | date: '%d %b %Y, %R%:z' }}

[def]: assets/images/innoboard/deleteideareference.png
