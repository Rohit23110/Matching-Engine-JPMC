import pandas as pd
from Output import *
from fetchPrices import getCurrentPrice
if __name__ == "__main__":
# def matching():
    sellorders = pd.read_csv("Sellorders.csv")
    # print(sellorders.dtypes)
    # sellorders.limit_price = sellorders.limit_price.fillna(value="")
    # print(sellorders.dtypes)
    buyorders = pd.read_csv("Buyorders.csv")
    # print(buyorders.dtypes)
    # buyorders.limit_price = buyorders.limit_price.fillna(value="")
    # print(buyorders.dtypes)
    transactions = pd.DataFrame(columns = ['buy_customer_id', 'sell_customer_id', 'quantity', 'stock_code', 'price', 'buy_order_id', 'sell_order_id'])
    # transactions.price = transactions.price.astype("float")
    # print(transactions.dtypes)

    for i in range(buyorders.shape[0]):
        if buyorders.iloc[i].order_type == 'market':
            sellorder = sellorders[(sellorders.order_type == "market") & (sellorders.status == "pending") & (buyorders.iloc[i].status == "pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code) & (sellorders.quantity == buyorders.iloc[i].quantity)]
            if len(sellorder) != 0:
                sellorder = sellorder.iloc[0]
                # print(sellorder, "\n")
                # print(sellorder.order_id, "\n")
                transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': sellorder.customer_id, 'quantity': sellorder.quantity, 'stock_code' : sellorder.stock_code, 'price': getCurrentPrice(str(sellorder.stock_code)), 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': sellorder.order_id}
                transactions = transactions.append(transaction, ignore_index=True)
                sellorders.loc[sellorders.order_id == sellorder.order_id, 'status'] = "completed"
                buyorders.at[i, 'status'] = "completed"
        else:
            sellorder = sellorders[(sellorders.order_type == "limit") & (sellorders.status == "pending") & (buyorders.iloc[i].status == "pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code) & (sellorders.quantity == buyorders.iloc[i].quantity) & (sellorders.limit_price <= buyorders.iloc[i].limit_price)]
            if len(sellorder) != 0:
                sellorder = sellorder.iloc[0]
                # print(sellorder, "\n")
                # print(sellorder.order_id, "\n")
                transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': sellorder.customer_id, 'quantity': sellorder.quantity, 'stock_code' : sellorder.stock_code, 'price': sellorder.limit_price, 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': sellorder.order_id}
                transactions = transactions.append(transaction, ignore_index=True)
                sellorders.loc[sellorders.order_id == sellorder.order_id, 'status'] = "completed"
                buyorders.at[i, 'status'] = "completed"

    # print(buyorders)
    # print(buyorders.dtypes)
    # print(sellorders)
    # print(sellorders.dtypes)
    # print(transactions)
    # print(transactions.dtypes)
    convert_dict = { # Had to add this to prevent the colums from converting to float
        "buy_customer_id": "int64",
        "sell_customer_id": "int64",
        "quantity": "int64",
        "stock_code": "int64",
        "price": "float64",
        "buy_order_id": "int64",
        "sell_order_id": "int64"
    }
    transactions = transactions.astype(convert_dict)
    # print(transactions)
    # print(transactions.dtypes)
    printOutput(sellorders,buyorders,transactions)
    buyorders.to_csv("Buyorders.csv", sep=",", na_rep="NaN", index=False)
    sellorders.to_csv("Sellorders.csv", sep=",", na_rep="NaN", index=False)
