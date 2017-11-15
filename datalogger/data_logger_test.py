import unittest

import data_logger

class DataLoggerTestCase(unittest.TestCase):

	def setUp(self):
		self.dl = data_logger.DataLogger()

	def testFoo(self):
		self.assertEqual(True, True)

if __name__ == "__main__":
	unittest.main()
