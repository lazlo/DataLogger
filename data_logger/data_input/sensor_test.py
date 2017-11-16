import unittest

import sensor
import data_input

class SensorTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedName = "Temperature"
		self.sen = sensor.Sensor(self.expectedName)

	def testIsSubclassOfDataInput(self):
		self.assertEqual(True, issubclass(sensor.Sensor, data_input.DataInput))

	def testGetData_returnsDict(self):
		self.assertEqual(True, isinstance(self.sen.get_data(), dict))

if __name__ == "__main__":
	unittest.main()
