#
# System to monitor
#  - position (via GPS)
#  - temperature (via I2C sensors)
#  - status of various switch contacts (via GPIOs)
#
# The data collected will be forwarded via HTTP and stored locally if the connection
# is not available.

import data_logger

def main():
	cfg = data_logger.Config()
	cfg.load_file("data_logger_test_cfg.json")
	dl = data_logger.DataLogger(cfg)
	dl.update()

if __name__ == "__main__":
	main()
