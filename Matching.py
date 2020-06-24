import pandas as pd
from Output import *
from fetchPrices import getCurrentPrice
if __name__ == "__main__":
# def matching():
    sellorders = pd.read_csv("Sellorders.csv")
    buyorders = pd.read_csv("Buyorders.csv")
    transactions = pd.DataFrame(columns = ['buy_customer_id', 'sell_customer_id', 'quantity', 'stock_code', 'price', 'buy_order_id', 'sell_order_id'])

    for i in range(buyorders.shape[0]):
        if buyorders.iloc[i].status == "pending":
            sellorder_list = sellorders[(sellorders.status == "pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code)]
            # print(sellorder_list)
            for j in range(sellorder_list.shape[0]): # Iterate over market sell orders until the buy order is completely satisfied
                # print("Market buy order with market sell order")
                transaction_quantity = min(buyorders.iloc[i].pending_quantity, sellorder_list.iloc[j].pending_quantity)
                pending_quantity = sellorder_list.iloc[j].pending_quantity - buyorders.iloc[i].pending_quantity
                buyorders.loc[i, 'pending_quantity'] = max(0, -(pending_quantity))
                sellorders.loc[(sellorder_list.iloc[j].order_id == sellorders.order_id), 'pending_quantity'] = max(0, pending_quantity)                
                
                transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': sellorder_list.iloc[j].customer_id, 'quantity': transaction_quantity, 'stock_code' : sellorder_list.iloc[j].stock_code, 'price': getCurrentPrice(str(sellorder_list.iloc[j].stock_code)), 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': sellorder_list.iloc[j].order_id}
                transactions = transactions.append(transaction, ignore_index=True)
                # print(sellorders.loc[(sellorder_list.iloc[j].order_id == sellorders.order_id), 'pending_quantity'])
                if sellorders.loc[(sellorder_list.iloc[j].order_id == sellorders.order_id), 'pending_quantity'].iloc[0] == 0:
                    sellorders.loc[sellorder_list.iloc[j].order_id == sellorders.order_id, 'status'] = 'completed'
                if buyorders.loc[i, 'pending_quantity'] == 0:
                    buyorders.loc[i, 'status'] = 'completed'
                    break
            # print(buyorders)
            # print(sellorders)

    convert_dict = { # Had to add this to prevent the columns from converting to float
        "buy_customer_id": "int64",
        "sell_customer_id": "int64",
        "quantity": "int64",
        "stock_code": "int64",
        "price": "float64",
        "buy_order_id": "int64",
        "sell_order_id": "int64"
    }
    transactions = transactions.astype(convert_dict)
    printOutput(sellorders,buyorders,transactions)
    buyorders.to_csv("Buyorders.csv", sep=",", na_rep="NaN", index=False)
    sellorders.to_csv("Sellorders.csv", sep=",", na_rep="NaN", index=False)
