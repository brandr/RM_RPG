from gamescreen import GameScreen, WHITE
from camera import WIN_WIDTH, WIN_HEIGHT
from pygame import Surface, Color, font

MONSTER_FLOOR_Y = 300

UI_X, UI_Y = 0, WIN_HEIGHT*2/3
PARTY_DATA_X, PARTY_DATA_Y = UI_X, UI_Y
PARTY_DATA_WIDTH, PARTY_DATA_HEIGHT = 200, WIN_HEIGHT - UI_Y

class BattleScreen(GameScreen):
	""" MainGameScreen( ControlManager, Player ) -> MainGameScreen

	The main game screen is used when the game is not paused and the player is doing
	stuff or a cutscene is playing.

	Attributes:

	player: The player affected by this screen.
	"""
	def __init__(self, control_manager, player, monsters, tile):
		GameScreen.__init__(self, control_manager)
		self.width, self.height = WIN_WIDTH, WIN_HEIGHT
		self.player = player
		self.monsters = monsters
		self.bg = self.generate_bg(tile)
		self.ui_font = font.Font("./fonts/FreeSansBold.ttf", 16)

	def update(self):
		""" mgs.update( ) -> None

		Call update methods related to the game.
		"""
		self.screen_image.blit(self.bg, (0, 0))
		self.draw_monsters()
		self.draw_ui()

	def generate_bg(self, tile):
		#TODO: generate bg based on tile
		bg = Surface((WIN_WIDTH, WIN_HEIGHT))
		bg.fill(tile.bg_color)
		return bg

	def draw_monsters(self):
		x_offset = 20
		for m in self.monsters.monsters:
			self.screen_image.blit(m.image, (x_offset, MONSTER_FLOOR_Y - m.image.get_height()))
			x_offset += 100

	def draw_ui(self):
		ui_pane = Surface((WIN_WIDTH, WIN_HEIGHT - UI_Y))
		self.draw_party_data(ui_pane)
		#TODO: blit ui components here
		self.screen_image.blit(ui_pane, (UI_X, UI_Y))

	def draw_party_data(self, pane):
		data_pane = Surface((PARTY_DATA_WIDTH, PARTY_DATA_HEIGHT))
		y_offset = 8
		for p in self.player.party:
			name = p.name
			name_image = self.ui_font.render(name, True, WHITE)
			data_pane.blit(name_image, (8, y_offset))

			hp_text = str(p.hitpoints[0]) + "/" + str(p.hitpoints[1])
			hp_image = self.ui_font.render(hp_text, True, WHITE)
			data_pane.blit(hp_image, (100, y_offset))
			y_offset += 40
		pane.blit(data_pane, (0, 0))

	def pause_update(self):
		""" mgs.pause_update( ) -> None

		Update the game in its paused state.
		"""
		pass

	def clear(self):
		""" mgs.level_update( ) -> None

		Revert the screen's contents to a black rectangle.
		"""
		self.contents = Surface((self.width, self.height))