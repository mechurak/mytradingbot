import logging
import os
from datetime import date
from slack import run


logger = logging.getLogger('MyLogger')
logger.setLevel(logging.DEBUG)
logger.propagate = 0
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
if not os.path.exists("logs"):
    os.makedirs("logs")
today = date.today()
filename = "logs/" + today.strftime("%Y%m%d") + ".log"
fileHandler = logging.FileHandler(filename, "a", "utf-8")
streamHandler = logging.StreamHandler()
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)


# start slack_bot
run.main()



