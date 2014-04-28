import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado_hipchat_plugin import HipChatHandler
from tornado_json_check_plugin import JsonCheckHandler
from tornado_beacon_data_plugin import BeaconDataLogger

tornado.options.define("port", default=8080, help="Port to run the Tornado server on", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		project_dir = os.getcwd()
		#Define the paths that are available for Circonus to POST to
		handlers = [
			(r"/hipchat/", HipChatHandler),
			(r"/json_check/", JsonCheckHandler),
		]
		settings = dict()
		tornado.web.Application.__init__(self, handlers, **settings)

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(tornado.options.options.port)
	#tornado.ioloop.IOLoop.instance().start()
	interval_ms = 15
	main_loop = tornado.ioloop.IOLoop.instance()
	logdata = tornado.ioloop.PeriodicCallback(BeaconDataLogger.logRandomIPData(),interval_ms, io_loop = main_loop)
	logdata.start()
	main_loop.start()

if __name__ == "__main__":
	main()

