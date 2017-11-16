import unittest

import data_server

class DataServerTestCase(unittest.TestCase):

	def setUp(self):
		self.srv = data_server.DataServer()

	def testFoo(self):
		self.assertEqual(True, True)
