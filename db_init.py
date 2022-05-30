from app import app, db
from app.models import Profile, RecurringRecord, Ledger, Record
from datetime import datetime

ryan = Profile(name='ryan')
salary_recurring = RecurringRecord(name='salary', description='salary', amount=2000, recurring_dom=6, profile=ryan)
june = Ledger(month=datetime.utcnow(), profile=ryan)
salary = Record(name=salary_recurring.name, description=salary_recurring.description, amount=salary_recurring.amount, ledger=june)

db.session.add_all([ryan, salary_recurring, june, salary])
db.session.commit()