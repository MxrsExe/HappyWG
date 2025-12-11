import sqlite3

from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



def db_connection():
    if 'db_con' not in g:
        g.db_con = sqlite3.connect(current_app.config['DATABASE'])
    return db_con

def db_close(db_con):
    db_con = g.pop('db_con', None)
    if db_con is not None:
        db_con.close()

sql_query = "SELECT * FROM list ORDER BY name;"

db_con = db_connection()
lists = db_con.execute(sql_query)
db_close(db_con)