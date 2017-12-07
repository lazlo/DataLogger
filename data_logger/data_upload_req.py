import json
import custom_json

class DataUploadRequest():
	def __init__(self, logger_name):
		self.logger_name = logger_name
		self.records = []

	def to_json(self):
		s = json.dumps(self.__dict__, cls=custom_json.CustomJSONEncoder)
		s = s.replace("logger_name", "LoggerName")
		return s
