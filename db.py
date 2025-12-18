# import sqlite3

# from flask import current_app, g
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()
import click

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.sqlite'

db = SQLAlchemy()
db.init_app(app)

class Shopping_Category(db.Model):
    
# def db_connection():
#     if 'db_con' not in g:
#         g.db_con = sqlite3.connect(current_app.config['DATABASE'])
#     return db_con

# def db_close(db_con):
#     db_con = g.pop('db_con', None)
#     if db_con is not None:
#         db_con.close()

# sql_query = "SELECT * FROM list ORDER BY name;"

# db_con = db_connection()
# lists = db_con.execute(sql_query)
# db_close(db_con)