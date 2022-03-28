from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, DateField, HiddenField, FloatField, SelectField
from wtforms.validators import DataRequired, Optional

class AddAccount(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add')

class AddItemForm(FlaskForm):
    uuid = HiddenField('uuid')
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    amount = IntegerField('Amount', validators=[DataRequired()])
    recurring = BooleanField('Recurring')
    repeat_dom = IntegerField('Repeat DOM')
    end_month = DateField('End Month', validators=[Optional()])
    type = SelectField('Type', choices=[(1, 'Regular'), (2, 'Irregular')])
    period = FloatField('Period', validators=[Optional()])
    month = DateField('Payment Month', validators=[Optional()])
    submit = SubmitField('Submit')