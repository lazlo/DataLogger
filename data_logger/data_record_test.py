import unittest

import data_record

class DataRecordTestCase(unittest.TestCase):

	def setUp(self):
		self.dr = data_record.DataRecord()

	def testFoo(self):
		self.assertEqual(True, True)
