from DataLogger import *
import time

logManager = LoggingManager("./")
logManager.add_logging_channel("Test")

print(logManager.status)


for i in range(10):

    time.sleep(10)
    logManager.write_entry("Test", "Type", 0.5, 100, False)