import requests
import json
import tornado.web
import random

class JsonCheckHandler(tornado.web.RequestHandler):
	def get(self):
		data = {
			"number": random.uniform(1.0, 2.0),
			"test": "a text string",
			"bignum_as_string": "281474976710656", 
			"container": { "key1": random.randint(1200, 1300) },
			"array": [
				random.randint(1200, 1300),
				"string",
				{ "crazy": "like a fox" }
			],
			"testingtypedict": { "_type": "L", "_value": "12398234" },
			"histogramdata": { "_type": "n", "_value": [int(1000*random.betavariate(1,3)) for i in xrange(10000)] }
		}
		self.write(json.dumps(data))

