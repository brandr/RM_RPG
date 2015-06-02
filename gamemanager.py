import pygame
from pygame import *
from player import Player
from world import World
from worldcontrols import WorldControls
from worldscreen import WorldScreen
from controlmanager import ControlManager
from screenmanager import ScreenManager

FRAMES = 100

WIN_WIDTH = 800
WIN_HEIGHT = 640

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

class GameManager:
	"""GameManager () -> GameManager

	This is the screen used to play the game.
	(Will add more description as more stuff is implemented.)

	Attributes: None
	"""
	def __init__(self):
		pass

	def run_game(self):
		master_screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
		pygame.display.set_caption("RM RPG")
		timer = pygame.time.Clock()

		#TEMP
		world = World()
		player = Player(world)
		world.add_player(player, 35, 20)
		#TEMP

		game_controls = WorldControls(player) # TODO: specify what kind of controls should be used at the start of the game and use a different constructor.
		control_manager = ControlManager(game_controls)
		main_screen = WorldScreen(control_manager, player) #TODO: specify type of screen
		screen_manager = ScreenManager(master_screen, main_screen, player)

		world.initialize_screen(screen_manager, main_screen)

		while 1:
			timer.tick(FRAMES) # make this value lower to make the game run slowly for testing. (use about 40-50 I think)
 			for e in pygame.event.get():
				screen_manager.process_event(e)
			screen_manager.update_current_screen()
			self.draw_screen(screen_manager)
			pygame.display.update()
			"""
			timer.tick(100)
			for e in pygame.event.get():
				if e.type == QUIT: raise SystemExit, "QUIT"
			screen.blit(player.image, (0, 0))
			pygame.display.update()
			"""
		"""GM.runGame (...) -> None

		Run the game using a pygame screen.

		Attributes:
		master_screen: the pygame screen onto which everything will be displayed
		during the game.
		"""

		"""
		start_dungeon, dungeon_name, master_screen = self.build_dungeon_and_screen() 
		world = World(start_dungeon) # TODO: implement world (contains all dungeons, along with other global data-- how to do this?)
		"""
		"""
		pygame.display.set_caption(dungeon_name)
		timer = pygame.time.Clock()

		player_animations = Player.load_player_animation_set()
		start_level = start_dungeon.start_level()
		if not start_level: raise SystemExit, "ERROR: no starting level specified."

		player = Player(player_animations, start_level)
		start_level.addPlayer(player)

		game_controls = MainGameControls(player) # TODO: consider how controls may parse buttons differently for different screens.
		control_manager = ControlManager(game_controls)
		main_screen = MainGameScreen(control_manager, player) 
		screen_manager = ScreenManager(master_screen, main_screen, player)
		start_level.initialize_screen(screen_manager, main_screen)

		# TEMP for testing cutscenes
		# TODO: figure out how to better generalize cutscenes (start by figuring out how to generalize their actions)
		player_right_method = GameManager.temp_player_right
		player_right_action = GameAction(player_right_method, 60, None, player)
		actions = [player_right_action] 		# TODO: action for player moving right
		test_cutscene = Cutscene(actions)
		player.current_level.begin_cutscene(test_cutscene)

		#TEMP
		pygame.mixer.init()
		pygame.mixer.music.load('./music/test_song.mp3')
		pygame.mixer.music.play(-1)

		pygame.mixer.music.set_volume(0) # comment out this line to enable music.
		#TEMP

		while 1:
			timer.tick(FRAMES) # make this value lower to make the game run slowly for testing. (use about 40-50 I think)
 			for e in pygame.event.get():
				screen_manager.process_event(e)
			screen_manager.update_current_screen()
			self.draw_screen(screen_manager)
			pygame.display.update()
		"""

	def draw_screen(self, screen_manager):
		""" gm.draw_screen( ScreenManager) -> None

		Tell the screen manager to draw whatever should be onscreen.
		"""
		screen_manager.draw_screen()