import pandas as pd
from Output import *
from fetchPrices import getCurrentPrice
# if __name__ == "__main__":
def matching():
    sellorders = pd.read_csv("Sellorders.csv")
    buyorders = pd.read_csv("Buyorders.csv")
    transactions = pd.DataFrame(columns = ['buy_customer_id', 'sell_customer_id', 'quantity', 'stock_code', 'price', 'buy_order_id', 'sell_order_id'])

    for i in range(buyorders.shape[0]):
        if(buyorders.iloc[i].flavor=='all/none'): # if buyer wants all/none flavors irrespective of seller is partial or all/none
            sellorder = sellorders[(sellorders.status == "pending") & (buyorders.iloc[i].status == "pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code) & (sellorders.quantity == buyorders.iloc[i].quantity)]
            if len(sellorder) != 0:
                sellorder = sellorder.iloc[0]
                # print(sellorder, "\n")
                # print(sellorder.order_id, "\n")
                transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': sellorder.customer_id, 'quantity': sellorder.quantity, 'stock_code' : sellorder.stock_code, 'price': getCurrentPrice(str(sellorder.stock_code)), 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': sellorder.order_id}
                transactions = transactions.append(transaction, ignore_index=True)
                sellorders.loc[sellorders.order_id == sellorder.order_id, 'status'] = "completed"
                buyorders.at[i, 'status'] = "completed"
            else:
                sellorder = sellorders[(sellorders.status == "pending") & (buyorders.iloc[i].status == "pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code) & (sellorders.quantity > buyorders.iloc[i].quantity) & (sellorders.flavor=="partial")]
                if len(sellorder) != 0:# if yes then seller status pending and quantity debit by buyer's quantity and buyer status completed
                    sellorder = sellorder.iloc[0]
                    # print(sellorder, "\n")
                    # print(sellorder.order_id, "\n")
                    transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': sellorder.customer_id, 'quantity': buyorders.iloc[i].quantity, 'stock_code' : sellorder.stock_code, 'price': getCurrentPrice(str(sellorder.stock_code)), 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': sellorder.order_id}
                    transactions = transactions.append(transaction, ignore_index=True)
                    sellorders.loc[sellorders.order_id == sellorder.order_id, 'status'] = "pending"
                    buyorders.at[i, 'status'] = "completed"
                    sellorders.loc[sellorders.order_id == sellorder.order_id, 'quantity'] = sellorder.quantity-buyorders.iloc[i].quantity
        else: # now if buyer want partial fill then check first if all/none fill is possible
            sellorder = sellorders[(sellorders.status == "pending") & (buyorders.iloc[i].status == "pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code) & (sellorders.quantity == buyorders.iloc[i].quantity)]
            if len(sellorder) != 0: #if yes then its great both buyer and seller got connected exactly
                sellorder = sellorder.iloc[0]
                # print(sellorder, "\n")
                # print(sellorder.order_id, "\n")
                transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': sellorder.customer_id, 'quantity': sellorder.quantity, 'stock_code' : sellorder.stock_code, 'price': getCurrentPrice(str(sellorder.stock_code)), 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': sellorder.order_id}
                transactions = transactions.append(transaction, ignore_index=True)
                sellorders.loc[sellorders.order_id == sellorder.order_id, 'status'] = "completed"
                buyorders.at[i, 'status'] = "completed"
            else: # else now check for partial fill i.e. if any seller can completely satisfy buyer's request and seller is allowing partial sell
                sellorder = sellorders[(sellorders.status == "pending") & (buyorders.iloc[i].status == "pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code) & (sellorders.quantity > buyorders.iloc[i].quantity) & (sellorders.flavor=="partial")]
                if len(sellorder) != 0:# if yes then seller status pending and quantity debit by buyer's quantity and buyer status completed
                    sellorder = sellorder.iloc[0]
                    # print(sellorder, "\n")
                    # print(sellorder.order_id, "\n")
                    transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': sellorder.customer_id, 'quantity': buyorders.iloc[i].quantity, 'stock_code' : sellorder.stock_code, 'price': getCurrentPrice(str(sellorder.stock_code)), 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': sellorder.order_id}
                    transactions = transactions.append(transaction, ignore_index=True)
                    sellorders.loc[sellorders.order_id == sellorder.order_id, 'status'] = "pending"
                    buyorders.at[i, 'status'] = "completed"
                    sellorders.loc[sellorders.order_id == sellorder.order_id, 'quantity'] = sellorder.quantity-buyorders.iloc[i].quantity
                else: # now we have not got any seller who can satisfy buyer's needs completely then buyer has to buy in partial manner
                    sellorder = sellorders[(sellorders.status == "pending") & (buyorders.iloc[i].status == "pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code) & (sellorders.quantity < buyorders.iloc[i].quantity)]
                    if len(sellorder) != 0: #so seller status will get completed and buyer status is pending and quantity will be debited by sellorder ka quantity.
                        sellorder = sellorder.iloc[0]
                        # print(sellorder, "\n")
                        # print(sellorder.order_id, "\n")
                        transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': sellorder.customer_id, 'quantity': sellorder.quantity, 'stock_code' : sellorder.stock_code, 'price': getCurrentPrice(str(sellorder.stock_code)), 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': sellorder.order_id}
                        transactions = transactions.append(transaction, ignore_index=True)
                        sellorders.loc[sellorders.order_id == sellorder.order_id, 'status'] = "completed"
                        buyorders.at[i, 'status'] = "pending"
                        buyorders.at[i,'quantity']= - sellorder.quantity + buyorders.iloc[i].quantity
            #abhi tak kuch nahi mila toh sorry buyer.

    # print(buyorders)
    # print(sellorders)
    # print(transactions)
    printOutput(sellorders,buyorders,transactions)
    buyorders.to_csv("Buyorders.csv", sep=",", index=False)
    sellorders.to_csv("Sellorders.csv", sep=",", index=False)
matching()
