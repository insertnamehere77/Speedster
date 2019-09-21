import json, configparser
import requests





class SlackBot():

	_URL = 'https://slack.com/api/'

	"""docstring for DiscordBot"""
	def __init__(self, token):
		self.token = token




	def __del__(self):
		pass


	def send_msg(self, channel_id, msg, *blocks):

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
			"ts" : timestamp,
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


	def create_actions(self, *elements):

		block = {
			"type": "actions",
			"elements": elements
		}

		return block


	def create_button(self, text, value):

		block = {
			"type": "button",
			"text": {
				"type": "plain_text",
				"text": text,
				"emoji": True
			},
			"value": value
		}	

		return block





def main():

	config = configparser.ConfigParser()
	config.read('bot_config.cfg')
	
	token = config['slack']['token']

	speedster = SlackBot(token)

	left_button = speedster.create_button('⬅️', 'left')
	right_button = speedster.create_button('➡️', 'right')
	actions = speedster.create_actions(left_button, right_button)

	speedster.send_msg('DN4GLP64B', 'Morning', actions)


if __name__ == '__main__':
	main()



