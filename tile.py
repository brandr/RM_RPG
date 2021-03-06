from gameimage import GameImage, load_image_file
from monsterfactory import *
from monsterparty import MonsterParty
import pygame
from pygame import Rect, Color, Surface
import random

TILE_SIZE = 16
DEFAULT_COLORKEY = Color("#FF00FF")

class Tile(GameImage):
	def __init__(self, x = 0, y = 0, key = DEFAULT):
		GameImage.__init__(self)
		filename = TILE_DATA_MAP[key][IMAGE_FILENAME]
		self.default_image = load_image_file("./images", filename)
		self.default_image.set_colorkey(DEFAULT_COLORKEY)
		self.image = Surface((TILE_SIZE, TILE_SIZE))
		self.image.blit(self.default_image, (0, 0))
		self.x, self.y = x, y
		self.rect = Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
		self.encounter_data = TILE_DATA_MAP[key][ENCOUNTER_DATA]
		self.bg_color = TILE_DATA_MAP[key][BACKGROUND_COLOR]
		self.base_encounter_rate = TILE_DATA_MAP[key][BASE_ENCOUNTER_RATE]
		self.entity = None

	def set_entity(self, entity):
		self.entity = entity
		self.entity.rect = Rect(self.rect.left, self.rect.top, TILE_SIZE, TILE_SIZE)
		self.entity.mask = pygame.mask.from_surface(entity.image)
		self.entity.tile = self
		self.image.blit(self.default_image, (0, 0))
		self.image.blit(entity.image, (0, 0))

	def clear_entity(self):
		self.entity = None
		self.image.blit(self.default_image, (0, 0))

	def roll_monster_party(self):
		first_monster = self.roll_monster()
		monsters = [first_monster]
		roll_goal = .4
		while len(monsters) < MAX_MONSTERS:
			roll = random.random()
			if roll < roll_goal: 
				monsters.append(self.roll_monster())
				roll_goal = roll_goal*.5
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

# tile attributes
IMAGE_FILENAME = "image_filename"
BACKGROUND_COLOR = "background_color"
ENCOUNTER_DATA = "encounter_data"
BASE_ENCOUNTER_RATE = "base_encounter_rate"

# tile types
DEFAULT = "default"
MEADOW_GRASS = "meadow_grass"
FOREST_GRASS = "forest_grass"
CHARRED_GRASS = "charred_grass"
BUG_GRASS = "bug_grass"
DARK_GRASS = "dark_grass"

TILE_DATA_MAP = {
	DEFAULT:{
		IMAGE_FILENAME:None,
		ENCOUNTER_DATA:None
	},
	MEADOW_GRASS:{
		IMAGE_FILENAME:"default_grass_1.bmp",
		BACKGROUND_COLOR:Color("#00BB00"),
		ENCOUNTER_DATA:[(.4, SPARROW), (.5, GRASS_BEING), (.1, ALPHA_BEETLE)],
		BASE_ENCOUNTER_RATE: 1.0
	},
	FOREST_GRASS:{
		IMAGE_FILENAME:"forest_grass_1.bmp",
		BACKGROUND_COLOR:Color("#007700"),
		ENCOUNTER_DATA:[(.3, SPARROW), (.2, SPIKE_BADGER), (.5, SPROUTLING)],
		BASE_ENCOUNTER_RATE: 1.1
	},
	CHARRED_GRASS:{
		IMAGE_FILENAME:"charred_grass_1.bmp",
		BACKGROUND_COLOR:Color("#777777"),
		ENCOUNTER_DATA:[(1, BONFIRAK)],
		BASE_ENCOUNTER_RATE:.9
	},
	BUG_GRASS:{
		IMAGE_FILENAME:"bug_grass_1.bmp",
		BACKGROUND_COLOR:Color("#CFC20E"),
		ENCOUNTER_DATA:[(.9, ALPHA_BEETLE), (.1, BETA_BEETLE)],
		BASE_ENCOUNTER_RATE:2.0
	},
	DARK_GRASS:{
		IMAGE_FILENAME:"dark_grass_1.bmp",
		BACKGROUND_COLOR:Color("#002500"),
		ENCOUNTER_DATA:[(.1, SPROUTLING), (.5, SHADOW_CRAWLER), (.4, SHADOW_TWIN)],
		BASE_ENCOUNTER_RATE:1.6
	}
}