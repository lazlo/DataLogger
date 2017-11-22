# TODO Allow transformation of object to the following format
# {
#     "LoggerName": "SomeName",
#     "Records": [
#         {"Timestamp": "2017-04-28T00:00:00",
#          "Measurements": [44.44, 55.55, 66.66],
#         }
#     ]
# }
import time
import json

class DataRecord():

	def __init__(self, timestamp=None, measurements=None):
		if timestamp:
			self.timestamp = timestamp
		else:
			self.timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
		if measurements:
			self.measurements = measurements
		else:
			self.measurements = []

	def to_json(self):
		return json.dumps(self.__dict__)

	@staticmethod
	def from_json_string(input_str):
		data = json.loads(input_str)
		return DataRecord(data["timestamp"], data["measurements"])
