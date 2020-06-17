import csv
from Matching import matching
class order:
    def __init__(self,status,quantity,stock_code,customer_id,order_id,order_type,flavour):
        self.order_id = order_id
        self.status = status
        self.quantity = quantity
        self.stock_code = stock_code
        self.customer_id = customer_id
        self.order_type = order_type
        self.flavour = flavour 

# def inputOrders():
if __name__ == "__main__":
    csv_columns = ['order_id','quantity','stock_code','customer_id','order_type','flavour','status']
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
        print("Please Enter Quantity :")
        quantity = int(input())
        while(quantity <= 0):
            print("Please Enter Valid Quantity :")
            quantity = int(input())  
        print("Please Enter Stock Code :")
        stock_code = str(input())
        print("Please Enter Order Type :")
        order_type = str(input())
        while(not (order_type.lower() == 'buy' or order_type.lower() == 'sell')):
            print("Please Enter Valid Order Type :")
            order_type = str(input())
        print("Partial or All/None :")
        flavour = str(input())
        while(not (flavour.lower() == 'partial' or flavour.lower() == 'all/none')):
            print("Please Enter Valid Flavour :")
            flavour = str(input())
        print("Press 1 to add Order")
        a = int(input())
        new_order = order('pending',quantity,stock_code,customer_id,order_id,order_type,flavour)
        if order_type == 'buy':
            with open('Buyorders.csv', 'a') as f:
                writer = csv.DictWriter(f,fieldnames=csv_columns)
                writer.writerow(new_order.__dict__)
        elif order_type == 'sell':
            with open('Sellorders.csv', 'a') as f:
                writer = csv.DictWriter(f,fieldnames=csv_columns)
                writer.writerow(new_order.__dict__)
        matching()
    print("Thanks for orders")
