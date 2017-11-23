import json

class CustomJSONEncoder(json.JSONEncoder):

	def default(self, obj):
		if hasattr(obj, "__dict__"):
			return obj.__dict__
		else:
			return json.JSONEncoder.default(self, obj)
