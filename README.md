# Web-Development-Project Happy WG

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


FÜR DIE QUELLEN: Alle Quellen sind möglichst genau im Code als Kommentar (#) angegeben und getrennt. 
Für weitere Informationen zu den Quellen bzw. LLM-Prompts, siehe die jeweiligen PDFs (unter docs/llm_prompts_files/).

Weiteres: Bei einigen Abschnitten könnte mehr LLM-Benutzung stattgefunden haben, da wir uns (vor allem am Anfang) unsicher waren oder nicht wussten, wie Sachen umzusetzen sind bzw. funktionieren, einiges konnte man nicht aus den Vorlesungsfolien entnehmen und LLMs eine sehr große Hilfe darstellen, wenn es um das Verständnis geht. 

In diesen Fällen haben wir die Hauptquelle angegeben, z.B. "ChatGPT", auch wenn es kleinere Hilfen von anderen Quellen gab 
(z.B. Fehlersuche, Syntax-Hilfe, Debugging-Hilfe, Prompt-Formulierungshilfe etc.).

Weitere Quellensammlung:
https://github.com/hwrberlin/fswd-app/tree/main (Struktur der App)
https://hwrberlin.github.io/fswd-app/
https://hwrberlin.github.io/fswd/ (Alle Überschriften "Python + VS Code Setup" bis "Design Decisions")
https://docs.python.org/3/library/datetime.html
https://www.stefan-goebel.com/2018/was-ist-das-n1-query-problem/

Bootstrap-Theme: https://bootswatch.com/zephyr/

