from enum import unique
from app import db
from datetime import datetime

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    recurring = db.Column(db.Boolean)
    repeat_dom = db.Column(db.Integer)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(512))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
