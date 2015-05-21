from gameimage import GameImage
from tile import TILE_SIZE
from partymember import PartyMember
from pygame import Surface, Rect, Color

import random

UP, DOWN, LEFT, RIGHT = "up", "down", "left", "right"

class Player(GameImage):
	def __init__(self, world):
		GameImage.__init__(self)
		self.world_image = Surface((16, 16))
		self.rect = Rect(0, 0, 16, 16)
		self.world_image.fill(Color("#FF0000"))
		self.world = world
		self.button_press_map = DEFAULT_BUTTON_PRESS_MAP
		self.party = [PartyMember("Bernard", 10), PartyMember("Daniel", 8), PartyMember("Staniel", 12)]

	def update(self):
		up, down, left, right = self.button_press_map[UP], self.button_press_map[DOWN], self.button_press_map[LEFT], self.button_press_map[RIGHT]
		if up and not down: self.rect.top -= 1
		if down and not up: self.rect.top += 1
		if left and not right: self.rect.left -= 1
		if right and not left: self.rect.left += 1
		tile = self.current_tile()
		self.roll_encounter(tile)

	def deactivate(self):
		self.button_press_map[UP], self.button_press_map[DOWN], self.button_press_map[LEFT], self.button_press_map[RIGHT]

	def roll_encounter(self, tile):
		roll = random.random()
		if roll < tile.base_encounter_rate/100000.0: 
			monster_party = tile.roll_monster_party()
			self.begin_encounter(monster_party)

	def begin_encounter(self, monsters):
		self.deactivate()
		self.world.screen_manager.switch_to_battle_screen(self, monsters, self.current_tile())

	def current_tile(self):
		x, y = self.rect.left/TILE_SIZE, self.rect.top/TILE_SIZE
		return self.world.tile_at(x, y)

DEFAULT_BUTTON_PRESS_MAP = {UP:False, DOWN:False, LEFT:False, RIGHT:False}