import datetime

from globals import *

def logMessage(messageName, isoFilename, isoName):
    timeNow = datetime.datetime.now()
    timeNow = str(timeNow.year) + '/' + str(timeNow.month) + '/' + str(timeNow.day) + '/' +\
              str(timeNow.hour) + '/' + str(timeNow.minute) + '/' + str(timeNow.second)
    
    logFile = open(LOGFILE, "a")
    logFile.write(timeNow + '\t' + messageName + '\t' + isoFilename + '\t' + isoName + '\n');
    

def logWodim(message):
    timeNow = datetime.datetime.now()
    timeNow = str(timeNow.year) + '/' + str(timeNow.month) + '/' + str(timeNow.day) + '/' +\
              str(timeNow.hour) + '/' + str(timeNow.minute) + '/' + str(timeNow.second)
    
    logFile = open(LOGFILE, "a")
    logFile.write(timeNow + '\t' + MWODIM + message)
    
