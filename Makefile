all:
	make -C data_logger vtest
package:
	python setup.py sdist
