# import sqlite3

# from flask import current_app, g
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()




import click

# We import SQLAlchemy from the Flask-SQLAlchemy package, and also the object app from our own app module (i.e., from file 📄app.py).
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm
from app import app

# Next, we store the database location as configuration value in app.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///happywg.sqlite'

# Then, we create the instance db of class SQLAlchemy, which gives us access to the Flask-SQLAlchemy functionality.
db = SQLAlchemy()

# Lastly, we associate db with app by calling db.init_app().
db.init_app(app)

class User(db.Model):
    __tablename__ = 'USER'
    user_id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.String, nullable=False)
    #Beziehungen
    added_items = db.relationship('ShoppingItem', foreign_keys='ShoppingItem.added_by')
    assigned_items = db.relationship('ShoppingItem', foreign_keys='ShoppingItem.assigned_to')

    wg = db.relationship('Wg', back_populates='users')


class Wg(db.Model):
    __tablename__ = 'WG'
    wg_id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    #Beziehungen
    shopping_items = db.relationship('ShoppingItem', back_populates='wg', cascade='all, delete-orphan')

    users = db.relationship('User', back_populates='wg')
    


class ShoppingItem(db.Model):
    __tablename__ = 'SHOPPING_ITEM'
    item_id = db.Column(db.Integer, primary_key=True, index=True)
    wg_id = db.Column(db.Integer, db.ForeignKey('WG.wg_id'), nullable=False)
    added_by = db.Column(db.Integer, db.ForeignKey('USER.user_id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('USER.user_id'))
    name = db.Column(db.String, nullable=False)
    quantity= db.Column(db.String)
    #Beziehungen
    wg = db.relationship('Wg', back_populates='shopping_items')
    added_by_user=db.relationhip('User', foreign_keys[added_by])
    assigned_to_user=db.relationship('User', foreign_keys=[assigned_to])




    

    
















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