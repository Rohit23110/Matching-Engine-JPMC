from wtforms import StringField,IntegerField,ValidationError,SelectField,SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import Length,DataRequired

class inputOrderForm(FlaskForm):
    quantity = IntegerField("Enter the quantity",validators=[DataRequired()])
    stock_code = StringField("Enter the stock code",validators=[Length(min=6)])
    customer_id = IntegerField("Enter the Customer ID",validators=[DataRequired()])
    trade_type = SelectField("Enter the trade type",validators=[DataRequired()],choices=[('buy','Buy'),('sell','Sell')])
    order_type = SelectField("Order type",validators=[DataRequired()],choices=[('market','Market')]) 
    #flavour = SelectField("Flavour type",validators=[DataRequired()],choices=[('all/none','All/None')])
    submit = SubmitField("Submit")




