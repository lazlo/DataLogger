import unittest

import position
import data_input
import gps

class PositionTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedName = "Location"
		self.pos = position.Position(self.expectedName)

	def testIsSubclassOfDataInput(self):
		self.assertEqual(True, issubclass(position.Position, data_input.DataInput))

	def testInit_gpsFieldIsOfTypeGPS(self):
		self.assertEqual(True, isinstance(self.pos._gps, gps.gps))

	def testGetData_returnsDictWithKeyLat(self):
		self.assertEqual(True, "lat" in self.pos.get_data().keys())

	def testGetData_returnsDictWithKeyLon(self):
		self.assertEqual(True, "lon" in self.pos.get_data().keys())
