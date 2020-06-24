from flask import Flask,request,jsonify,url_for,render_template,redirect,logging
import json
import pandas as pd
import csv
from csv import DictWriter
from forms import inputOrderForm
from fetch_prices import getCurrentPrice

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


def append_dict_as_row(file_name, dict_of_elem, field_names):
    with open(file_name, 'a+', newline='') as write_obj:
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        dict_writer.writerow(dict_of_elem)

@app.route('/transactions')
def show_transaction():
    transaction_data = []
    input_file = csv.DictReader(open("transaction.csv"))
    for row in input_file:
        transaction_data.append(row)
        print(type(row['price']))
        print(row)
    return render_template('transaction.html',transaction_data = transaction_data)

@app.route('/',methods=['GET','POST'])
def get_orders():
    form = inputOrderForm()
    buy_data = []
    sell_data = []
    max_order_id = 0
    input_file = csv.DictReader(open("buy_orders.csv"))
    for row in input_file:
        if(max_order_id < int(row['order_id'])):
            max_order_id = int(row['order_id'])
        # row['price'] = getCurrentPrice(row['stock_code'])
        # print(row)
        buy_data.append(row)
    input_file = csv.DictReader(open("sell_orders.csv"))
    for row in input_file:
        if(max_order_id < int(row['order_id'])):
            max_order_id = int(row['order_id'])
        # row['price'] = getCurrentPrice(row['stock_code'])
        # print(row)
        sell_data.append(row)
    # print(type(buy_data[0]))
    # buy_data = sorted(buy_data,key= lambda x : x['price'] )
    # sell_data = sorted(sell_data,key= lambda x : x['price'], reverse = True)
    # print(buy_data)
    # print(sell_data)
    if(max_order_id == 0):
        max_order_id += 1
    if form.validate_on_submit():
        order_dict = form.data
        print(order_dict["order_type"])
        del order_dict['csrf_token']
        del order_dict['submit']
        order_dict['status'] = 'pending'
        order_dict['order_id'] = max_order_id+1
        #order_dict['order_id'] = current_order
        append_dict_as_row(order_dict["order_type"]+'_orders.csv',order_dict,['quantity','stock_code','customer_id','order_id','order_type','flavour','status'])
        return redirect(url_for('get_orders'))
    return render_template("orders.html", buy_data = buy_data , sell_data = sell_data , form = form)

if __name__ == '__main__':
    app.run(debug = True)