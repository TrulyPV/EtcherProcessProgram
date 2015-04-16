#!/usr/bin/env python
#-*- coding:utf-8 -*-

from EtcherIO import *
import time
## logging parameters
import logging
from logging.handlers import RotatingFileHandler
LOGFILE = "motor.log"
MAXLOGSIZE = 2*1024*1024    #Bytes
BACKUPCOUNT = 2
FORMAT = \
"%(asctime)s %(levelname)-8s[%(filename)s:%(lineno)d(%(funcName)s)] %(message)s"
LOGLVL = logging.DEBUG
# create file handler which logs even debug messages  
fh = RotatingFileHandler(LOGFILE,
                         mode='w',
                         maxBytes=MAXLOGSIZE,
                         backupCount=BACKUPCOUNT)
formatter = logging.Formatter(FORMAT)
# create console handler with a higher log level  
ch = logging.StreamHandler()  
ch.setLevel(logging.DEBUG)  
# create formatter and add it to the handlers  
ch.setFormatter(formatter)  
fh.setFormatter(formatter)

LOG = logging.getLogger()
# add the handlers to logger  
LOG.addHandler(ch)
LOG.addHandler(fh)    
LOG.setLevel(LOGLVL)
LOG.debug("logging init")

port = COMOperator(LOG)

throttle = Motor("Throttle",port)

while True:
	key = raw_input("Your command ->")

	if key == 'q':
		break
	elif key == 'f':
		throttle.move(5)
	elif key == 'b':
		throttle.move(-20)
	elif key == 'z':
		throttle.gotoZero()
	elif key == 'o':
		throttle.gotoLimit()
	elif key == 'd':
		throttle.findLimit()
	else:
		throttle.stop()
	time.sleep(0.1)
	ret,data = throttle.readStatus()
	LOG.info(" Opened,Closed,Origin:%s, location:%s, \n %s"%((throttle.LL,throttle.RL,throttle.zero),throttle.location,(ret,data)))
LOG.info("Exiting ... ")


