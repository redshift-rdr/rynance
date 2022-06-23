from flask import render_template, flash, redirect, request, url_for, session, make_response
from app import app, db
from app.models import Profile, RecurringRecord, Ledger, Record
from app.forms import AddRecurringRecordForm, AddRecordForm, AddProfile
from sqlalchemy import extract
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class LedgerInfo:
    def __init__(self, ledger_model):
        self.ledger = ledger_model

        self.month = self.ledger.month
        self.prev_month = self.month - relativedelta(months=1)
        self.prev_month_str = f'{self.prev_month.month}-{self.prev_month.year}'
        self.next_month = self.month + relativedelta(months=1)
        self.next_month_str = f'{self.next_month.month}-{self.next_month.year}'
        self.today = datetime.utcnow()
        self.calc_totals()

    def calc_totals(self):
        self.disposable_income = 0
        self.total_income = 0
        self.total_expenses = 0
        self.bank_balance = 0

        for record in self.ledger.records:
            # disposable income is income - expenses
            #   as expenses are stored as negative numbers we can just add them all up
            self.disposable_income += record.amount

            # to get total income we add up all positive amounts
            #   as incomes are stored as positive numbers
            if record.amount > 0:
                self.total_income += record.amount

            # to get total expenses we add up all negative amounts
            #   as expenses are stored as negative numbers
            if record.amount < 0:
                self.total_expenses += record.amount

            # bank balance will be income to date - expenses to date
            #   the figure is meant to reflect the amount of money in the bank account
            if record.recurring_dom < self.today.day:
                self.bank_balance += record.amount
            

@app.route('/')
@app.route('/index')
def index():
    if request.cookies.get('profile_id'):
        session['profile_id'] = request.cookies.get('profile_id')

    if not 'profile_id' in session:
        profiles = Profile.query.all()

        if not profiles:
            return redirect(url_for('addprofile'))
        else:
            return redirect(url_for('chooseprofile'))

    month_select = request.args.get('month')
    if month_select:
        if '-' in month_select: 
            m,y = month_select.split('-')
            date_select = datetime(year=int(y), month=int(m), day=1)
            print(date_select)
            thismonth = get_month(session['profile_id'], date_select)
        else:
            thismonth = get_current_month()
    else:
        # get the ledger for the current month from the db
        thismonth = get_current_month()

    # calculate totals
    totals = {}
    if thismonth:
        ledger_info = LedgerInfo(thismonth)
        #totals['disposable'] = sum([t.amount for t in thismonth.records])
        #totals['income'] = sum([t.amount if (t.amount > 0) else 0 for t in thismonth.records])
        #totals['expenses'] = sum([t.amount if (t.amount < 0) else 0 for t in thismonth.records])
        #totals['todate'] = sum([t.amount if ((t.recurring_dom <= today_dom) and (t.amount > 0)) else 0 for t in thismonth.records]) + sum([t.amount if ((t.recurring_dom <= today_dom) and (t.amount < 0)) else 0 for t in thismonth.records])
    else:
        ledger_info = None

    return render_template('index.html', title='Home', ledger=thismonth, ledger_info=ledger_info)

@app.route('/addprofile', methods=['GET', 'POST'])
def addprofile():
    form = AddProfile()

    if form.validate_on_submit():
        profile = Profile(name=form.name.data)
        session['profile_id'] = profile.uuid
        db.session.add(profile)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('addprofile.html', title='Add profile', form=form)
    
@app.route('/chooseprofile', methods=['GET'])
def chooseprofile():
    profiles = Profile.query.all()
    profile_id = request.args.get('profile_id')

    if db.session.query(Profile).filter_by(uuid=profile_id).first():
        session['profile_id'] = profile_id
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('profile_id', profile_id, expires=datetime.now() + timedelta(days=30))
        return resp

    return render_template('chooseprofile.html', title='Choose profile', profiles=profiles)


@app.route('/addrecord', methods=['GET', 'POST'])
def addrecord():
    form = AddRecordForm()

    thismonth = get_current_month()

    if form.validate_on_submit():
        if form.recurring.data:
            amount = normalise_amount(form.amount.data, form.type.data)
            rrecord = RecurringRecord(name=form.name.data, 
                        description=form.description.data, 
                        amount=amount,  
                        recurring_dom=form.recurring_dom.data,
                        profile=db.session.query(Profile).filter_by(uuid=session['profile_id']).first())

            db.session.add(rrecord)

            thismonth = get_current_month()

            if form.addthismonth.data:
                record = Record(ledger=thismonth, name=rrecord.name, description=rrecord.description, amount=rrecord.amount, recurring_dom=rrecord.recurring_dom)
                db.session.add(record)

        else:
            amount = normalise_amount(form.amount.data, form.type.data)
            record = Record(name = form.name.data,
                            description = form.description.data,
                            amount = amount,
                            recurring_dom = form.recurring_dom.data,
                            ledger = thismonth,
                            payment_method=form.payment_method.data)
            db.session.add(record)
            
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('addrecord.html', title='Add Record', form=form)


@app.route('/recurring', methods=['GET', 'POST'])
def recurring_records():
    profile_id = session['profile_id']
    profile = db.session.query(Profile).filter_by(uuid=profile_id).first()
    recurring_records = db.session.query(RecurringRecord).filter_by(profile_id=profile.id).all()
    return render_template('items.html', recurring_records=recurring_records)

@app.route('/editrecurring', methods=['GET', 'POST'])
def editrecurring():
    item_id = request.args.get('rrecord_id')
    item = db.session.query(RecurringRecord).filter_by(uuid=item_id).first()
    form = AddRecurringRecordForm(obj=item)

    if request.method == 'POST':
        amount = normalise_amount(form.amount.data, form.type.data)
        if form.uuid.data and db.session.query(RecurringRecord).filter_by(uuid=form.uuid.data).first(): 
            item = db.session.query(RecurringRecord).filter_by(uuid=form.uuid.data).first()
            item.name = form.name.data
            item.description = form.description.data
            item.amount = amount
            item.recurring_dom = form.recurring_dom.data
            item.payment_method = form.payment_method.data

            db.session.add(item)
            db.session.commit()

            flash('edit successful') 
            return redirect(url_for('editrecurring'))

        flash('edit failed')
    
    return render_template('edititem.html', item=item, form=form)

@app.route('/editrecord', methods=['GET', 'POST'])
def editrecord():
    record_id = request.args.get('record_id')
    record = db.session.query(Record).filter_by(uuid=record_id).first()
    form = AddRecordForm(obj=record)

    if request.method == 'POST':
        amount = normalise_amount(form.amount.data, form.type.data)
        if form.uuid.data and db.session.query(Record).filter_by(uuid=form.uuid.data).first():
            record = db.session.query(Record).filter_by(uuid=form.uuid.data).first()
            record.name = form.name.data
            record.description = form.description.data
            record.amount = amount
            record.recurring_dom = form.recurring_dom.data
            record.paid = form.paid.data

            db.session.add(record)
            db.session.commit()

            flash('edit successful')
            return redirect(url_for('index'))

        flash('edit failed')

    return render_template('editrecord.html', record=record, form=form)


@app.route('/deleterecurring')
def deleterecurring():
    rrecord_id = request.args.get('rrecord_id')

    if rrecord_id and db.session.query(RecurringRecord).filter_by(uuid=rrecord_id):
        db.session.query(RecurringRecord).filter_by(uuid=rrecord_id).delete()
        db.session.commit()

        flash('recurring record deleted')
    else:
        flash('rrecord not provided or invalid')

    return redirect(url_for('recurring_records'))

@app.route('/deleterecord')
def deleterecord():
    record_id = request.args.get('record_id')

    if record_id and db.session.query(Record).filter_by(uuid=record_id):
        db.session.query(Record).filter_by(uuid=record_id).delete()
        db.session.commit()

        flash('record deleted')
    else:
        flash('record not provided or invalid')

    return redirect(url_for('index'))


def addmonth(profile_id : str, month : datetime) -> Ledger:
    ledger = Ledger(month=month, profile=db.session.query(Profile).filter_by(uuid=profile_id).first())
    db.session.add(ledger)

    recurring = db.session.query(RecurringRecord).filter_by(uuid=profile_id).all()
    for item in recurring:
        entry = Record(ledger=ledger, name=item.name, description=item.description, amount=item.amount, recurring_dom=item.recurring_dom, payment_method=item.payment_method)
        db.session.add(entry)

    db.session.commit()
    return ledger

def get_current_month() -> Ledger:
    if not 'profile_id' in session:
        return []

    return get_month(session['profile_id'], datetime.utcnow(), create=True)

def get_month(profile_id : str, month : datetime, create : bool = False) -> Ledger:
    m, y = (month.month, month.year)

    profile = db.session.query(Profile).filter_by(uuid=profile_id).first()
    ledger = db.session.query(Ledger).filter_by(profile=profile).filter(extract('year', Ledger.month)==y).filter(extract('month', Ledger.month)==m).first()

    if not ledger and create:
        ledger = addmonth(session['profile_id'], month)

    return ledger

def normalise_amount(amount : int, type : str) -> int:
    if type == 'income':
        if amount < 0:
            return amount * -1
    elif type == 'expense':
        if amount > 0:
            return amount * -1

    return amount