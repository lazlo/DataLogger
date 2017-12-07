import unittest

import pin
import data_input

class PinTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedName = "Ignition"
		self.p = pin.Pin(self.expectedName)

	def testIsSubclassOfDataInput(self):
		self.assertEqual(True, issubclass(pin.Pin, data_input.DataInput))

	def testGetData_returnsFloat(self):
		self.assertEqual(True, isinstance(self.p.get_data(), float))

if __name__ == "__main__":
	unittest.main()
