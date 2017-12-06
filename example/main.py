#!/usr/bin/python

#
# System to monitor
#  - position (via GPS)
#  - temperature (via I2C sensors)
#  - status of various switch contacts (via GPIOs)
#
# The data collected will be forwarded via HTTP and stored locally if the connection
# is not available.

import data_logger
import sys

def main():
	cfg_file = data_logger.DataLogger.DEFAULT_CONFIG_FILE_NAME
	if len(sys.argv) > 1:
		cfg_file = sys.argv[1]
	cfg = data_logger.Config()
	cfg.load_file(cfg_file)
	dl = data_logger.DataLogger(cfg)
	while True:
		dl.update()

if __name__ == "__main__":
	main()
