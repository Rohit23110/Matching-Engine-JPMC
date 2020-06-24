import pandas as pd
import schedule
import time

def remove():
    sellOrders = pd.read_csv("Sellorders.csv")
    buyOrders = pd.read_csv("Buyorders.csv")
    newSellOrders = sellOrders[sellOrders.status=="Completed"]
    newSellOrders = newSellOrders.reset_index(drop=True)
    newSellOrders.to_csv("Sellorders.csv", sep=",", index=False)
    newBuyOrders = buyOrders[buyOrders.status=="Completed"]
    newBuyOrders = newBuyOrders.reset_index(drop=True)
    newBuyOrders.to_csv("Buyorders.csv", sep=",", index=False)
    print(newBuyOrders)
    
if __name__ == "__main__":
    # remove() uncomment this if using task scheduler
    #  uncomment this if u  are using scheduler and running manually to check output
    print("Done")

schedule.every().day.at("15:30").do(remove) 
while True:
    schedule.run_pending()
    time.sleep(1)


    
    