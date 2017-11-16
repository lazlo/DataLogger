import unittest

import position
import data_input
from gps3 import gps3

class PositionTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedName = "Location"
		self.pos = position.Position(self.expectedName)

	def testIsSubclassOfDataInput(self):
		self.assertEqual(True, issubclass(position.Position, data_input.DataInput))

	def testInit_gpsSockFieldIsOfTypeGPSDSocket(self):
		self.assertEqual(True, isinstance(self.pos._gpsd_sock, gps3.GPSDSocket))

	def testInit_gpsStreamFieldIsOfTypeDataStream(self):
		self.assertEqual(True, isinstance(self.pos._gps_stream, gps3.DataStream))

	def testGetData_returnsDictWithKeyLat(self):
		self.assertEqual(True, "lat" in self.pos.get_data().keys())

	def testGetData_returnsDictWithKeyLon(self):
		self.assertEqual(True, "lon" in self.pos.get_data().keys())
