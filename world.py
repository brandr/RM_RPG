from camera import Camera, WIN_WIDTH, WIN_HEIGHT
from tile import Tile, TILE_SIZE, MEADOW_GRASS, FOREST_GRASS
from tileentity import TileEntity, HEALING_TOTEM
from pygame import Surface

WORLD_WIDTH = 50
WORLD_HEIGHT = 50

class World:
	def __init__(self):
		self.screen = None
		self.player = None
		self.camera = Camera()
		self.initialize_tiles()
		self.flash_counter = [0, 0]
		self.flash_image = Surface((WIN_WIDTH, WIN_HEIGHT))

	def initialize_screen(self, screen_manager, game_screen):
		""" l.initialize_screen( ScreenManager, GameScreen ) -> None

		Associate this level with the given screen_manager and game_screen.
		"""
		self.screen_manager = screen_manager
		self.screen = game_screen.screen_image

	def initialize_tiles(self):	#TEMP
		self.tiles = []
		for y in xrange(WORLD_HEIGHT):
			self.tiles.append([])
			for x in xrange(WORLD_WIDTH): 
				t = Tile(x, y, MEADOW_GRASS)	
				self.tiles[y].append(t)
		for y in range(WORLD_HEIGHT*3/8, WORLD_HEIGHT*3/8 + WORLD_HEIGHT/4):
			for x in range(WORLD_WIDTH*3/8, WORLD_WIDTH*3/8 + WORLD_WIDTH/4):
				self.tiles[y][x] = Tile(x, y, FOREST_GRASS)
		self.tiles[WORLD_HEIGHT/2][WORLD_WIDTH/2].set_entity(TileEntity(HEALING_TOTEM))

	def update(self, up, down, left, right):
		player = self.player
		self.camera.update(player)
		player.update()
		self.draw_tiles()
		self.screen.blit(player.world_image, self.camera.apply(player))
		self.flash_update()

	def begin_flash(self, color, duration):
		self.flash_counter = [duration, duration]
		self.flash_image.fill(color)
		
	def draw_tiles(self):
		for row in self.tiles:
			for t in row:
				if t: self.screen.blit(t.image, self.camera.apply(t))

	def flash_update(self):
		if self.flash_counter[0] <= 0: return
		half = self.flash_counter[1]/2
		if half <= 0: return
		current = self.flash_counter[0]
		if current > half: alpha = int(255.0 - ((current - half)/float(half))*255.0)
		else: alpha = int(((current)/float(half))*255.0)
		self.flash_image.set_alpha(alpha)
		self.screen.blit(self.flash_image, (0, 0))
		self.flash_counter[0] -= 1

	def add_player(self, player):
		self.player = player

	def add_tile(self, tile, x, y):
		self.tiles[y][x] = tile

	def tile_at(self, x, y):
		width, height = len(self.tiles[0]), len(self.tiles)
		if x < 0 or x > width: return None
		if y < 0 or y > height: return None
		return self.tiles[y][x]