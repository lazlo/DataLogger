import data_input
import gps

class Position(data_input.DataInput):

	def __init__(self, name):
		data_input.DataInput.__init__(self, name)
		self._gps = gps.gps()

	def get_data(self):
		d = {"lat": None, "lon": None}
		return d
