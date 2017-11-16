import data_input
from gps3 import gps3

class Position(data_input.DataInput):

	def __init__(self, name):
		data_input.DataInput.__init__(self, name)
		self._gpsd_sock = gps3.GPSDSocket()
		self._gps_stream = gps3.DataStream()

	def get_data(self):
		d = {"lat": None, "lon": None}
		return d
