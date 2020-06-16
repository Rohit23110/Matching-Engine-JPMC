import pandas as pd
from Output import *
if __name__ == "__main__":
    sellorders = pd.read_csv("Sellorders.csv")
    buyorders = pd.read_csv("Buyorders.csv")
    transactions = pd.DataFrame(columns = ['buy_customer_id', 'sell_customer_id', 'quantity', 'stock_code', 'price', 'buy_order_id', 'sell_order_id'])

    for i in range(buyorders.shape[0]):
        sellorder = sellorders[(sellorders.status == "Pending") & (buyorders.iloc[i].status == "Pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code) & (sellorders.quantity == buyorders.iloc[i].quantity)]
        if len(sellorder) != 0:
            sellorder = sellorder.iloc[0]
            print(sellorder, "\n")
            transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': sellorder.customer_id, 'quantity': sellorder.quantity, 'stock_code' : sellorder.stock_code, 'price': 1, 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': sellorder.order_id}
            transactions = transactions.append(transaction, ignore_index=True)
            sellorders.loc[sellorders.order_id == sellorder.order_id, 'status'] = "Completed"
            buyorders.at[i, 'status'] = "Completed"
    printOutput(sellorders,buyorders,transactions)
    buyorders.to_csv("Buyorders.csv", sep=",", index=False)
    sellorders.to_csv("Sellorders.csv", sep=",", index=False)
