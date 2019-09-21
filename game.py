import enum

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