from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired

class AddItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    amount = IntegerField('Amount', validators=[DataRequired()])
    recurring = BooleanField('Recurring')
    repeat_dom = IntegerField('Repeat DOM')
    repeat_end = DateField('Repeat End')
    submit = SubmitField('Add')