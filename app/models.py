from app import db
from datetime import datetime

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    items = db.relationship('Item', backref='account', lazy='dynamic')
    ledgers = db.relationship('Ledger', backref='account', lazy='dynamic')

    def __repr__(self):
        return f'Account<{self.name}>'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    recurring = db.Column(db.Boolean, default=False)
    repeat_dom = db.Column(db.Integer)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(512))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __repr__(self):
        return f'Item<{self.name}>'

class LedgerEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    item = db.relationship("Item")

    ledger_id = db.Column(db.Integer, db.ForeignKey('ledger.id'))

    def __repr__(self):
        return f'LedgerEntry<ledger: {self.ledger_id}, item: {self.item_id}>'

class Ledger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Date)
    entries = db.relationship('LedgerEntry', backref='ledger', lazy='dynamic')
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __repr__(self):
        return f'Ledger<{self.month}>'

