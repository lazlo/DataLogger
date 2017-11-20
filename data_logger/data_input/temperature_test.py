import unittest

import temperature

class TemperatureTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedName = "Room 42"
		self.t = temperature.Temperature(self.expectedName)

	def testFoo(self):
		self.assertEqual(True, True)
