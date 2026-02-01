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

Für die visuelle Orientierung empfehlen wir die [Customer Journey]({{ site.baseurl }}/value_proposition.html#customer-journey).

### Was die Web-App macht
- **Login und Registrierung:** Account anlegen und sich mit diesem einloggen.
- **WG-Onboarding:** WG erstellen oder per zufallsgeneriertem **Invite-Code** beitreten.
- **Dashboard**: Überblick über letzte Aktivitäten innerhalb der WG, persönliche ToDos bzw. Erinnerungen, Anzahl offener Putzaufgaben, anstehende Aktivitäten, (neue) Ideen von WG-Mitgliedern und 
- **Putzplan:** Putzaufgaben anlegen, einem WG-Mitglied zuweisen, Status (*open/completed*) togglen bzw. durchstreichen und bestätigen und Fortschritt anzeigen.
- **Innovationboard:** Ideen posten, kommentieren, liken (leichtes Collaboration-Feature). 
- **Activityboard:** Events erstellen, beitreten/abmelden, maximale Teilnehmeranzahl prüfen, **.ics Export** fürs Kalender-Importieren.
- **Einkaufsliste:** Items hinzufügen, optional zuständig zuweisen, transparent für die gesamte WG.

{: .fs-2 }
Last build: {{ site.time | date: '%d %b %Y, %R%:z' }}