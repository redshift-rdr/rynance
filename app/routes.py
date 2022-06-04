from flask import render_template, flash, redirect, request, url_for, session, make_response
from app import app, db
from app.models import Profile, RecurringRecord, Ledger, Record
from app.forms import AddItemForm, AddProfile
from sqlalchemy import extract
from datetime import datetime, timedelta

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

    # get the ledger for the current month from the db
    thismonth = get_current_month()

    # calculate totals
    totals = {}
    if thismonth:
        totals['disposable'] = sum([t.amount for t in thismonth.records])
        totals['income'] = sum([t.amount if (t.amount > 0) else 0 for t in thismonth.records])
        totals['expenses'] = sum([t.amount if (t.amount < 0) else 0 for t in thismonth.records])

    return render_template('index.html', title='Home', ledger=thismonth, totals=totals)

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

"""
@app.route('/items', methods=['GET', 'POST'])
def items():
    items = db.session.query(Item).filter_by(active=True).all()
    return render_template('items.html', items=items)

@app.route('/edititem', methods=['GET', 'POST'])
def edititem():
    item_id = request.args.get('item_id')
    item = db.session.query(Item).filter_by(uuid=item_id).first()
    form = AddItemForm(obj=item)

    if request.method == 'POST':
        if form.uuid.data and db.session.query(Item).filter_by(uuid=form.uuid.data).first(): 
            item = db.session.query(Item).filter_by(uuid=form.uuid.data).first()
            item.name = form.name.data
            item.description = form.description.data
            item.amount = form.amount.data
            item.recurring = form.recurring.data
            item.repeat_dom = form.repeat_dom.data

            db.session.add(item)
            db.session.commit()

            flash('edit successful') 
            return redirect(url_for('edititem'))

        flash('edit failed')
    
    return render_template('edititem.html', item=item, form=form)

@app.route('/additem', methods=['GET', 'POST'])
def additem():
    form = AddItemForm()

    if form.validate_on_submit():
        item = Item(name=form.name.data, 
                    description=form.description.data, 
                    amount=form.amount.data, 
                    recurring=form.recurring.data, 
                    repeat_dom=form.repeat_dom.data,
                    type=int(form.type.data),
                    period=form.period.data,
                    month=form.period.data,
                    account=db.session.query(Account).filter_by(uuid=session['account_id']).first())

        item.active = item.recurring
        db.session.add(item)

        thismonth = get_current_month()
        if item.type == 1:
            entry = LedgerEntry(ledger=thismonth, item=item, name=item.name, amount=item.amount, description=item.description)
            db.session.add(entry)
        if item.type == 2 and (item.month == datetime.utcnow().month):
            entry = LedgerEntry(ledger=thismonth, item=item, name=item.name, amount=item.amount, description=item.description)
            db.session.add(entry)
        

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('additem.html', title='Add item', form=form)

@app.route('/deleteitem')
def deleteitem():
    item_id = request.args.get('item_id')

    if item_id and db.session.query(Item).filter_by(uuid=item_id):
        item = db.session.query(Item).filter_by(uuid=item_id).first()
        item.active = False
        db.session.add(item)
        db.session.commit()

        flash('item deleted')
    else:
        flash('item_id not provided or invalid')

    return redirect(url_for('items'))


"""
def addmonth(profile_id : str, month : datetime) -> Ledger:
    ledger = Ledger(month=month, profile=db.session.query(Profile).filter_by(uuid=profile_id).first())
    db.session.add(ledger)

    recurring = db.session.query(RecurringRecord).all()
    for item in recurring:
        entry = Record(ledger=ledger, name=item.name, description=item.description, amount=item.amount, recurring_dom=item.recurring_dom)
        db.session.add(entry)

    db.session.commit()
    return ledger

def get_current_month() -> Ledger:
    if not 'profile_id' in session:
        return []

    return get_month(session['profile_id'], datetime.utcnow())

def get_month(profile_id : str, month : datetime) -> Ledger:
    m, y = (month.month, month.year)

    profile = db.session.query(Profile).filter_by(uuid=profile_id).first()
    ledger = db.session.query(Ledger).filter_by(profile=profile).filter(extract('year', Ledger.month)==y).filter(extract('month', Ledger.month)==m).first()

    if not ledger:
        ledger = addmonth(session['profile_id'], month)

    return ledger
