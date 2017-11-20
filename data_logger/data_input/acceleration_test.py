import unittest

import acceleration

class AccelerationUnitTest(unittest.TestCase):

	def setUp(self):
		self.expectedName = "Acceleration"
		self.acc = acceleration.Acceleration(self.expectedName)

	def testFoo(self):
		self.assertEqual(True, True)
