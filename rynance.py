from app import app, db
from app.models import Item, Account, Ledger, LedgerEntry

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Item': Item, 'Account': Account, 'Ledger': Ledger, 'LedgerEntry': LedgerEntry}