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

class DataRecord():

	def __init__(self):
		self.timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
		self.measurements = []
