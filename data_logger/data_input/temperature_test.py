import unittest

import temperature

class TemperatureTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedName = "Room 42"
		self.t = temperature.Temperature(self.expectedName)

	def testGetData_returnsFloat(self):
		self.assertEqual(True, type(self.t.get_data()) is float)
