import unittest

import position
import data_input
import gps

gps_next_called = False
def fake_gps_next():
	global gps_next_called
	gps_next_called = True

class PositionTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedName = "Location"
		self.pos = position.Position(self.expectedName)

	def testIsSubclassOfDataInput(self):
		self.assertEqual(True, issubclass(position.Position, data_input.DataInput))

	def testInit_gpsFieldIsOfTypeGPS(self):
		self.assertEqual(True, isinstance(self.pos._gps, gps.gps))

	def testGetData_callsGPSNext(self):
		global gps_next_called
		gps_next_called = False
		self.pos._gps.next = fake_gps_next
		self.pos.get_data()
		self.assertEqual(True, gps_next_called)

	def testGetData_returnsDictWithKeyLat(self):
		self.assertEqual(True, "lat" in self.pos.get_data().keys())

	def testGetData_returnsDictWithKeyLon(self):
		self.assertEqual(True, "lon" in self.pos.get_data().keys())
