import unittest

import data_server
import httplib

class DataServerTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedAddr = "http://localhost"
		self.expectedUser = "eris"
		self.expectedPassword = "fnord2342"
		self.srv = data_server.DataServer(self.expectedAddr, self.expectedUser, self.expectedPassword)

	def testInit_addrIsSet(self):
		self.assertEqual(self.expectedAddr, self.srv.addr)

	def testInit_userIsSet(self):
		self.assertEqual(self.expectedUser, self.srv.user)

	def testInit_passwordIsSet(self):
		self.assertEqual(self.expectedPassword, self.srv.password)

	def testInit_httpConnIsInstanceOfHTTPConnection(self):
		self.assertEqual(True, isinstance(self.srv.httpconn, httplib.HTTPConnection))
