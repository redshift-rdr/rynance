from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, DateField, HiddenField
from wtforms.validators import DataRequired

class AddAccount(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add')

class ChooseAccount(FlaskForm):
    accountid = HiddenField('accountid')
    submit = SubmitField('Choose')

class AddItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    amount = IntegerField('Amount', validators=[DataRequired()])
    recurring = BooleanField('Recurring')
    repeat_dom = IntegerField('Repeat DOM')
    repeat_end = DateField('Repeat End')
    submit = SubmitField('Add')