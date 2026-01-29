---
layout: default
title: Value Proposition
nav_order: 2
---

## Value Proposition

**Problem**: Ungleiche Aufgabenverteilung, vergessene Einkäufe, Kommunikationslücken, unstrukturierter Alltag, Konflikte über Sauberkeit und Verantwortlichkeiten. Unsere App soll bei diesen Problemen helfen.

**Lösung**: WG-Leben nachhaltig verbessern, indem Organisation, Transparenz und gemeinschaftliches Handeln in einem digitalen Raum vereint werden. Schluss mit den verstreuten Notizen, chaotischen Whatsapp-Chats oder unzuverlässigen mündlichen Absprachen, die zu unnötigem Streit führen. Unsere WG-Helfer Plattform bietet zentrale, intuitive Werkzeuge, die speziell auf die Bedürfnisse von WGs zugeschnitten sind. 

Mit einem smarten WG-Planer,Putzplänen, einem flexiblen Innovation-Board für Ideen & Projekte, einem Activity Board für gemeinsame Events sowie einer gemeinschaftichen Einkaufsliste wird das Zusammenleben nicht nur strukturierter, sondern auch harmonischer und effizienter.

Unser Ziel ist, den Alltag in der WG spürbar zu erleichtern, Konflikte reduzieren, Verantwortungen fair zu verteilen und gleichzeitig die Gemeinschaft stärken. 

## **Goals**:
**Susann**: Mein WG Leben leichter und angenehmer machen, Programmiererfahrung sammeln, gegebenenfalls Web App im Alltag benutzen
**Marcel**: Programmiererfahrung sammeln im Bereich Python und Full Stack Web Development für das Berufsleben ggf.

**Als Gruppe**: Großes Ambitionslevel, regelmäßige Arbeit am Projekt, keine Prokrastion, Großteil vor Weihnachten fertig haben?

# Customer Journey

## Login bzw. Registrierung

Der Customer landet erstmal auf der Login Page, wo er/sie auswählen kann, ob man sich anmelden (Account vorhanden) oder registrieren möchte.
In diesem Fall hat der Customer keinen Account, weshalb er/sie auf "Jetzt registrieren" klickt, um sich einen Account zu erstellen.



## Putzplan
![PutzplanGeneral](assets/images/putzplan/putzplan_general.png)

Wie man im Putzplan sieht, sieht man nichts. Nur die Überschrift und die Navigationsleiste. Das liegt daran, dass weder der User, noch jemand anderes in der WG eine Aufgabe angelegt hat. Der User erstellt eine Aufgabe, indem er/sie auf den blauen Button oben rechts "🧼Neue Aufgabe" klickt.

![PutzplanModal](assets/images/putzplan/putzplan_modal.png)

Beim Klicken des Buttons bekommt der User ein Modal mit den einzelnen Daten angezeigt, die er/sie bestimmen kann. Dazu gehören: Von wann bis wann, welche Aufgabe und wer dafür zuständig ist. Achtung: Es können NUR WG-Mitglieder der selben WG Aufgaben bekommen (siehe). Im Privaten einigen sich die WG-Mitglieder selber, wer wann welche Aufgabe übernimmt.

Der User kann nun die Felder ausfüllen. Dabei wählt der User die von und bis-Daten per Kalenderansicht aus, benennt die Aufgabe, erteilt die Zuständigkeit und klickt auf den Button "Erstellen". 

![PutzplanVonDate](assets/images/putzplan/von_datum.png)
![PutzplanBisDate](assets/images/putzplan/bis_datum.png)

So kann beispielsweise ein ausgefülltes Modal aussehen für eine Aufgabe:

![PutzplanModalFilled](assets/images/putzplan/putzplan_modal_filled.png)



{: .fs-2 }
Last build: {{ site.time | date: '%d %b %Y, %R%:z' }}