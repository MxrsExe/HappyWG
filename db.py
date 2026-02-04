# import sqlite3

# from flask import current_app, g
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()



from datetime import datetime
import click

# We import SQLAlchemy from the Flask-SQLAlchemy package, and also the object app from our own app module (i.e., from file 📄app.py).
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

activity_participants = db.Table(
    "ACTIVITY_PARTICIPANTS",
    db.Column("activity_id", db.Integer, db.ForeignKey("ACTIVITY.activity_id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("USER.user_id"), primary_key=True),
    )

class User(db.Model):
    __tablename__ = 'USER'
    user_id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    wg_id = db.Column(db.Integer, db.ForeignKey('WG.wg_id'), nullable=True)
    role = db.Column(db.String, nullable=False, default='member')  #roles implemented: member (further implementation of others roles possible)
    #Beziehungen
    wg = db.relationship('Wg', back_populates='users')
    cleaning_tasks = db.relationship('CleaningTask', back_populates='assigned_user')
    activities_created = db.relationship('Activity', back_populates='creator')
    ideas = db.relationship('Idea', back_populates='creator',foreign_keys='Idea.created_by')
    idea_comments = db.relationship('Idea_Comment', back_populates='user')
    idea_likes = db.relationship('Idea_Like', back_populates='user')
    added_items = db.relationship('ShoppingItem', foreign_keys='ShoppingItem.added_by', back_populates='added_by_user')
    assigned_items = db.relationship('ShoppingItem', foreign_keys='ShoppingItem.assigned_to', back_populates='assigned_to_user')

    
    joined_activities = db.relationship(
        "Activity",
        secondary=activity_participants,
        back_populates="participants"
    )  #joined_activities

class Wg(db.Model):
    __tablename__ = 'WG'
    wg_id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    invite_code = db.Column(db.String(6), nullable=True)

    #Beziehungen
    shopping_items = db.relationship('ShoppingItem', back_populates='wg', cascade='all, delete-orphan')
    users = db.relationship('User', back_populates='wg')
    cleaning_templates = db.relationship('CleaningTemplate', back_populates='wg', cascade='all, delete-orphan')
    activities = db.relationship('Activity', back_populates='wg', cascade='all,delete-orphan')
    ideas = db.relationship('Idea', back_populates='wg', cascade='all, delete-orphan')

class ShoppingItem(db.Model):
    __tablename__ = 'SHOPPING_ITEM'
    item_id = db.Column(db.Integer, primary_key=True, index=True)
    wg_id = db.Column(db.Integer, db.ForeignKey('WG.wg_id'), nullable=False)
    added_by = db.Column(db.Integer, db.ForeignKey('USER.user_id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('USER.user_id'), nullable=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    #Beziehungen
    wg = db.relationship('Wg', back_populates='shopping_items')
    added_by_user = db.relationship('User', foreign_keys=[added_by], back_populates='added_items')
    assigned_to_user = db.relationship('User', foreign_keys=[assigned_to], back_populates='assigned_items')

class CleaningTemplate(db.Model):
    __tablename__ = 'CLEANING_TEMPLATE'
    template_id = db.Column(db.Integer, primary_key=True, index=True)
    wg_id = db.Column(db.Integer, db.ForeignKey('WG.wg_id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    frequency = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    #Beziehungen
    wg = db.relationship('Wg', back_populates='cleaning_templates')
    tasks = db.relationship('CleaningTask', back_populates='template', cascade='all, delete-orphan')

class CleaningTask(db.Model):
    __tablename__ = 'CLEANING_TASK'
    task_id = db.Column(db.Integer, primary_key=True, index=True)
    template_id = db.Column(db.Integer, db.ForeignKey('CLEANING_TEMPLATE.template_id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('USER.user_id'), nullable=False)
    status = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime)
    notes = db.Column(db.String)
    #Beziehungen   
    template = db.relationship('CleaningTemplate', back_populates='tasks')
    assigned_user = db.relationship('User', back_populates='cleaning_tasks')

class Activity(db.Model):
    __tablename__ = 'ACTIVITY'
    activity_id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    wg_id = db.Column(db.Integer, db.ForeignKey('WG.wg_id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('USER.user_id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String)
    max_participants = db.Column(db.Integer, nullable=True)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    date_to = db.Column(db.DateTime, nullable=False)  
    #Beziehungen
    participants = db.relationship(
        "User",
        secondary=activity_participants,
        back_populates="joined_activities"
    )  #participants 
    wg = db.relationship('Wg', back_populates='activities')
    creator = db.relationship('User', back_populates='activities_created')
    
    

class Idea(db.Model):
    __tablename__ = 'IDEA'
    idea_id = db.Column(db.Integer, primary_key=True, index=True)
    wg_id = db.Column(db.Integer, db.ForeignKey('WG.wg_id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('USER.user_id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    status = db.Column(db.String)
    color = db.Column(db.String(7), nullable=False, default="#ffffff")
    #Beziehungen
    wg = db.relationship('Wg', back_populates='ideas')
    creator = db.relationship('User', back_populates='ideas', foreign_keys=[created_by])
    comments = db.relationship('Idea_Comment', back_populates='idea', cascade='all, delete-orphan')
    likes = db.relationship('Idea_Like', back_populates='idea', cascade='all, delete-orphan')

class Idea_Comment(db.Model):
    __tablename__ = 'IDEA_COMMENT'
    comment_id = db.Column(db.Integer, primary_key=True, index=True)
    idea_id = db.Column(db.Integer, db.ForeignKey('IDEA.idea_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    #Beziehungen
    idea = db.relationship('Idea', back_populates='comments')
    user = db.relationship('User', back_populates='idea_comments')

class Idea_Like(db.Model):
    __tablename__ = 'IDEA_LIKE'
    like_id = db.Column(db.Integer, primary_key=True, index=True)
    idea_id = db.Column(db.Integer, db.ForeignKey('IDEA.idea_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), nullable=False)
    #Beziehungen
    idea = db.relationship('Idea', back_populates='likes')
    user = db.relationship('User', back_populates='idea_likes')
    

