from flask import render_template, flash, redirect, request, url_for, session
from app import app, db
from app.models import Item, Account, Ledger, LedgerEntry
from app.forms import AddItemForm, AddAccount
from sqlalchemy import extract
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    if not 'account_id' in session:
        accounts = Account.query.all()

        if not accounts:
            return redirect(url_for('addaccount'))
        else:
            return redirect(url_for('chooseaccount'))

    # get the ledger for the current month from the db
    thismonth = get_current_month()

    # calculate totals
    totals = {'total': sum([t.item.amount for t in thismonth.entries])}

    return render_template('index.html', title='Home', ledger=thismonth, totals=totals)

@app.route('/items', methods=['GET', 'POST'])
def items():
    items = Item.query.all()
    return render_template('items.html', items=items)

@app.route('/edititem', methods=['GET', 'POST'])
def edititem():
    item_id = request.args.get('item_id')
    item = Item.query.get(item_id)
    form = AddItemForm(obj=item)

    if request.method == 'POST':
        if form.id.data and Item.query.get(form.id.data):
            item = Item.query.get(form.id.data)
            item.name = form.name.data
            item.description = form.description.data
            item.amount = form.amount.data
            item.recurring = form.recurring.data
            item.repeat_dom = form.repeat_dom.data

            db.session.add(item)
            db.session.commit()

            flash('edit successful') 
            return redirect(url_for('index'))

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
                    account=Account.query.get(session['account_id']))

        db.session.add(item)

        thismonth = get_current_month()
        entry = LedgerEntry(ledger=thismonth, item=item)

        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('additem.html', title='Add item', form=form)

@app.route('/addaccount', methods=['GET', 'POST'])
def addaccount():
    form = AddAccount()

    if form.validate_on_submit():
        account = Account(name=form.name.data)
        session['account_id'] = account.id
        db.session.add(account)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('addaccount.html', title='Add account', form=form)
    
@app.route('/chooseaccount', methods=['GET'])
def chooseaccount():
    accounts = Account.query.all()
    account_id = request.args.get('account')

    if Account.query.get(account_id):
        session['account_id'] = account_id
        return redirect(url_for('index'))

    return render_template('chooseaccount.html', title='Choose account', accounts=accounts)

def addmonth(account_id : int, month : datetime) -> None:
    month = Ledger(month=month, account=Account.query.get(account_id))
    db.session.add(month)

    recurring = db.session.query(Item).filter(Item.recurring == True).all()
    for item in recurring:
        entry = LedgerEntry(item=item, ledger=month)
        db.session.add(entry)

    db.session.commit()

def get_current_month():
    m, y = (datetime.utcnow().month, datetime.utcnow().year)
    return db.session.query(Ledger).filter(extract('year', Ledger.month)==y).filter(extract('month', Ledger.month)==m).all()[0]