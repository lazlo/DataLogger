#!/usr/bin/python

import BaseHTTPServer
import SocketServer

class DebugHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_POST(self):
		print(self.headers)
		print(self.path)
		self.send_response(200)


def main():
	handler = DebugHTTPRequestHandler
	httpd = SocketServer.TCPServer(("", 3000), handler)
	httpd.serve_forever()

if __name__ == "__main__":
	main()
