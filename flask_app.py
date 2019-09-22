# encoding=utf8
import threading, time, json
import flask
import slack_bot, game

app = flask.Flask('speedster')

curr_games = {}



bot = slack_bot.create_config_bot()



left_button = bot.create_button('⬅️', 'left')
right_button = bot.create_button('➡️', 'right')
controls = bot.create_actions(left_button, right_button)


# test_game = game.Game()
# game_str = str(test_game)
# response_body = bot.send_msg('DN4GLP64B', game_str)
# response_body = bot.send_msg('DN4GLP64B','', controls)

def run_game(channel_id, curr_game):

	print('Game starting!')

	game_str = str(curr_game)
	response_body = bot.send_msg(channel_id, game_str)
	bot.send_msg(channel_id, '', controls)
	timestamp = response_body['ts']

	while curr_game.running:
		print('Game loop')
		time.sleep(2)
		curr_game.update()
		game_str = str(curr_game)
		bot.update_msg(channel_id, timestamp, game_str)

	game_str = str(curr_game)
	bot.update_msg(channel_id, timestamp, game_str)
	del curr_games[channel_id]




def start_game(channel_id):
	new_game = game.Game()
	curr_games[channel_id] = new_game

	thread = threading.Thread(target = run_game, args = [channel_id, new_game])
	thread.start()



def move_player(channel_id, move):
	curr_game = curr_games[channel_id]

	if move == 'right':
		curr_game.move_right()
	else:
		curr_game.move_left()




@app.route('/move', methods=['POST'])
def test_move():
	form = flask.request.form.to_dict()
	payload = json.loads(form['payload'])

	channel_id = payload['channel']['id']
	button_val = payload['actions'][0]['value']


	move_player(channel_id, button_val)
	

	return '', 200



@app.route('/', methods=['POST'])
def test_endpoint():
	form = flask.request.form.to_dict()
	channel_id = form['channel_id']
	
	start_game(channel_id)

	return '', 200



if __name__ == '__main__':
	app.run(port = 5000, debug = True)

