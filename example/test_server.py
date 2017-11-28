#!/usr/bin/python

import BaseHTTPServer
import SocketServer
import json

class DebugHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_POST(self):
		#print(self.headers)
		#print(self.path)
		req_body = self.rfile.read(int(self.headers["Content-Length"]))
		try:
			parsed = json.loads(req_body)
			print(json.dumps(parsed, indent=4))
		except Exception as ex:
			print("Error: JSON decode failed with \"%s\" for:\n%s" % (ex.message, req_body))
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
