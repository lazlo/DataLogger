import time
import json

class DataRecord():

	TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"

	def __init__(self, timestamp=None, measurements=None):
		if timestamp:
			self.timestamp = timestamp
		else:
			self.timestamp = time.strftime(self.TIMESTAMP_FORMAT)
		if measurements:
			self.measurements = measurements
		else:
			self.measurements = []

	def to_json(self):
		return json.dumps(self.__dict__)

	@staticmethod
	def from_json(input_str):
		data = json.loads(input_str)
		return DataRecord(data["timestamp"], data["measurements"])
