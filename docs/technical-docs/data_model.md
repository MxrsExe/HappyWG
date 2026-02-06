---
layout: default
title: Data model
parent: Technical documentation
nav_order: 2
---

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

---
# Data Model

---

## Das Data Model von Happy WG, Stand 05.02.2025
![DataModel](assets/images/data_model.png)

---

## Entities (Tabellen) und wichtigste Spalten

*_nicht (direkt) implementiert, aber geeignet für evtl. weitere App-Erweiterungen_

---

### Dashboard

---

`WG`
- **PK:** `wg_id`
- **Spalten:** `name` (unique), invite_code (String(6)), created_at 
- **Rollen:** Scope für fast alle Daten & Kollaboration

---

`User`
- **PK:** `user_id`
- **Spalten:** FK: Wg → `wg_id`(nullable),`username` (unique), `email` (unique), `password_hash`, `role` (default: member; für Erweiterungen geeignet)
- **Rolle:** Nutzerkonto; gehört optional zu einer WG (am Anfang keiner, deswegen nullable), wird nach "Join" gesetzt.

---

### Putzplan

---

`CLEANING_TEMPLATE`
- **PK:** `template_id`
- **FK:** `wg_id` → `WG.wg_id`
- **Spalten:** `name`, `description`, `frequency`*, `is_active`
**Rolle:** Für weitere Erweiterungen gedacht; Template abspeichern und wiederverwenden (_aus Zeitgründen & Projektkomplexität nicht implementiert_)

---

`CLEANING_TASK`
- **PK:** `task_id`
- **FKs:** `template_id` → `CLEANING_TEMPLATE.template_id`, `assigned_to` → `USER.user_id`
- **Spalten:** `status`, `completed_at`* & `notes`*
- **Rolle:** Beinhaltet die Aufgabe zum durchstreichen.

---

### InnovationBoard

---

`IDEA`
- **PK:** `idea_id`
- **FKs:** `wg_id` 
- **Spalten:** `title`, `description`, `color`, `created_at`, `updated_at`* & `status`*
- **Rolle:** WG-Mitglieder können eine Idee erstellen, beinhaltet alle wichtigen Infos zu dieser Idee.

---

`IDEA_COMMENT`
- **PK:** `comment_id`
- **FKs:** `idea_id` → `IDEA.idea_id`, `user_id` → `USER.user_id`
- **Spalten:** `content`, `created_at`
- **Rolle:** Gehört einer Idee, der User kann diese Idee kommentieren.

---

`IDEA_LIKE`
- **PK:** `like_id`
- **FKs:** `idea_id` → `IDEA.idea_id`, `user_id` → `USER.user_id`
- **Rolle:** Die Idee hat einen Like-Button, welchen die User klicken können. Ein Like von diesem User wird dieser Idee hinzugefügt.

---

### ActivityBoard

---

`ACTIVITY`
- **PK:** `activity_id`
- **FKs:** `wg_id` → `Wg.wg_id`, `created_by` → `USER.user_id`
- **Spalten:** `title`, `description`, `date`, `date_to`, `location`, `max_participants`, `created_at`
- **Rolle:** User können Aktivitäten hinzufügen, die alle Informationen über diese Aktivität enthalten.

---

`ACTIVITY_PARTICIPANTS` (Assoziationstabelle)
- **Composite PK:** (`activity_id`, `user_id`)
- **FKs:** `activity_id` → `ACTIVITY.activity_id`, `user_id` → `USER.user_id`
- **Rolle:** Many-to-Many: Teilnehmer einer Activity.

---

### Einkaufsplan

---

`ShoppingItem`
- **PK:** `item_id` → `WG.wg_id`, `created_by` → `USER.user_id`
- **FKs**: wg_id → WG.wg_id, added_by → USER.user_id, assigned_to → USER.user_id
- **Spalten:** `name`, `quantity`, `created_at`
- **Rolle:** User können Einkaufsitems anlegen mit der zuständigen Person, Menge & Name

---

## Beziehungen zwischen den Tabellen
---
### 1:N Beziehungen

| Von | Zu | Beschreibung |
| --- | --- | --- |
| **WG** | USER | Eine WG kann viele User haben, ein User gehört zu einer WG. |
| **WG** | CLEANING_TEMPLATE | Eine WG kann viele Putzpläne haben, ein erstellter Putzplan gehört zu einer WG. |
| **WG** | SHOPPING_ITEM | Eine WG kann viele Einkaufsitems haben, ein erstelltes Einkaufsitem gehört zu einer WG. |
| **WG** | IDEA | Eine WG kann viele Ideen haben, eine erstellte Idee gehört zu einer WG. |
| **WG** | ACTIVITY | Eine WG kann viele Activities haben, ein eine erstellte Activity gehört zu einer WG. |
| **ACTIVITY** | ACTIVITY_PARTICIPANTS | Eine Activity kann viele Teilnehmer haben. |
| **CLEANING_TEMPLATE** | CLEANING_TASK | Jede Vorlage kann mehrere Tasks enthalten. |
| **USER** | CLEANING_TASK | Ein User kann mehrere Putzaufgaben haben, eine Putzaufgabe ist einem User zugeordnet. |
| **USER** | ACTIVITY_PARTICIPANTS | Ein User kann an vielen Activities teilnehmen, vermittelt über Activity_Participants. |
| **USER** | IDEA | Ein User kann Ideen erstellen, eine Idee kann von einem User erstellt werden. |
| **USER** | IDEA_COMMENT | Ein User kann mehrere Kommentare unter eine Idee schreiben, ein Kommentar kann von einem User erstellt werden. |
| **USER** | IDEA_LIKE | Ein User kann mehrere Ideen liken, ein Like kommt von einem User. |
| **IDEA** | IDEA_LIKE | Eine Idee kann mehrere Likes haben, ein gespeichertes Like gehört einer Idee. |


---
### N:M Beziehungen

| Von | Zu | Beschreibung |
| --- | --- | --- |
| **USER** | ACTIVITY_PARTICIPANTS | Ein User kann an vielen Activities teilnehmen, vermittelt über Activity_Participants |

---


{: .fs-2 }
Last build: {{ site.time | date: '%d %b %Y, %R%:z' }}