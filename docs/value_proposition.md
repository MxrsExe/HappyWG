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
![Login](assets/images/login_register/login.png)
![Register](assets/images/login_register/register.png)

Nach dem Registrieren folgt die Anmeldung(aus Demonstrationszwecken übersprungen) und die Auswahl, ob man einer WG beitreten möchte oder eine erstellen will.
In diesem Fall wird der Customer eine WG erstellen.
![CreateWG](assets/images/wg_creation_or_join/wg_create_or_join.png)

Bei der Erstellung der Wohngemeinschaft bekommt der Customer einen Einladungscode bzw. einen "digitalen Schlüssel" zur WG, den er ins unterliegende Feld eingibt.

![WGKey](assets/images/wg_creation_or_join/wg_key.png)

Danach landet der User auf dem Dashboard, welches leer ist und im Verlauf noch mit Informationen gefüllt werden wird.
![dashboardEmpty](assets/images/dashboard/dashboard_empty.png)

Der User möchte einen Putzplan anlegen. Dazu wählt er/sie in der Navigationsleiste auf dem Dashboard den "Putzplan"-Button.

## Putzplan
![PutzplanGeneral](assets/images/putzplan/putzplan_general.png)

Wie man im Putzplan sieht, sieht man nichts. Nur die Überschrift und die Navigationsleiste. Das liegt daran, dass weder der User, noch jemand anderes in der WG eine Aufgabe angelegt hat. Der User erstellt eine Aufgabe, indem er/sie auf den blauen Button oben rechts "🧼Neue Aufgabe" klickt.

![PutzplanModal](assets/images/putzplan/putzplan_modal.png)

Beim Klicken des Buttons bekommt der User ein Modal mit den einzelnen Daten angezeigt, die er/sie bestimmen kann. Dazu gehören: Von wann bis wann, welche Aufgabe und wer dafür zuständig ist. Achtung: Es können NUR WG-Mitglieder der selben WG Aufgaben bekommen (siehe [WG-Scope](#wg-scope)). Im Privaten einigen sich die WG-Mitglieder selber, wer wann welche Aufgabe übernimmt.

Der User kann nun die Felder ausfüllen. Dabei wählt der User die von und bis-Daten per Kalenderansicht aus, benennt die Aufgabe, erteilt die Zuständigkeit und klickt auf den Button "Erstellen". 

![PutzplanVonDate](assets/images/putzplan/von_datum.png)
![PutzplanBisDate](assets/images/putzplan/bis_datum.png)

So kann beispielsweise ein ausgefülltes Modal aussehen für eine Aufgabe:

![PutzplanModalFilled](assets/images/putzplan/putzplan_modal_filled.png)

Wenn die Aufgabe erstellt wurde, wird sie so als Card angezeigt. Der User sieht den Zuständigen, die Bezeichnung der Aufgabe und die Kalenderwoche bzw. das Datum, wann wer zuständig ist. Außerdem noch einen Löschen-Button mit einem Mülltonne-Emoji oben rechts in der Card und einen bestätigen-Button, um wirklich die Aufgabe nach dem Checken der Checkbox als erledigt zu markieren (nötig aus HTML-Persistenz-Gründen). 

Bei Erledigung aller Aufgaben (aus Demonstrationsgründen hier nur eine) wird die Progressbar grün und der User wird benachrichtigt, dass alle Aufgaben erfüllt wurden. Ein anderes Mitglied kann Aufgaben hinzufügen, löschen aber kann es nur seine eigenen Aufgaben (siehe [Putzaufgabe löschen (anderes WG-Mitglied)](#delete-task-other-member)).

![PutzplanCard](assets/images/putzplan/task_completed.png)
![PutzplanCardCompleted](assets/images/putzplan/task_completed_progressbar.png)

## InnovationBoard

Das Prinzip ist das gleiche wie im Putzplan. Man sieht ein leeres InnovationBoard, in dem man mit dem blauen Button oben rechts ("✨Neue Idee") Ideen für die WG erstellen kann.

![InnoboardEmpty](assets/images/innoboard/inno_empty.png)

Der User klickt auf den Button und bekommt ein Modal angezeigt, wo er/sie den Titel seiner/ihrer Idee und die Beschreibung dazu eintragen kann. Zuzüglich hat der User eine breite Palette an Akzentfarben zum Auswählen für die individuelle Idee-Card.

![InnoModal](assets/images/innoboard/inno_modal.png)

So kann ein beispielhaftes, ausgefülltes Modal aussehen:

![InnoModalFilled](assets/images/innoboard/modal_filled.png)

Der User klickt auf Erstellen und bekommt seine Card mit der gewünschten Akzentfarbe angezeigt. Er/Sie sieht einen Like-Counter oben links und einen löschen-Button oben rechts in der erstellten Idee-Card. In der Mitte ist der Content (Titel, Beschreibung und von wem diese Idee-Card wann erstellt wurde). Ganz unten nun die Kommentarsektion, die man aufklappt. Der User kann seine Idee selber liken oder kommentieren, aus Gründen der Logik wird das aber erst später mit einem weiteren WG-Mitglied demonstiert.

![InnoCardNormal](assets/images/innoboard/inno_card.png)
![InnoCardCommentscetion](assets/images/innoboard/innocard_commentsection.png)

Anschließend wechselt der User auf das ActivityBoard.

## ActivityBoard

Wie auch bei den vorherigen Seiten, ist die Seite leer. Der User wird eine Aktivität mithilfe des Buttons ("+ Neue Aktivität") oben rechts erstellen.

![ActivityEmpty](assets/images/activityboard/activity_empty.png)

Der User bekommt nun das Modal angezeigt, wo er die Daten eintragen kann. Dazu gehören: Ein Feld für den Titel der Aktivität, Beschreibung, zwei Felder für Daten mit spezifischer Uhrzeit, Ort und maximalen Teilnehmern (optional).

![ActivityModal](assets/images/activityboard/activity_modal.png)

Wie auch beim Putzplan, kann hier der User per Kalenderansicht bestimmen, wann die Aktivität stattfinden soll. Zusätzlich kommt noch die Tageszeit hinzu, die er/sie spezifizieren kann.

![ActivityModalDateFrom](assets/images/activityboard/activity_modal_date_from.png)
![ActivityModalDateTo](assets/images/activityboard/activity_modal_date_to.png)

So kann ein beispielhaft ausgefülltes Modal aussehen (mit maximalen Teilnehmern):

![ActivityModalFilled](assets/images/activityboard/activity_modal_filled.png)

Der User klickt nun auf den Button "Aktivität hinzufügen" und bekommt eine Activity-Card angezeigt mit der Beschreibung und den angegebenen Daten. Oben rechts auf der Card gibt es wie gewohnt den Löschen-Button (wie bei den anderen aus Demonstrationsgründen nicht genutzt), sowie den 📅 Kalender-Export-Button (.ics), über den die Aktivität als ICS-Datei heruntergeladen und in Google/Apple/Outlook importiert werden kann. Unten rechts befindet sich der "Join" bzw. "Leave"-Button. Der User klickt auf ihn tritt der Aktivität bei. Wenn der User doch keine Lust auf diese Aktivität hat, kann er/sie immer verlassen, der Button ändert sich dementsprechend.

![ActivityCard](assets/images/activityboard/activity_card.png)

Der User tritt über den Join-Button einer Aktivität bei.

![ActivityJoined](assets/images/activityboard/activity_joined.png)

Der User will diese Aktivität als Kalender-Export haben. Dafür klickt er/sie auf den entsprechenden Button 📅 und bekommt eine .ics-Datei als Download.

![ActivityCalendarDownload](assets/images/activityboard/activity_ics_download.png)

Aus Demonstrationszwecken wird hier der Prozess des Imports übersprungen und Microsoft Outlook benutzt.
Die Aktivität mit all ihren Daten wird nun im Kalender angezeigt:

![ActivityInCalendar](assets/images/activityboard/activity_in_calendar.png)

Der User verlässt nun die Aktivität:

![ActivityLeft](assets/images/activityboard/activity_left.png)

Im Folgenden will der User Produkte zum Einkaufen anlegen. Dazu wechselt er/sie auf die Einkaufsliste.

## Einkaufsliste

![EinkaufslisteEmpty](assets/images/einkaufsliste/einkaufsplan_empty.png)

Der Einkaufsplan ist sehr simpel. Der User gibt die Bezeichnung des Produkts ins Eingabefeld "Artikel hinzufügen..." ein und gibt die Menge an.
Um das Produkt hinzuzufügen, klickt der User auf den blauen "+" Button daneben.

So kann eine Produkteingabe beispielsweise aussehen:
![EinkaufItem](assets/images/einkaufsliste/sample_item_einkauf.png)

Und so kann ein beispielhaftes Produkt aussehen:
![EinkaufsItemActual](assets/images/einkaufsliste/sample_item_actual.png)

Der User sieht, wer zuständig ist für dieses Produkt. Diese Funktion ist dazu intendiert, dass man z.B. eine gemeinsame Feier plant und die Produkte für diese Feier zusammen kauft, daher wird der zuständige User zufällig aus der WG ausgewählt. Sollte ein User zu viele Produkte zum Einkaufen haben und sich beschweren, kann man entweder das Produkt neu anlegen oder sich darauf einigen, dass es doch jemand anderes besorgt.

Anschließend geht der User zurück auf das Dashboard und sieht die allgemeine Übersicht: die Anzahl der offenen Putzaufgaben (bei denen der spezifische User zuständig ist), neuen Ideen, bevorstehenden Aktivitäten und Einkaufsartikeln, die vom User noch einzukaufen sind, letzte Aktivitäten der WG allgemein, Hinweise (z.B. diverse Erinnerungen) und die WG-Mitglieder unten.
![dashboard](assets/images/dashboard/dashboard_filled.png)
![WgMember](assets/images/dashboard/wg_member.png)

## Kooperation in der Wohngemeinschaft

Da ein integraler Bestandteil des WG-Lebens das Zusammenleben der WG-Mitgliedern ist, haben wir das Programm so gestaltet, dass es mehrere Mitglieder in einer WG geben kann, die zur selben Zeit verschiedene Sachen machen können. Aus Demonstrationsgründen werden im Folgenden nur die wichtigsten Features des Kollaborations-Features gezeigt.

Ein anderes Mitglied der WG erstellt sich einen Account und will der bisherigen Beispiel-WG beitreten:
![JoinWG](assets/images/wg_creation_or_join/invitation_code_eingabe.png)

Das zweite Mitglied landet auf dem Dashboard und sieht die bisherigen Informationen und letzte Begebenheiten der WG.
![2ndUserDashboard](assets/images/dashboard/2nd_user_dashboard.png)

<a id="wg-scope"></a>
Anschließend möchte das 2. Mitglied eine **Putzaufgabe** im **Putzplan** erstellen, es kann, wie bereits erwähnt, nur WG-Mitglieder dieser WG zum zuständig sein auswählen:
![2ndUserPutzplan](assets/images/putzplan/2nd_user_add_task.png)

Weiteres WG-Mitglied erstellt neue Putzaufgabe und sieht, wieviele Tasks noch offen sind.
![2ndUserTask](assets/images/putzplan/collab_putzplan.png)

<a id="delete-task-other-member"></a>
Das zweite WG-Mitglied will eine Putzaufgabe von einem weiteren WG-Mitglied löschen, was nicht möglich ist. Das geschieht ebensfalls bei dem InnovationBoard (Ideen) und ActivityBoard (Aktivitäten), dies wird aber aus Simplizitätsgründen übersprungen, da dies eine repetitive Funktion darstellt.
![2ndUserDeleteTask](assets/images/putzplan/danger_msg_putzplan.png)

Im **InnovationBoard** kann das 2. WG-Mitglied jetzt den Vorschlag von Mars liken und kommentieren (Klick auf "Kommentare", Dropdown), und selber einen Vorschlag posten (übersprungen, da selber Erstellprozess):
![InnoLikeAndComment](assets/images/innoboard/comment_like.png)
![InnoCommented](assets/images/innoboard/commented_inno.png)
![InnoFromOtherMember](assets/images/innoboard/inno_from_second_user.png)

Im **ActivityBoard** tritt das Mitglied einer Aktivität bei:
![activityJoined](assets/images/activityboard/ActivityJoined.png)
...und kann sie wieder verlassen:
![activityLeft](assets/images/activityboard/activityLeft.png)
Es kann auch eine neue Aktivität erstellen:
![activityCreateNew](assets/images/activityboard/activity_new.png)

Im **Einkaufsplan** kann das weitere WG-Mitglied neue Produkte hinzufügen:
![ShoppingItemPlus](assets/images/einkaufsliste/newShoppingItem.png)

Am Ende kehrt das weitere WG-Mitglied auf das **Dashboard** zurück und sieht die Übersicht mit den **aktualisierten Informationen** (individuelle Aufgaben und letzte Aktivitäten)
![dashboardFilled2](assets/images/dashboard/dashboard2ndMember.png)
![WGMembers](assets/images/dashboard/wg_members_refreshed.png)

{: .fs-2 }
Last build: {{ site.time | date: '%d %b %Y, %R%:z' }}