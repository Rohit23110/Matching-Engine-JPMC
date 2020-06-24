from wtforms import StringField,IntegerField,ValidationError,SelectField,SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import Length,DataRequired

class inputOrderForm(FlaskForm):
    quantity = IntegerField("Enter the quantity",validators=[DataRequired()])
    stock_code = StringField("Enter the stock code",validators=[Length(min=6)])
    customer_id = IntegerField("Enter the Customer ID",validators=[DataRequired()])
    order_type = SelectField("Enter the order type",validators=[DataRequired()],choices=[('buy','BUY'),('sell','SELL')])
    flavour = SelectField("Enter the flavour type",validators=[DataRequired()],choices=[('all/none','All/None'),('partial','Partial')])
    submit = SubmitField("Submit")




