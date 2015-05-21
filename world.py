from camera import Camera, WIN_WIDTH, WIN_HEIGHT
from tile import Tile, TILE_SIZE

WORLD_WIDTH = 50
WORLD_HEIGHT = 50

class World:
	def __init__(self):
		self.screen = None
		self.player = None
		self.camera = Camera()
		self.initialize_tiles()

	def initialize_screen(self, screen_manager, game_screen):
		""" l.initialize_screen( ScreenManager, GameScreen ) -> None

		Associate this level with the given screen_manager and game_screen.
		"""
		self.screen_manager = screen_manager
		self.screen = game_screen.screen_image

	def initialize_tiles(self):
		self.tiles = []
		for y in xrange(WORLD_HEIGHT):
			self.tiles.append([])
			for x in xrange(WORLD_WIDTH): 
				t = Tile(x, y)
				self.tiles[y].append(t)

	def update(self, up, down, left, right):
		player = self.player
		self.camera.update(player)
		player.update()
		self.draw_tiles()
		self.screen.blit(player.world_image, self.camera.apply(player))
		
	def draw_tiles(self):
		for row in self.tiles:
			for t in row:
				if t: self.screen.blit(t.image, self.camera.apply(t))

	def add_player(self, player):
		self.player = player

	def add_tile(self, tile, x, y):
		self.tiles[y][x] = tile

	def tile_at(self, x, y):
		width, height = len(self.tiles[0]), len(self.tiles)
		if x < 0 or x > width: return None
		if y < 0 or y > height: return None
		return self.tiles[y][x]