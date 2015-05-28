from controls import *

class PauseControls(Controls):
	""" MapControls( Player ) -> MapControls

	The inventory controls are used to make item-based changes or to exit the inventory screen.

	Attributes:

	player: The Player whose inventory is controlled via these controls.
	"""

	def __init__(self, player):
		Controls.__init__(self)
		self.initialize_control_map(PAUSE_CONTROL_MAP)
		self.player = player

	def move_cursor(self, key, toggle):
		""" mc.move_cursor( str, bool ) -> None

		Move the inventory cursor from its current position to select an item.
		"""
		if not toggle: return
		#if not self.battle_state() in BATTLE_MOVE_CURSOR_MAP: return
		direction = DIRECTION_MAP[key]
		self.control_manager.screen.move_cursor(direction)

	def press_enter(self, key, toggle):
		if toggle: self.control_manager.screen.press_enter()

	def press_escape(self, key, toggle):
		if toggle: self.control_manager.screen.press_escape()

move_cursor = PauseControls.move_cursor
press_enter = PauseControls.press_enter
press_escape = PauseControls.press_escape

DIRECTION_MAP = {
	K_LEFT:(-1, 0),
	K_RIGHT:(1, 0),
	K_UP:(0, -1),
	K_DOWN:(0, 1)
}

PAUSE_CONTROL_MAP = {
	K_LEFT:move_cursor,
	K_RIGHT:move_cursor,
	K_UP:move_cursor,
	K_DOWN:move_cursor,
	K_RETURN:press_enter,
	K_ESCAPE:press_escape
}