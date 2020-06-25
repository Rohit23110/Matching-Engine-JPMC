from flask import Flask,request,jsonify,url_for,render_template,redirect,logging
import json
import pandas as pd
import csv
import datetime
import subprocess
from csv import DictWriter
from forms import inputOrderForm
from Matching import matching

subprocess.call('python Cancellation.py', creationflags=subprocess.CREATE_NEW_CONSOLE)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

def append_dict_as_row(file_name, dict_of_elem, field_names):
    with open(file_name, 'a+', newline='') as write_obj:
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        dict_writer.writerow(dict_of_elem)

@app.route('/transactions')
def show_transaction():
    transaction_data = []
    input_file = csv.DictReader(open("Transaction.csv"))
    for row in input_file:
        transaction_data.append(row)
    return render_template('transaction.html',transaction_data = transaction_data)

@app.route('/',methods=['GET','POST'])
def get_orders():
    form = inputOrderForm()
    buy_data = []
    sell_data = []
    max_buyorder_id = 0
    max_sellorder_id = 0
    input_file = csv.DictReader(open("Buyorders.csv"))
    for row in input_file:
        if(max_buyorder_id < int(row['order_id'])):
          max_buyorder_id = int(row['order_id'])
        buy_data.append(row)
    input_file = csv.DictReader(open("Sellorders.csv"))
    for row in input_file:
        if(max_sellorder_id < int(row['order_id'])):
          max_sellorder_id = int(row['order_id'])
        sell_data.append(row)
    if form.validate_on_submit():
        order_dict = form.data
        trade_type = order_dict['trade_type']
        del order_dict['csrf_token']
        del order_dict['submit']
        order_dict['status'] = 'pending'
        if order_dict['trade_type']=='buy':
            order_dict['order_id'] = max_buyorder_id+1
        else:
            order_dict['order_id'] = max_sellorder_id+1
        del order_dict['trade_type']
        order_dict['pending_quantity'] = form.quantity.data
        append_dict_as_row(trade_type.title()+'orders.csv',order_dict,['order_id','quantity','pending_quantity','stock_code','customer_id','order_type','flavour','status'])
        currentTime = datetime.datetime.now()
        startTime = datetime.time(9, 15, 0)
        endTime = datetime.time(15, 30, 0)
        print(currentTime)

        if ((currentTime.time() < endTime) and (currentTime.time() > startTime)): #works
            matching()
        
        return redirect(url_for('get_orders'))
    return render_template("orders.html", buy_data = buy_data , sell_data = sell_data , form=form )

if __name__ == '__main__':
    app.run(debug = True)
    
