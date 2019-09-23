# encoding=utf8
import threading, time, json
import flask
import slack_bot, speedster


# Bot to talk to slack
bot = slack_bot.create_config_bot()

# Flask app to listen to slack
app = flask.Flask('speedster')

# Controls made using block kit for user to interact with
_LEFT_BUTTON = bot.create_button('⬅️', 'left')
_RIGHT_BUTTON = bot.create_button('➡️', 'right')
_CONTROLS = bot.create_actions(_LEFT_BUTTON, _RIGHT_BUTTON)

# All active games
curr_games = {}

# Time in between updates, needed for Slack rate limiting
_UPDATE_DELAY = 2

# Top scores to display on game over
leaderboard = speedster.LeaderBoard()



# Function to run a game until completion
# Our child threads run this
def run_game(channel_id, curr_game):

	# Sending the initial screen and control messages
	game_str = str(curr_game)
	screen_resp_body = bot.send_msg(channel_id, game_str)
	screen_ts = screen_resp_body['ts']

	controls_resp_body = bot.send_msg(channel_id, '', _CONTROLS)
	controls_ts = controls_resp_body['ts']


	# Game loop
	while curr_game.running:
		time.sleep(_UPDATE_DELAY)
		curr_game.update()
		game_str = str(curr_game)
		bot.update_msg(channel_id, screen_ts, game_str)



	# Game over, post to leaderboard
	leaderboard.add_score(channel_id, curr_game.score)

	# Display final score and leaderboard
	game_str = str(curr_game)
	bot.update_msg(channel_id, screen_ts, game_str)
	
	board_str = str(leaderboard)
	bot.update_msg(channel_id, controls_ts, board_str)

	# Remove from currently running games
	del curr_games[channel_id]



# Starts an instance of the game and it's game thread
def start_game(channel_id):
	new_game = speedster.Game()
	curr_games[channel_id] = new_game

	thread = threading.Thread(target = run_game, args = [channel_id, new_game])
	thread.start()


# Move the player in the channel's currently running game
def move_player(channel_id, move):
	curr_game = curr_games[channel_id]

	if move == 'right':
		curr_game.move_right()
	else:
		curr_game.move_left()



# Endpoint to move the player
@app.route('/move', methods=['POST'])
def move_player_endpoint():
	form = flask.request.form.to_dict()
	payload = json.loads(form['payload'])

	channel_id = payload['channel']['id']
	button_val = payload['actions'][0]['value']


	move_player(channel_id, button_val)
	

	return '', 200


# Endpoint to start the game
@app.route('/start', methods=['POST'])
def start_game_endpoint():
	form = flask.request.form.to_dict()
	channel_id = form['channel_id']
	
	start_game(channel_id)

	return '', 200


@app.route('/', methods = ['GET'])
def root_endpoint():
	return 'I\'m up', 200



if __name__ == '__main__':
	app.run(port = 5000, debug = True)


