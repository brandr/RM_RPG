from controls import *

class BattleControls(Controls):
	""" MapControls( Player ) -> MapControls

	The inventory controls are used to make item-based changes or to exit the inventory screen.

	Attributes:

	player: The Player whose inventory is controlled via these controls.
	"""

	def __init__(self, player):
		Controls.__init__(self)
		self.initialize_control_map(BATTLE_CONTROL_MAP)
		self.player = player

	def unpause(self, key, toggle):
		""" mc.unpause( str, bool ) -> None

		When the player presses enter, resume the game.
		"""
		if toggle: self.player.unpause_game()

	def move_cursor(self, key, toggle):
		""" mc.move_cursor( str, bool ) -> None

		Move the inventory cursor from its current position to select an item.
		"""
		pass
		"""
		if toggle:
			if key not in DIRECTION_MAP: return 
			direction = DIRECTION_MAP[key]
			self.control_manager.screen.move_cursor(direction)
		"""

move_cursor = BattleControls.move_cursor

DIRECTION_MAP = {
	K_LEFT:(-1, 0),
	K_RIGHT:(1, 0),
	K_UP:(0, -1),
	K_DOWN:(0, 1)
}

BATTLE_CONTROL_MAP = {
	K_LEFT:move_cursor,
	K_RIGHT:move_cursor,
	K_UP:move_cursor,
	K_DOWN:move_cursor
}