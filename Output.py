import pandas as pd
def printOutput(sellOrder,buyOrder,trans):
    if(sellOrder.empty==False):
        print("_______________________Status Of All SellOrders_____________________________")
        print(sellOrder)
    else:
        print("There are no new SellOrders!")
    if(buyOrder.empty==False):
        print("_______________________Status Of All BuyOrders_______________________________")
        print(buyOrder)
    else:
        print("There are no new BuyOrders!")

    
    if(trans.empty==True):
        print("______________________________No Transaction Occured!____________________________")
        transaction = pd.read_csv("Transaction.csv")
        if(transaction.empty==False):
            print(transaction)
    else:
        print("______________________________Transaction Occured!____________________________")
        trans.to_csv("Transaction.csv",mode='a', sep=",", index=False,header=None)
        transaction = pd.read_csv("Transaction.csv")
        print(transaction)
    