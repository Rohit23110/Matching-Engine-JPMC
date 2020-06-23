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
    transactions = pd.DataFrame(columns = ['buy_customer_id', 'sell_customer_id', 'quantity', 'pending_quantity', 'stock_code', 'price', 'buy_order_id', 'sell_order_id'])
    # transactions.price = transactions.price.astype("float")
    # print(transactions.dtypes)

    for i in range(buyorders.shape[0]):
        if buyorders.iloc[i].order_type == "market": # Market order code
            market_price = getCurrentPrice(buyorders.iloc[i].stock_code)
            sellorder_list = sellorders[(sellorders.status == "pending") & (buyorders.iloc[i].status == "pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code)]
            market_sellorder_list = sellorder_list[(sellorder_list.order_type == "market")]
            limit_sellorder_list = sellorder_list[(sellorder_list.order_type == "limit")]
            
            for j in range(market_sellorder_list.shape[0]): # Iterate over market sell orders until the buy order is completely satisfied
                print("Market buy order with market sell order")
                transaction_quantity = min(buyorders.iloc[i].pending_quantity, market_sellorder_list.iloc[j].pending_quantity)
                pending_quantity = market_sellorder_list.iloc[j].pending_quantity - buyorders.iloc[i].pending_quantity
                buyorders.iloc[i].pending_quantity = max(0, -(pending_quantity))
                sellorders.loc[market_sellorder_list.iloc[j].order_id == sellorders.order_id, 'pending_quantity'] = max(0, pending_quantity)                
                
                transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': market_sellorder_list.iloc[j].customer_id, 'quantity': transaction_quantity, 'stock_code' : market_sellorder_list.iloc[j].stock_code, 'price': market_price, 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': market_sellorder_list.iloc[j].order_id}
                transactions = transactions.append(transaction, ignore_index=True)
                if market_sellorder_list.iloc[i].pending_quantity == 0:
                    sellorders.loc[market_sellorder_list.iloc[j].order_id == sellorders.order_id, 'status'] = 'completed'
                if buyorders.iloc[i].pending_quantity == 0:
                    buyorders.iloc[i].status = 'completed'
                    break

            else: # No market sell order satisfied complete requirement
                if buyorders.iloc[i].pending_quantity != 0:
                    for j in range(limit_sellorder_list.shape[0]):# Iterate over limit sell orders until the buy order is completely satisfied
                        if limit_sellorder_list.iloc[j].limit_price <= market_price:
                            if limit_sellorder_list.iloc[j].flavour == "all/none":
                                if buyorders.iloc[i].pending_quantity == limit_sellorder_list.iloc[j].pending_quantity:
                                    transaction_quantity = buyorders.iloc[i].pending_quantity
                                    buyorders.iloc[i].pending_quantity = 0
                                    sellorders.loc[limit_sellorder_list.iloc[j].order_id == sellorders.order_id, 'pending_quantity'] = 0
                                    buyorders.iloc[i].status = 'completed'
                                    sellorders.loc[limit_sellorder_list.iloc[j].order_id == sellorders.order_id, 'status'] = 'completed'
                                    transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': limit_sellorder_list.iloc[j].customer_id, 'quantity': transaction_quantity, 'stock_code' : limit_sellorder_list.iloc[j].stock_code, 'price': market_price, 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': limit_sellorder_list.iloc[j].order_id}
                                    transactions = transactions.append(transaction, ignore_index=True)
                                    break
                            else:
                                transaction_quantity = min(buyorders.iloc[i].pending_quantity, limit_sellorder_list.iloc[j].pending_quantity)
                                pending_quantity = limit_sellorder_list.iloc[j].pending_quantity - buyorders.iloc[i].pending_quantity
                                buyorders.iloc[i].pending_quantity = max(0, -(pending_quantity))
                                sellorders.loc[limit_sellorder_list.iloc[j].order_id == sellorders.order_id, 'pending_quantity'] = max(0, pending_quantity)                
                                
                                transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': limit_sellorder_list.iloc[j].customer_id, 'quantity': transaction_quantity, 'stock_code' : limit_sellorder_list.iloc[j].stock_code, 'price': market_price, 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': limit_sellorder_list.iloc[j].order_id}
                                transactions = transactions.append(transaction, ignore_index=True)
                                if limit_sellorder_list.iloc[i].pending_quantity == 0:
                                    sellorders.loc[market_sellorder_list.iloc[j].order_id == sellorders.order_id, 'status'] = 'completed'
                                if buyorders.iloc[i].pending_quantity == 0:
                                    buyorders.iloc[i].status = 'completed'
                                    break
        elif buyorders.iloc[i].order_type == "limit": # Limit order code
            



                
        # if(buyorders.iloc[i].flavor=='all/none'): # if buyer wants all/none flavors irrespective of seller is partial or all/none
        #     sellorder = sellorders[(sellorders.status == "pending") & (buyorders.iloc[i].status == "pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code) & (sellorders.quantity == buyorders.iloc[i].quantity)]
        #     if len(sellorder) != 0:
        #         sellorder = sellorder.iloc[0]
        #         # print(sellorder, "\n")
        #         # print(sellorder.order_id, "\n")
        #         transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': sellorder.customer_id, 'quantity': sellorder.quantity, 'stock_code' : sellorder.stock_code, 'price': getCurrentPrice(str(sellorder.stock_code)), 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': sellorder.order_id}
        #         transactions = transactions.append(transaction, ignore_index=True)
        #         sellorders.loc[sellorders.order_id == sellorder.order_id, 'status'] = "completed"
        #         buyorders.at[i, 'status'] = "completed"
        #     else:
        #         sellorder = sellorders[(sellorders.status == "pending") & (buyorders.iloc[i].status == "pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code) & (sellorders.quantity > buyorders.iloc[i].quantity) & (sellorders.flavor=="partial")]
        #         if len(sellorder) != 0:# if yes then seller status pending and quantity debit by buyer's quantity and buyer status completed
        #             sellorder = sellorder.iloc[0]
        #             # print(sellorder, "\n")
        #             # print(sellorder.order_id, "\n")
        #             transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': sellorder.customer_id, 'quantity': buyorders.iloc[i].quantity, 'stock_code' : sellorder.stock_code, 'price': getCurrentPrice(str(sellorder.stock_code)), 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': sellorder.order_id}
        #             transactions = transactions.append(transaction, ignore_index=True)
        #             sellorders.loc[sellorders.order_id == sellorder.order_id, 'status'] = "pending"
        #             buyorders.at[i, 'status'] = "completed"
        #             sellorders.loc[sellorders.order_id == sellorder.order_id, 'quantity'] = sellorder.quantity-buyorders.iloc[i].quantity
        # else: # now if buyer want partial fill then check first if all/none fill is possible
        #     sellorder = sellorders[(sellorders.status == "pending") & (buyorders.iloc[i].status == "pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code) & (sellorders.quantity == buyorders.iloc[i].quantity)]
        #     if len(sellorder) != 0: #if yes then its great both buyer and seller got connected exactly
        #         sellorder = sellorder.iloc[0]
        #         # print(sellorder, "\n")
        #         # print(sellorder.order_id, "\n")
        #         transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': sellorder.customer_id, 'quantity': sellorder.quantity, 'stock_code' : sellorder.stock_code, 'price': getCurrentPrice(str(sellorder.stock_code)), 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': sellorder.order_id}
        #         transactions = transactions.append(transaction, ignore_index=True)
        #         sellorders.loc[sellorders.order_id == sellorder.order_id, 'status'] = "completed"
        #         buyorders.at[i, 'status'] = "completed"
        #     else: # else now check for partial fill i.e. if any seller can completely satisfy buyer's request and seller is allowing partial sell
        #         sellorder = sellorders[(sellorders.status == "pending") & (buyorders.iloc[i].status == "pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code) & (sellorders.quantity > buyorders.iloc[i].quantity) & (sellorders.flavor=="partial")]
        #         if len(sellorder) != 0:# if yes then seller status pending and quantity debit by buyer's quantity and buyer status completed
        #             sellorder = sellorder.iloc[0]
        #             # print(sellorder, "\n")
        #             # print(sellorder.order_id, "\n")
        #             transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': sellorder.customer_id, 'quantity': buyorders.iloc[i].quantity, 'stock_code' : sellorder.stock_code, 'price': getCurrentPrice(str(sellorder.stock_code)), 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': sellorder.order_id}
        #             transactions = transactions.append(transaction, ignore_index=True)
        #             sellorders.loc[sellorders.order_id == sellorder.order_id, 'status'] = "pending"
        #             buyorders.at[i, 'status'] = "completed"
        #             sellorders.loc[sellorders.order_id == sellorder.order_id, 'quantity'] = sellorder.quantity-buyorders.iloc[i].quantity
        #         else: # now we have not got any seller who can satisfy buyer's needs completely then buyer has to buy in partial manner
        #             sellorder = sellorders[(sellorders.status == "pending") & (buyorders.iloc[i].status == "pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code) & (sellorders.quantity < buyorders.iloc[i].quantity)]
        #             if len(sellorder) != 0: #so seller status will get completed and buyer status is pending and quantity will be debited by sellorder ka quantity.
        #                 sellorder = sellorder.iloc[0]
        #                 # print(sellorder, "\n")
        #                 # print(sellorder.order_id, "\n")
        #                 transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': sellorder.customer_id, 'quantity': sellorder.quantity, 'stock_code' : sellorder.stock_code, 'price': getCurrentPrice(str(sellorder.stock_code)), 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': sellorder.order_id}
        #                 transactions = transactions.append(transaction, ignore_index=True)
        #                 sellorders.loc[sellorders.order_id == sellorder.order_id, 'status'] = "completed"
        #                 buyorders.at[i, 'status'] = "pending"
        #                 buyorders.at[i,'quantity']= - sellorder.quantity + buyorders.iloc[i].quantity
            #abhi tak kuch nahi mila toh sorry buyer.

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

# if buyorders.iloc[i].order_type == 'market':
#     sellorder = sellorders[(sellorders.order_type == "market") & (sellorders.status == "pending") & (buyorders.iloc[i].status == "pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code) & (sellorders.quantity == buyorders.iloc[i].quantity)]
# else:
#     sellorder = sellorders[(sellorders.order_type == "limit") & (sellorders.status == "pending") & (buyorders.iloc[i].status == "pending") & (sellorders.stock_code == buyorders.iloc[i].stock_code) & (sellorders.quantity == buyorders.iloc[i].quantity) & (sellorders.limit_price <= buyorders.iloc[i].limit_price)]
#     if len(sellorder) != 0:
#         sellorder = sellorder.iloc[0]
#         # print(sellorder, "\n")
#         # print(sellorder.order_id, "\n")
#         transaction = {'buy_customer_id': buyorders.iloc[i].customer_id, 'sell_customer_id': sellorder.customer_id, 'quantity': sellorder.quantity, 'stock_code' : sellorder.stock_code, 'price': sellorder.limit_price, 'buy_order_id': buyorders.iloc[i].order_id, 'sell_order_id': sellorder.order_id}
#         transactions = transactions.append(transaction, ignore_index=True)
#         sellorders.loc[sellorders.order_id == sellorder.order_id, 'status'] = "completed"
#         buyorders.at[i, 'status'] = "completed"