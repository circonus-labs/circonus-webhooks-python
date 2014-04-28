import requests
import json
import tornado.web
import random

import logging
logger = logging.getLogger('tornado_beacon_data')
logger.setLevel(logging.INFO)
# create a file handler
handler = logging.FileHandler('tornado_beacon_data.log')
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

class BeaconDataLogger():

def logRandomIPData():
	not_valid = [10,127,169,172,192]
	first = random.randrange(1,256)
	while first in not_valid:
		first = random.randrange(1,256)
	ip = ".".join([str(first),str(random.randrange(1,256)),str(random.randrange(1,256)),str(random.randrange(1,256))])
	randomtime = random.randrange(1,100)
	logger.info(",%s,%s", ip, randomtime)

