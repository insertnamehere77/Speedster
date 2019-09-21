import random

class GameObject():

	def __init__(self, icon, row = 0, col = 0):
		self.icon = icon
		self.row = row
		self.col = col


	def __eq__(self, other):
		if isinstance(other, GameObject):
			same_row = (self.row == self.row)
			same_col = (self.col == self.col)
			return (same_col and same_row)
		else:
			return False




class Game():

	def __init__(self):
		self._player = GameObject('🏎️', row = 2, col = 1)
		self._hazard = GameObject('🛢️', row = 0, col = 1)
		self.score = 0
		self.running = True


	def _format_row(self, items):
		row_str = '|{}\t{}\t{}|'.format(*items)
		return row_str


	def _update_hazard(self):

		if self._hazard.row == 2:
			self._hazard.row = 0
			self._hazard.col = random.randrange(3)
			self.score += 1

		else:
			self._hazard.row += 1
			


	def update(self):
		self._update_hazard()
		if self._player == self._hazard:
			self.running = False




	def _add_board_obj(self, board, obj):
		board[obj.row][obj.col] = obj.icon

	def move_left(self):
		self._player._col -= 1
		if self._player._col < 0:
			self._player._col = 0

	def move_right(self):
		self._player._col += 1
		if self._player._col > 2:
			self._player._col = 2


	def _render_game(self):
		board = [
			['', '', ''],
			['', '', ''],
			['', '', '']
		]

		self._add_board_obj(board, self._hazard)
		self._add_board_obj(board, self._player)

		row_strs = []
		for row in board:
			row_str = self._format_row(row)
			row_strs.append(row_str)

		return '\n'.join(row_strs)

	def _game_over_screen(self):
		return 'GAME OVER!\nScore: {}'.format(self.score)



	def __str__(self):
		if self.running:
			return self._render_game()
		else:
			return self._game_over_screen()





def main():
	game = Game()
	print(game)
	print('\n\n')
	game.update()
	print(game)
	print('\n\n')
	game.update()
	print(game)
	print('\n\n')
	game.update()
	print(game)
	print('\n\n')
	game.update()
	print(game)


if __name__ == '__main__':
	main()


