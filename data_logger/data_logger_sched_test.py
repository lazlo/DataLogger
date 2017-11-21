import unittest

import data_logger_sched

class DataLoggerSchedTestCase(unittest.TestCase):

	def setUp(self):
		self.sch = data_logger_sched.DataLoggerScheduler()

	def testFoo(self):
		self.assertEqual(True, True)
