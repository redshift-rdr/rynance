from flask import render_template, flash, redirect, url_for, session
from app import app, db
from app.models import Item, Account
from app.forms import AddItemForm, AddAccount, ChooseAccount

@app.route('/')
@app.route('/index')
def index():
    if not session['account']:
        accounts = Account.query.all()

        if not accounts:
            return redirect(url_for('addaccount'))
        else:
            return redirect(url_for('chooseaccount'))

    items = Item.query.all()

    return render_template('index.html', title='Home', items=items)

@app.route('/additem', methods=['GET', 'POST'])
def additem():
    form = AddItemForm()

    if form.validate_on_submit():
        item = Item(name=form.name.data, 
                    description=form.description.data, 
                    amount=form.amount.data, 
                    recurring=form.recurring.data, 
                    repeat_dom=form.repeat_dom.data,
                    repeat_end=form.repeat_end.data)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('additem'))

    return render_template('additem.html', title='Add item', form=form)

@app.route('/addaccount', methods=['GET', 'POST'])
def addaccount():
    form = AddAccount()

    if form.validate_on_submit():
        account = Account(name=form.name.data)
        session['account'] = account
        db.session.add(account)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('addaccount.html', title='Add account', form=form)
    
@app.route('/chooseaccount', methods=['GET', 'POST'])
def chooseaccount():
    accounts = Account.query.all()

    form = ChooseAccount()

    return render_template('chooseaccount.html', title='Choose account', accounts=accounts, form=form)