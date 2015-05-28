from controls import *
from player import UP, DOWN, LEFT, RIGHT

class WorldControls(Controls):
	""" WorldControls( Player ) -> WorldControls

	Can handle various contexts, but they should all be associated with
	the main game.

	Attributes:

	player: the player associated with these controls. 

	direction_map: the buttons used in the main game (as strings) mapped to the actions they cause.
	"""

	def __init__(self, player):
		Controls.__init__(self)
		self.player = player
		self.load_controls()

	def load_controls(self):
		self.control_map = WORLD_CONTROL_MAP

	def move_up(self, key, toggle):
		""" mgc.move_up( str, bool ) -> None

		Up key action.
		"""
		self.player.button_press_map[UP] = toggle

	def move_down(self, key, toggle):
		""" mgc.move_down( str, bool ) -> None

		Down key action.
		"""
		self.player.button_press_map[DOWN] = toggle

	def move_left(self, key, toggle):
		""" mgc.move_left( str, bool ) -> None

		Left key action.
		"""
		self.player.button_press_map[LEFT] = toggle

	def move_right(self, key, toggle):
		""" mgc.move_right( str, bool ) -> None

		Right key action.
		"""
		self.player.button_press_map[RIGHT] = toggle

	def press_enter(self, key, toggle):
		pass

	def press_escape(self, key, toggle):
		if toggle: 
			self.player.deactivate()
			self.control_manager.screen.pause()
			self.control_manager.screen.screen_manager.switch_to_pause_screen(self.player)

move_up, move_down, move_left, move_right = WorldControls.move_up, WorldControls.move_down, WorldControls.move_left, WorldControls.move_right

WORLD_CONTROL_MAP = {K_UP:move_up, K_DOWN:move_down, K_LEFT:move_left, K_RIGHT:move_right, K_RETURN:WorldControls.press_enter, K_ESCAPE:WorldControls.press_escape}
DIRECTION_MAP = {K_UP:(0, -1), K_DOWN:(0, 1), K_LEFT:(-1, 0), K_RIGHT:(1, 0)}