from controlmanager import ControlManager
from battlecontrols import BattleControls
from battlescreen import BattleScreen
from worldcontrols import WorldControls
from worldscreen import WorldScreen
from pausecontrols import PauseControls
from pausescreen import PauseScreen

class ScreenManager:
	""" ScreenManager ( Surface, GameScreen, Player ) -> ScreenManager

	A manager object used to switch screens and controls during the game.

	Attributes:
	
	master_screen: the pygame screen (technically a Surface) that screen elements are drawn onto.

	current_screen: the current screen to be displayed. Only one may display at a time.

	player: the player associated with the current game session.
	"""

	def __init__(self, master_screen, current_screen, player = None):
		self.master_screen = master_screen
		self.set_current_screen(current_screen)
		self.player = player
		if(player != None):
			player.screen_manager = self

	def set_current_screen(self, screen):
		""" sm.set_current_screen( GameScreen ) -> None

		Store the given screen to the one that should be shown.
		"""
		self.current_screen = screen
		screen.screen_manager = self

	def set_controls(self, controls):
		""" sm.set_controls( Controls ) -> None

		Set a control scheme while leaving the current screen the same.
		"""
		self.current_screen.control_manager.switch_controls(controls)

	def process_event(self, event):
		""" sm.process_event( Event ) -> None

		Process a pygame event based on the current control scheme.
		"""
		self.current_screen.control_manager.process_event(event)

	def update_current_screen(self):
		""" sm.update_current_screen( ) -> None

		Tell the current screen to update its visual elements.
		"""
		self.current_screen.update()

	def draw_screen(self):
		""" sm.draw_screen( ) -> None

		The screen manager draws its screen image onto the screen that the player would see.
		"""
		self.current_screen.draw_screen(self.master_screen)

	def switch_to_battle_screen(self, player, monsters, tile):
		controls = BattleControls(player)
		control_manager = ControlManager(controls)
		battle_screen = BattleScreen(control_manager, player, monsters, tile)
		self.set_current_screen(battle_screen)

	def switch_to_world_screen(self, player):
		controls = WorldControls(player)
		control_manager = ControlManager(controls)
		world_screen = WorldScreen(control_manager, player)
		self.set_current_screen(world_screen)
		player.world.initialize_screen(self, world_screen)
	
	def switch_to_pause_screen(self, player):
		controls = PauseControls(player)
		control_manager = ControlManager(controls)
		pause_screen = PauseScreen(control_manager, player)
		self.set_current_screen(pause_screen)