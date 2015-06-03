from monster import Monster
from armor import *
from weapon import *
from equipment import *
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

def init_defense(monster, value):
	monster.defense = value

def init_magic_resist(monster, value):
	monster.magic_resist = value

def init_speed(monster, value):
	monster.speed = value

def init_item_drops(monster, value):
	monster.item_drop_data = value

def init_exp_yield(monster, value):
	monster.exp_yield = value

def init_battle_letter_flag(monster, value):
	monster.battle_letter_flag = value

#monster attributes
IMAGE = "image"
IMAGE_TRANSPARENCY = "image_transparency"
NAME = "name"
HITPOINTS = "hitpoints"
DAMAGE = "damage"
DEFENSE = "defense"
MAGIC_RESIST = "magic_resist"
SPEED = "speed"
ITEM_DROPS = "item_drops"
EXP_YIELD = "exp_yield"
BATTLE_LETTER_FLAG = "battle_letter_flag"

ATTRIBUTE_LIST = [IMAGE, NAME, HITPOINTS, DAMAGE, DEFENSE, MAGIC_RESIST, SPEED, ITEM_DROPS, EXP_YIELD, BATTLE_LETTER_FLAG]

INIT_METHOD_MAP = {
	IMAGE:init_image,
	NAME:init_name,
	HITPOINTS:init_hitpoints,
	DAMAGE:init_damage,
	DEFENSE:init_defense,
	MAGIC_RESIST:init_magic_resist,
	SPEED:init_speed,
	ITEM_DROPS:init_item_drops,
	EXP_YIELD:init_exp_yield,
	BATTLE_LETTER_FLAG:init_battle_letter_flag
}

#monster types
DEFAULT = "default"
SPARROW = "sparrow"
GRASS_BEING = "grass_being"
ALPHA_BEETLE = "alpha_beetle"
BETA_BEETLE = "beta_beetle"
SPIKE_BADGER = "spike_badger"
SPROUTLING = "sproutling"
BONFIRAK = "bonfirak"

#bosses
SVON = "svon"

MASTER_MONSTER_MAP = {
	DEFAULT:{
		IMAGE:None,
		IMAGE_TRANSPARENCY:255,
		NAME:None,
		HITPOINTS:None,
		DAMAGE:2, 
		DEFENSE:0,
		MAGIC_RESIST:0,
		SPEED:1,
		ITEM_DROPS:[],
		EXP_YIELD:0,
		BATTLE_LETTER_FLAG:True
	},
	SPARROW:{
		IMAGE:"sparrow_1.bmp",
		NAME:"Sparrow",
		HITPOINTS:12,
		DAMAGE:2,
		SPEED:8,
		ITEM_DROPS:[(LEATHER_BOOTS, .2), (LEATHER_VEST, .1)],
		EXP_YIELD:5
	},
	GRASS_BEING:{
		IMAGE:"grass_being_1.bmp",
		NAME:"Grass Being",
		HITPOINTS:8,
		ITEM_DROPS:[(GRASS_HEADBAND, .05), (ORB_OF_PLAINS, .01)],
		EXP_YIELD:5
	},
	ALPHA_BEETLE:{
		IMAGE:"alpha_beetle_1.bmp",
		NAME:"Alpha Beetle",
		HITPOINTS:5,
		DAMAGE:5,
		DEFENSE:1,
		SPEED:2,
		EXP_YIELD:20
	},
	BETA_BEETLE:{
		IMAGE:"beta_beetle_1.bmp",
		NAME:"Beta Beetle",
		HITPOINTS:10,
		DAMAGE:10,
		DEFENSE:4,
		SPEED:2,
		EXP_YIELD:80
	},
	SPIKE_BADGER:{
		IMAGE:"spike_badger_1.bmp",
		NAME:"Spike Badger",
		HITPOINTS:20,
		DAMAGE:6,
		DEFENSE:2,
		SPEED:4,
		ITEM_DROPS:[(SPIKED_CLOAK, .1), (SPIKED_STAFF, .05), (BLADE_BOW, .05), (BADGERSPIKE_DAGGER, .1)],
		EXP_YIELD:15
	},
	SPROUTLING:{
		IMAGE:"sproutling_1.bmp",
		NAME:"Sproutling",
		HITPOINTS:8,
		DAMAGE:2,
		SPEED:4,
		ITEM_DROPS:[(ENCHANTED_LEAF_HELMET, .05), (BRANCH_SHIELD, .1), (WOODEN_STAFF, .2)],
		EXP_YIELD:5
	},
	BONFIRAK:{
		IMAGE:"bonfirak_1.bmp",
		NAME:"Bonfirak",
		HITPOINTS:25,
		DAMAGE:5,
		DEFENSE:1,
		SPEED:1,
		ITEM_DROPS:[(SHARP_CHARCOAL, .1), (CHARRED_STAFF, .05), (CHARRED_SHORT_SWORD, .05), (CHARRED_SHIELD, .05)],
		EXP_YIELD:10
	},

	#BOSSES
	SVON:{
		IMAGE:"svon_1.bmp",
		NAME:"Svon the Charred Golem",
		HITPOINTS:50,
		DAMAGE:3,
		SPEED:0,
		ITEM_DROPS:[(CHARRED_STAFF, .1), (CHARRED_SHORT_SWORD, .2), (CHARRED_SHIELD, .2)],
		EXP_YIELD:100,
		BATTLE_LETTER_FLAG:False
	}
}

