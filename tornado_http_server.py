import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado_hipchat_plugin import HipChatHandler

tornado.options.define("port", default=8080, help="Port to run the Tornado server on", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		project_dir = os.getcwd()
		#Define the paths that are available for Circonus to POST to
		handlers = [
			(r"/hipchat/", HipChatHandler),
		]
		settings = dict()
		tornado.web.Application.__init__(self, handlers, **settings)

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(tornado.options.options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
