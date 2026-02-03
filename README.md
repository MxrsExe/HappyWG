# Web-Development-Project Happy WG

## **Local Setup** 
1. Repository klonen
2. Virtuelle Umgebung erstellen & aktivieren (Windows: `python -m venv venv` **ODER** auf MacOS/Linux: `python3 -m venv .venv`, dann `source .venv/bin/activate`)
3. Dependencies installieren (pip install -r requirements.txt)
4. DB initialisieren / Migrationen ausführen (im Terminal mit venv aktiv: `flask init-db`)
5. App starten

Wie man Flask Migrate benutzt (zum Tabellen ändern, droppen etc.)

Sollte das Terminal sowas werfen:

"`ERROR [flask_migrate] Error: Target database is not up to date.`" (aber man weiß, dass die Datenbank auf dem neusten Stand ist, Alembic hängt aber hinterher)
Grund: Durch `with app.app_context(): db.create_all()` in app.py wurde die Datenbank schon initialisiert

Fix: Neuen Head machen von der aktuellen Datenbank im Root-Verzeichnis (z.B. hier .../Web-Development-Project (Daten behalten))

Im Terminal: `flask --app app db stamp head`

Prüfen:
`flask --app app db current`
`flask --app app db heads`
(Beides sollte übereinstimmen)

dann:
`flask --app app db revision -m "Was ist in dieser DB-Revision"`
`flask --app app db upgrade`