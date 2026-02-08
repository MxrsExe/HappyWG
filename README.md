# Happy WG

Readme-Quelle (Aufbau): https://github.com/hwrberlin/fswd-app/blob/main/README.md?plain=1

Diese Repository beinhaltet das Projekt "HappyWG" und alle damit verbundenen Dokumentationsdateien und Code (inkl. Bilder, Markdown etc.).


## **Local Setup** 
**Step 1: Repository klonen:** `git clone HappyWG`

**Step 2:** Virtuelle Umgebung erstellen & aktivieren (Windows: `python -m venv venv` **ODER** auf MacOS/Linux: `python3 -m venv .venv`, dann `source .venv/bin/activate`)

**Step 3:** Im Virtual Environment Dependencies installieren (`pip install -r requirements.txt`):

```console
(venv) C:\Users\...\Web-Development-Project> pip install -r requirements.txt
```

> File `📄requirements.txt` erstellt mit diesem Command: `pip freeze > requirements.txt`

**Step 4:** DB initialisieren (im Terminal mit venv aktiv: `flask init-db`)

```console
(venv) PS C:\Users\...\Web-Development-Project> flask init-db
Database has been initialized.
```

**Step 5:**. App starten (`flask run --reload`)

```console
(venv) PS C:\Users\...\Web-Development-Project> flask run --reload
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
```

## Quellen

Alle Quellen bzw. LLM Prompts sind möglichst genau im Code als Kommentar (#) angegeben (z.B. "Quelle: ChatGPT (Prompt: ...)") und getrennt ("#--------"). 
Für weitere Informationen zu den Quellen bzw. LLM-Prompts, siehe die jeweiligen PDFs (unter docs/llm_prompts_files/).

**Links zu den ChatGPT Chats**:

https://chatgpt.com/g/g-p-6939dcde8a988191b6a437cd1a09b6e5-web-app/project

**Weitere Quellensammlung**:

Eck, Alexander (2024): "fwsd-app": https://github.com/hwrberlin/fswd-app/tree/main 
(Struktur der App) (Letzter Zugriff: 07.02.2026)

Eck, Alexander (2024) "Project Name": https://hwrberlin.github.io/fswd-app/
(Inhalt) (Letzter Zugriff: 07.02.2026)

Eck, Alexander (2025) "Full-Stack Web Dev @HWR Berlin": https://hwrberlin.github.io/fswd/ (Alle Überschriften "Python + VS Code Setup" bis "Design Decisions")
(Lehrmaterial) (Letzter Zugriff: 07.02.2026)

"datetime — Basic date and time types" (o.D): ttps://docs.python.org/3/library/datetime.html (Letzter Zugriff: 27.01.2026)

Göbel, Stefan (2018): "Was ist das N+1 Query Problem?": https://www.stefan-goebel.com/2018/was-ist-das-n1-query-problem/ (Letzter Zugriff: 04.02.2026)

Bootstrap-Theme: https://bootswatch.com/zephyr/ (Letzter Zugriff: 16.01.2026)

GeeksforGeeks. Generate random string of given length. Abschnitt: “Using random.choices()”, (last updated: 11.07.2025)
https://www.geeksforgeeks.org/python/python-generate-random-string-of-given-length/, (Zugriff: 10.01.2026)

Stack Overflow. (2014). How do I clear a flask session?
https://stackoverflow.com/questions/27747578/how-do-i-clear-a-flask-session
(Zugriff: 13.01.2026)


