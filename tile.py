from gameimage import GameImage, load_image_file
from monsterfactory import *
from monsterparty import MonsterParty
from pygame import Rect, Color
import random

TILE_SIZE = 16

class Tile(GameImage):
	def __init__(self, x = 0, y = 0):
		GameImage.__init__(self)
		self.image = load_image_file("./images", "default_grass_1.bmp")
		self.rect = Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
		self.base_encounter_rate = 500
		self.encounter_data = DEFAULT_ENCOUNTER_DATA
		self.bg_color = Color("#00BB00")	#TEMP. base this and encounter rate on the type of tile.

	def roll_monster_party(self):
		first_monster = self.roll_monster()
		monsters = [first_monster]
		roll_goal = .4
		while len(monsters) < MAX_MONSTERS:
			roll = random.random()
			if roll < roll_goal: monsters.append(self.roll_monster())
			else: break
		party = MonsterParty(monsters)
		return party

	def roll_monster(self):
		roll_goal = 0
		roll = random.random()
		for data in self.encounter_data:
			roll_goal += data[0]
			if roll < roll_goal:
				key = data[1]
				break
		monster = generate_monster(key)
		return monster

DEFAULT_ENCOUNTER_DATA = [
	(.4, SPARROW), (.5, GRASS_BEING), (.1, ALPHA_BEETLE)
]