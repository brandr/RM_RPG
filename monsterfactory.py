from monster import Monster
from gameimage import load_image_file

MAX_MONSTERS = 6

def generate_monster(key):
	monster = Monster(key)
	init_attributes(monster, key)
	return monster

def init_attributes(monster, key):
	attribute_map = MASTER_MONSTER_MAP[key]
	for attribute in ATTRIBUTE_LIST:
		if attribute in attribute_map: value = attribute_map[attribute]
		else: value = ENEMY_ATTRIBUTE_MAP[DEFAULT][attribute]
		init_method = INIT_METHOD_MAP[attribute]
		init_method(monster, value)

def init_image(monster, value):
	monster.image = load_image_file("./images", value)
	if IMAGE_TRANSPARENCY in MASTER_MONSTER_MAP[monster.key]: 
		alpha = MASTER_MONSTER_MAP[monster.key][IMAGE_TRANSPARENCY]
		self.image.set_alpha(alpha)

def init_hitpoints(monster, value):
	monster.hitpoints = [value, value]

#monster attributes
IMAGE = "image"
IMAGE_TRANSPARENCY = "image_transparency"
HITPOINTS = "hitpoints"


ATTRIBUTE_LIST = [IMAGE, HITPOINTS]

INIT_METHOD_MAP = {
	IMAGE:init_image,
	HITPOINTS:init_hitpoints
}

#monster types
SPARROW = "sparrow"
GRASS_BEING = "grass_being"

MASTER_MONSTER_MAP = {
	SPARROW:{
		IMAGE:"sparrow_1.bmp",
		HITPOINTS:20
	},
	GRASS_BEING:{
		IMAGE:"grass_being_1.bmp",
		HITPOINTS:15
	}
}

