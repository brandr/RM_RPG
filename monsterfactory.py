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
		else: value = MASTER_MONSTER_MAP[DEFAULT][attribute]
		init_method = INIT_METHOD_MAP[attribute]
		init_method(monster, value)

def init_image(monster, value):
	monster.image = load_image_file("./images", value)
	if IMAGE_TRANSPARENCY in MASTER_MONSTER_MAP[monster.key]: 
		alpha = MASTER_MONSTER_MAP[monster.key][IMAGE_TRANSPARENCY]
		self.image.set_alpha(alpha)

def init_name(monster, value):
	monster.name = value

def init_hitpoints(monster, value):
	monster.hitpoints = [value, value]

def init_damage(monster, value):
	monster.base_attack_damage = value

def init_speed(monster, value):
	monster.speed = value

#monster attributes
IMAGE = "image"
IMAGE_TRANSPARENCY = "image_transparency"
NAME = "name"
HITPOINTS = "hitpoints"
DAMAGE = "damage"
SPEED = "speed"

ATTRIBUTE_LIST = [IMAGE, NAME, HITPOINTS, DAMAGE, SPEED]

INIT_METHOD_MAP = {
	IMAGE:init_image,
	NAME:init_name,
	HITPOINTS:init_hitpoints,
	DAMAGE:init_damage,
	SPEED:init_speed
}

#monster types
DEFAULT = "default"
SPARROW = "sparrow"
GRASS_BEING = "grass_being"
ALPHA_BEETLE = "alpha_beetle"
SPIKE_BADGER = "spike_badger"
SPROUTLING = "sproutling"

MASTER_MONSTER_MAP = {
	DEFAULT:{
		IMAGE:None,
		IMAGE_TRANSPARENCY:255,
		NAME:None,
		HITPOINTS:None,
		DAMAGE:2,
		SPEED:1
	},
	SPARROW:{
		IMAGE:"sparrow_1.bmp",
		NAME:"Sparrow",
		HITPOINTS:12,
		DAMAGE:2,
		SPEED:8
	},
	GRASS_BEING:{
		IMAGE:"grass_being_1.bmp",
		NAME:"Grass Being",
		HITPOINTS:8
	},
	ALPHA_BEETLE:{
		IMAGE:"alpha_beetle_1.bmp",
		NAME:"Alpha Beetle",
		HITPOINTS:5,
		DAMAGE:5,
		SPEED:2
	},
	SPIKE_BADGER:{
		IMAGE:"spike_badger_1.bmp",
		NAME:"Spike Badger",
		HITPOINTS:20,
		DAMAGE:6,
		SPEED:4
	},
	SPROUTLING:{
		IMAGE:"sproutling_1.bmp",
		NAME:"Sproutling",
		HITPOINTS:8,
		DAMAGE:2,
		SPEED:4
	}
}

