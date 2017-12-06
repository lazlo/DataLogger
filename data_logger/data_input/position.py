import data_input
from gps3 import gps3

class Position(data_input.DataInput):

	def __init__(self, name, args=None):
		data_input.DataInput.__init__(self, name, args)
		self._gpsd_sock = gps3.GPSDSocket()
		self._gps_stream = gps3.DataStream()

	def get_data(self):
		d = {"lat": None, "lon": None}
		return d
