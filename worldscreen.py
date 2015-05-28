""" The main screen for playing the game. Most of the player's actions take place here.
"""

from gamescreen import *
#PAUSE_PANE_WIDTH, PAUSE_PANE_HEIGHT = WIN_WIDTH/
#PAUSE_PANE_X, PAUSE_PANE_Y = 

class WorldScreen(GameScreen):
	""" MainGameScreen( ControlManager, Player ) -> MainGameScreen

	The main game screen is used when the game is not paused and the player is doing
	stuff or a cutscene is playing.

	Attributes:

	player: The player affected by this screen.
	"""
	def __init__(self, control_manager, player):
		GameScreen.__init__(self, control_manager)
		self.width, self.height = WIN_WIDTH, WIN_HEIGHT
		self.player = player

	def update(self):
		""" mgs.update( ) -> None

		Call update methods related to the game.
		"""
		self.draw_bg()
		self.level_update()
		#if not self.paused: self.level_update()
		#else: self.pause_update()

	def pause_update(self):
		""" mgs.pause_update( ) -> None

		Update the game in its paused state.
		"""
		pass
		#self.draw_pause_pane(self.screen_image)

	#def draw_pause_pane(self, screen):
	#	pause_pane = Surface(())

	def level_update(self):
		""" mgs.level_update( ) -> None

		Call the updates that will make objects in the level update physically and visually.
		"""
		self.player.world.update(False, False, False, False)

	def pause(self):
		""" mgs.pause_game( ) -> None

		Pause the game.
		"""
		self.paused = True

	def clear(self):
		""" mgs.level_update( ) -> None

		Revert the screen's contents to a black rectangle.
		"""
		self.contents = Surface((self.width, self.height))