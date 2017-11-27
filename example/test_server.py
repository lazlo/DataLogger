#!/usr/bin/python

import BaseHTTPServer
import SocketServer

class DebugHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_POST(self):
		#print(self.headers)
		#print(self.path)
		print(self.rfile.read(int(self.headers["Content-Length"])))
		self.send_response(200)
		self.send_header("Content-type", "application/json")
		self.end_headers()
		self.wfile.write("{\"Message\":null, \"IsError\":false}")


def main():
	handler = DebugHTTPRequestHandler
	httpd = SocketServer.TCPServer(("", 3000), handler)
	httpd.serve_forever()

if __name__ == "__main__":
	main()
