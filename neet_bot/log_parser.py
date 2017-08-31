# -*- coding: utf-8 -*-
import configparser
import logging
import os

import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %a %H:%M:%S')
LOGGER = logging.getLogger(__name__)


def get_current_path(filename):
	"""
	Gets current path.
	:return: current path
	"""
	dir_name = os.path.dirname(sys.argv[0])
	config = dir_name + '/' + filename
	if not os.path.isfile(config):
		LOGGER.info("Trying different path for '%s'", filename)
		dir_name = os.path.join(os.getcwd())
		config = dir_name + '/' + filename
		LOGGER.info(dir_name)
	return config


def get_api_from_config(file_, header, parameter):
	"""
	Gets api from config
	:param file_: file to check path
	:param header: header from config file
	:param parameter: parameter to find
	:return: api from config
	"""
	fullpath = get_current_path(file_)
	dir_name = os.path.dirname(fullpath)
	parser = configparser.SafeConfigParser()
	parser.read(dir_name + "/" + file_)
	return parser.get(header, parameter)


def _run_as_standalone():
	a = get_api_from_config("settings.conf", "Discord", "BOT_TOKEN")
	pass

if __name__ == "__main__":
	_run_as_standalone()