from flask import render_template, flash, redirect, url_for
from app import app, db
from app.models import Item, Transaction
from app.forms import AddItemForm

@app.route('/')
@app.route('/index')
def index():
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
        return redirect('/index')

    return render_template('additem.html', title='Add item', form=form)