from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, DateField, HiddenField
from wtforms.validators import DataRequired

class AddAccount(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add')

class AddItemForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    amount = IntegerField('Amount', validators=[DataRequired()])
    recurring = BooleanField('Recurring')
    repeat_dom = IntegerField('Repeat DOM')
    submit = SubmitField('Submit')