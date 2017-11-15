import data_store
import data_input

class DataLogger():

	def __init__(self, config):
		self.config = config
		self.data_store = data_store.DataStore()
		self.data_inputs = []
		for di in self.config.data_inputs:
			self.data_inputs.append(data_input.DataInput("Foo"))
