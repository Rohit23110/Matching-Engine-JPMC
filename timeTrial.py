import datetime
currentTime = datetime.datetime.now()
startTime = datetime.time(9, 0, 0)
endTime = datetime.time(15, 0, 0)

if (currentTime.time() < endTime) and (currentTime.time() > startTime):
    print("Hello")