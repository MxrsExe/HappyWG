#run sql commands

import sqlite3
import sys

#Quelle: VS-Code Autocomplete, Java-Wissen & https://www.geeksforgeeks.org/python/how-to-use-sys-argv-in-python/ (insb. sys.argv[]) 
# & Inspiration aus https://hwrberlin.github.io/fswd/fswd-intro.html#34-populate-the-database-with-a-sample-data-set
db_path = sys.argv[1]
sql_path = sys.argv[2]

with open (sql_path, 'r') as f:
    sql_script = f.read()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
try:
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

except Exception as e:
    print(f"Fehler beim Ausführen des SQL-Skripts: {e}")
    conn.rollback()
    
finally:
    conn.close()