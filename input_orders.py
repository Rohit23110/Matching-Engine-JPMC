import csv
from Matching import matching
class order:
    def __init__(self,status,quantity,pending_quantity,stock_code,customer_id,order_id,order_type,flavour):
        self.order_id = order_id
        self.status = status
        self.quantity = quantity
        self.pending_quantity = pending_quantity
        self.stock_code = stock_code
        self.customer_id = customer_id
        self.order_type = order_type
        self.flavour = flavour 

# def inputOrders():
if __name__ == "__main__":
    csv_columns = ['order_id','quantity','pending_quantity','stock_code','customer_id','order_type','flavour','status']
    print("Press 1 to add Order")
    order_id = 0
    a = int(input())
    while(a == 1):
        order_id += 1
        print("Please Enter Customer ID :")
        customer_id = int(input())
        while(customer_id <= 0):
            print("Please Enter Valid Customer ID :")
            customer_id = int(input())
        print("Please Enter Trade Type (Buy or Sell):")
        trade_type = str(input()).lower()
        while(not (trade_type == 'buy' or trade_type == 'sell')):
            print("Please Enter Valid Trade Type (Buy or Sell):")
            trade_type = str(input()).lower()
        print("Please Enter Order Type (Market):")
        order_type = str(input()).lower()
        while(not order_type == 'market'):
            print("Please Enter Valid Order Type (Market):")
            order_type = str(input()).lower()
        flavour = 'NaN'
        print("Please Enter Quantity :")
        quantity = int(input())
        pending_quantity = quantity
        while(quantity <= 0):
            print("Please Enter Valid Quantity :")
            quantity = int(input())  
            pending_quantity = quantity
        print("Please Enter Stock Code :")
        stock_code = str(input())
        print("Press 1 to add Order")
        a = int(input())
        new_order = order('pending',quantity,pending_quantity,stock_code,customer_id,order_id,order_type,flavour)
        if trade_type == 'buy':
            with open('Buyorders.csv', 'a') as f:
                writer = csv.DictWriter(f,fieldnames=csv_columns)
                writer.writerow(new_order.__dict__)
        elif trade_type == 'sell':
            with open('Sellorders.csv', 'a') as f:
                writer = csv.DictWriter(f,fieldnames=csv_columns)
                writer.writerow(new_order.__dict__)
        matching()
    print("Thanks for orders")
