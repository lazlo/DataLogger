import unittest

import config

class ConfigTestCase(unittest.TestCase):

	def setUp(self):
		self.cfg = config.Config()
		self.cfg.system_name = "cargoContainer-23"
		self.cfg.server_addr = "http://localhost:8111"
		self.cfg.server_login = "eris"
		self.cfg.server_password = "fnord2342"

	def testIsValid_returnsFalseWhenSystemNameIsEmpty(self):
		self.cfg.system_name = None
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsFalseWhenServerAddressIsEmpty(self):
		self.cfg.server_addr = None
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsFalseWhenServerLoginIsEmpty(self):
		self.cfg.server_login = None
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsFalseWhenServerPasswordIsEmpty(self):
		self.cfg.server_password = None
		self.assertEqual(False, self.cfg.is_valid())

	def testIsValid_returnsTrueWhenAllRequiredFieldsAreNotEmpty(self):
		self.assertEqual(True, self.cfg.is_valid())

if __name__ == "__main__":
	unittest.main()
