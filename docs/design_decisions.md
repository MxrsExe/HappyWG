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


---

### Betrachtete Alternativen


