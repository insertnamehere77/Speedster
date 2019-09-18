import json, enum, configparser
import requests


class Position(enum.IntEnum):
	LEFT = 0
	MID = 1
	RIGHT = 2


class Driver():

	def __init__(self):
		self._avatar = '🏎️'
		self._position = Position.MID


class Road():

	_HAZARD = '🛢️'

	def __init__(self):
		self._player = Driver()


	def _row(self, items):
		row_str = '|{}\t{}\t{}|'.format(*items)
		return row_str


	def __str__(self):
		items = ['', '', '']
		items[self._player._position] = self._player._avatar
		items[0] = self._HAZARD
		return self._row(items)














class SlackBot():

	_URL = 'https://slack.com/api/'

	"""docstring for DiscordBot"""
	def __init__(self, token):
		self.token = token




	def __del__(self):
		pass


	def send_msg(self, channel_id, msg, blocks = None):

		endpoint = 'chat.postMessage'

		payload = {
			"text" : msg,
			"channel" : channel_id,
			"blocks" : blocks
		}


		self._post_api(endpoint, payload)


	def update_msg(self, channel_id, timestamp, msg, blocks = None):

		endpoint = "chat.update"

		payload = {
			"text" : msg,
			"channel" : channel_id,
			"ts" : timestamp
		}

		self._post_api(endpoint, payload)





	def _post_api(self, endpoint, payload):
		headers = self._headers()
		url = self._URL + endpoint
		response = requests.post(url = url, data = json.dumps(payload), headers = headers)






	# Creates the header for any HTTP calls
	def _headers(self):
		headers = {
			"Content-type" : "application/json",
			"Authorization": "Bearer " + self.token
		}
		return headers


	



def main():

	config = configparser.ConfigParser()
	config.read('bot_config.cfg')
	
	token = config['slack']['token']

	bot = SlackBot(token)
	bot.send_msg('DN4GLP64B', 'Morning')


if __name__ == '__main__':
	main()



