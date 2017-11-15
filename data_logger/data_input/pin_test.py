import unittest

import pin
import data_input

class PinTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedName = "Ignition"
		self.p = pin.Pin(self.expectedName)

	def testIsSubclassOfDataInput(self):
		self.assertEqual(True, issubclass(pin.Pin, data_input.DataInput))

if __name__ == "__main__":
	unittest.main()
