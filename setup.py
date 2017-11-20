from setuptools import setup

setup(
	name = "data-logger",
	version = "0.1",
	author = "Laszlo Sitzer",
	author_email = "lazlo@esys.de",
	description = "Collects data from sensors and uploads it to a server.",
	url = "http://github.com/lazlo/DataLogger",
	packages = ["data_logger", "data_logger/data_input"]
)
