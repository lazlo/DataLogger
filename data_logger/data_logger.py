import data_store
import data_input

class DataLogger():

	def __init__(self, config):
		self.config = config
		self.data_store = data_store.DataStore()
		self.data_inputs = []
		for di_cfg in self.config.data_inputs:
			di_class = getattr(data_input, di_cfg["class"])
			di_obj = di_class(di_cfg["name"])
			self.data_inputs.append(di_obj)

	def get_data(self):
		self.data_inputs[0].get_data()
