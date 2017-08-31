# -*- coding: utf-8 -*-
import logging
import os
import sys
import urllib.request

import configparser
import discord
from bs4 import BeautifulSoup

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
	parser.read(dir_name + "/" + 'api.conf')
	return parser.get(header, parameter)


TOKEN = get_api_from_config("settings.conf", "Discord", "BOT_TOKEN")


def make_soup(url):
	req = urllib.request.Request(
		url,
		data=None,
		headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
		}
	)
	f = urllib.request.urlopen(req)
	soup_data = BeautifulSoup(f, "html.parser")
	return soup_data


def run_discord_bot():
	client = discord.Client()

	@client.event
	async def on_ready():
		LOGGER.info('Logged in as')
		LOGGER.info(client.user.name)
		LOGGER.info(client.user.id)
		LOGGER.info('------')

	@client.event
	async def on_message(message):
		auth_name = message.author  # 'Username#9445'
		author_display_name = message.author.display_name  # 'Username'
		auth_id = message.author.id  # '112200572063449011'
		auth_mention = message.author.mention  # ''<@112200572063449011>''
		message_content = message.content
		LOGGER.info(auth_name)
		LOGGER.info(author_display_name)
		LOGGER.info(auth_id)
		LOGGER.info(auth_mention)
		LOGGER.info(message_content)

		# if message.content.startswith('!test'):
		# 	counter = 0
		# 	.bitcoiN = await client.send_message(message.channel, 'Calculating messages...')
		# 	async for log in client.logs_from(message.channel, limit=100):
		# 		if log.author == message.author:
		# 			counter += 1
		#
		# 	await client.edit_message(.bitcoiN, 'You have {} messages {}.'.format(counter, auth_mention))
		# elif message.content.startswith('!sleep'):
		# 	await asyncio.sleep(5)
		# 	await client.send_message(message.channel, 'Done sleeping')

		if message.content.startswith('!talk'):
			tmp = await client.send_message(message.channel, 'Listening..')
			soup = make_soup("http://labs.bible.org/api/?passage=random")
			text = soup.text
			await client.edit_message(tmp, '{}.'.format(text))

	client.run(TOKEN)


def _run_as_standalone():
	run_discord_bot()


if __name__ == "__main__":
	_run_as_standalone()
