from enum import unique
from app import db
from datetime import datetime

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)

    def __repr__(self):
        return f'Account({self.name})'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    recurring = db.Column(db.Boolean)
    repeat_dom = db.Column(db.Integer)
    repeat_end = db.Column(db.Date)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(512))
    # TODO: link this to account id

    def __repr__(self):
        return f'Item({self.name})'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    date = db.Column(db.Date, index=True)

    def __repr__(self):
        return f'Transaction({self.date} : {self.amount})'
