import random, collections

# Represents objects in the game world
class GameObject():

	# Icon should be the str used to represent obj
	# Row and Col are where the obj is located on the road
	def __init__(self, icon, row = 0, col = 0):
		self.icon = icon
		self.row = row
		self.col = col


	# Collision detection 
	# Used the __eq__ function so I can use the "in" keyword
	def __eq__(self, other):
		if isinstance(other, GameObject):
			same_row = (self.row == other.row)
			same_col = (self.col == other.col)
			return (same_col and same_row)
		else:
			return False



		


# A single running instance of the game
class Game():

	# Config vars
	_MAX_HAZARDS = 2
	_NUM_ROWS = 3
	_NUM_COLS = 3

	_PLAYER_ICON = '🏎️'
	_CRASH_ICON = '💥'
	_HAZARD_ICONS = ['🛢️', '🚘', '🚔', '🚖', '🚍', '🚧']



	def __init__(self):
		start_row = self._NUM_ROWS - 1
		start_col = int(self._NUM_COLS / 2)
		self._player = GameObject(self._PLAYER_ICON, row = start_row, col = start_col)
		self._hazards = []

		self.score = 0
		self.running = True
		self.crashed = False


	# Used to display the game as a string
	def __str__(self):
		if self.running:
			return self._render_game()
		else:
			return self._game_over()
			

	# Updates the game state
	def update(self):

		# If crashed last update, end game
		if (self.crashed):
			self.running = False
			return

		# If player crashed, update icon
		if self._player in self._hazards:
			self.crashed = True
			self._player.icon = self._CRASH_ICON
			return

		# Update our current hazards
		for hazard in list(self._hazards):
			self._update_hazard(hazard)

		# Spawn more hazards if needed
		if len(self._hazards) < self._MAX_HAZARDS:
			self._add_hazard()


	# Player moves left
	def move_left(self):
		if self.crashed:
			return

		self._player.col -= 1
		# Keeping player in bounds
		if self._player.col < 0:
			self._player.col = 0



	# Player moves right
	def move_right(self):
		if self.crashed:
			return

		self._player.col += 1
		# Keeping player in bounds
		if self._player.col > (self._NUM_COLS - 1):
			self._player.col = 2


	# Private Methods


	# Drawing Functions

	# Returns a string of the currently running game
	def _render_game(self):

		board = self._create_board()

		# Adding all the hazards to our board
		for hazard in self._hazards:
			self._add_board_obj(board, hazard)

		# Adding player
		self._add_board_obj(board, self._player)

		# Creating the strs for each row
		row_strs = []
		for row in board:
			row_str = self._format_row(row)
			row_strs.append(row_str)

		# Finally joining the row_strs together
		return '\n'.join(row_strs)



	# Returns the str matrix used when displaying the game
	def _create_board(self):
		empty_space = '_'
		board = []
		for r in range(self._NUM_ROWS):
			curr_row = []

			for c in range(self._NUM_COLS):
				curr_row.append(empty_space)

			board.append(curr_row)

		return board



	# Adds a GameObj to the board matrix
	def _add_board_obj(self, board, obj):
		board[obj.row][obj.col] = obj.icon



	# Formats a board row
	def _format_row(self, items):
		row_str = '|{}\t{}\t{}'.format(*items)
		return row_str



	# Returns a string of the game over screen
	def _game_over(self):
		return 'GAME OVER!\nYour Score: {}'.format(self.score)



	# Updating functions


	# Returns one of the possible hazard icons
	def _get_hazard_icon(self):
		icon = random.choice(self._HAZARD_ICONS)
		return icon

	# Updates the given hazard
	def _update_hazard(self, hazard):

		# Hazard off screen, gets deleted
		if hazard.row == 2:
			self._hazards.remove(hazard)
			self.score += 1

		# Keeps traversing down the col
		else:
			hazard.row += 1


	# Adds a new hazard when one has been passed
	def _add_hazard(self):
		icon = self._get_hazard_icon()
		col = random.randrange(self._NUM_COLS)
		hazard = GameObject(icon, row = 0, col = col)

		self._hazards.append(hazard)









# Class to hold the high scores across multiple instances of the game
class LeaderBoard():

	# Config vars
	_MAX_NUM_SCORES = 3
	_DEFAULT_NAMES = ['Malibu', 'Lacrosse', 'Denali']

	# Represents a single score on the board
	Score = collections.namedtuple('Score', 'name points')

	def __init__(self):
		self._init_scores()
		self._sort_scores()


	# Adds a new score entry
	def add_score(self, name, points):
		score = LeaderBoard.Score(name, points)
		self._scores.append(score)

		self._sort_scores()
		self._trim_scores()



	# Used to display the scores
	def __str__(self):
		result = 'TOP SCORES:'
		curr_place = 1
		for entry in self._scores:
			result += '\n'
			result += '{}. {} \t {}'.format(curr_place, entry.name, entry.points)
			curr_place += 1

		return result


	# PRIVATE METHODS

	# Sets the initial dummy scores
	def _init_scores(self):
		self._scores = []
		curr_score = 10

		for name in self._DEFAULT_NAMES:
			score = LeaderBoard.Score(name, curr_score)
			self._scores.append(score)
			curr_score += 5



	# Sorts self._scores in descending order
	def _sort_scores(self):
		# This lambda returns the key we sort scores by
		getScore = (lambda x : x.points)
		self._scores = sorted(self._scores, reverse = True, key = getScore)



	# Trims our scores to _MAX
	def _trim_scores(self):
		self._scores = self._scores[:self._MAX_NUM_SCORES]







def main():
	pass


if __name__ == '__main__':
	main()


