import unittest
import json

import config

class ConfigTestCase(unittest.TestCase):

	def setUp(self):
		self.cfg = config.Config()
		self.cfg.system_name = "cargoContainer-23"
		self.cfg.server_addr = "localhost"
		self.cfg.server_user = "eris"
		self.cfg.server_password = "fnord2342"
		self.cfg.server_upload_period_sec = 42
		self.cfg.server_poll_period_sec = 23
		self.cfg.data_inputs = [{"name": "Door Status", "class": "Pin"}]

	def testIsValid_returnsFalseWhenSystemNameIsEmpty(self):
		self.cfg.system_name = None
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsFalseWhenServerAddressIsEmpty(self):
		self.cfg.server_addr = None
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsFalseWhenServerUserIsEmpty(self):
		self.cfg.server_user = None
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsFalseWhenServerPasswordIsEmpty(self):
		self.cfg.server_password = None
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsFalseWhenServerUploadPeriodSecIsEmpty(self):
		self.cfg.server_upload_period_sec = None
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsFalseWhenServerPollPeriodSecIsEmpty(self):
		self.cfg.server_poll_period_sec = None
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsFalseWhenDataInputsIsEmpty(self):
		self.cfg.data_inputs = None
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsFalseWhenDataInputElementNameKeyMissing(self):
		self.cfg.data_inputs = [{}]
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsFalseWhenDataInputElementNameIsEmpty(self):
		self.cfg.data_inputs = [{"name": ""}]
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsFalseWhenDataInputElementNameIsNotUnique(self):
		self.cfg.data_inputs = [
			{"name": "Door"},
			{"name": "Door"}
		]
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsFalseWhenDataInputElementClassKeyMissing(self):
		self.cfg.data_inputs = [{"name": "Ignition"}]
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsFalseWhenDataInputElementClassIsEmpty(self):
		self.cfg.data_inputs = [{"name": "Ignition", "class": ""}]
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsFalseWhenDataInputElementClassHasNoMatchingClass(self):
		self.cfg.data_inputs = [{"name": "Ignition", "class": "DoesNotExist"}]
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsTrueWhenAllRequiredFieldsAreNotEmpty(self):
		self.assertEqual(True, self.cfg.is_valid())

	def testLoadFile_setsFieldsFromJSONFile(self):
		test_cfg_file = "data_logger_test_cfg.json"
		c1 = json.loads(open(test_cfg_file).read())
		c2 = config.Config()
		c2.load_file(test_cfg_file)
		self.assertEqual(c1, c2.__dict__)

	def testGetDataInput_returnsObjRefOnMatch(self):
		self.assertEqual(self.cfg.data_inputs[0], self.cfg.get_data_input("Door Status"))

	def testGetDataInput_returnsNoneOnMismatch(self):
		self.assertEqual(None, self.cfg.get_data_input("NameDoesNotExist"))

	def testGetDataInputsByClass_returnsListOfObjRefsOnMatch(self):
		expected = [
			{"name": "Door 1 Status", "class": "Pin"},
			{"name": "Door 2 Status", "class": "Pin"},
		]
		self.cfg.data_inputs = [
			{"name": "Camera", "class": "Video"},
			{"Name": "Position", "class": "Position"}
		]
		self.cfg.data_inputs.extend(expected)
		self.assertEqual(expected, self.cfg.get_data_inputs_by_class("Pin"))

if __name__ == "__main__":
	unittest.main()
