import pandas as pd
import schedule
import time

def remove():
    sellOrders = pd.read_csv("Sellorders.csv")
    buyOrders = pd.read_csv("Buyorders.csv")
    sellOrders.loc[sellOrders.status == "pending", "status"] = 'cancelled'
    # newSellOrders = newSellOrders.reset_index(drop=True)
    sellOrders.to_csv("Sellorders.csv", sep=",", index=False)
    # newBuyOrders = buyOrders[buyOrders.status == "completed"]
    buyOrders.loc[buyOrders.status == "pending", "status"] = 'cancelled'
    # newBuyOrders = newBuyOrders.reset_index(drop=True)
    buyOrders.to_csv("Buyorders.csv", sep=",", index=False)
    # print(newBuyOrders)
    
# if __name__ == "__main__":
#     # remove() uncomment this if using task scheduler
#     #  uncomment this if u  are using scheduler and running manually to check output
#     print("Done")

# schedule.every().day.at("3:30").do(remove) 
# while True:
#     schedule.run_pending()
#     time.sleep(1)


    
    