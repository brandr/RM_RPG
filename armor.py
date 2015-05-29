from equipment import Equipment
from equipmentset import RIGHT_HAND, LEFT_HAND, HEAD, TORSO, CLOAK, LEGS, FEET, RING_RIGHT, RING_LEFT

class Armor(Equipment):
	def __init__(self, key): #TODO: figure out init
		Equipment.__init__(self)
		self.equip_key = key
		for a in ARMOR_ATTRIBUTES: self.init_attribute(a)

	def init_attribute(self, key):
		data_map = ARMOR_DATA_MAP[self.equip_key]
		init_method = INIT_METHODS[key]
		if key in data_map: value = data_map[key]
		else: value = ARMOR_DATA_MAP[DEFAULT][key]
		init_method(self,value)
		
	def init_name(self, value):
		self.name = value		

	def init_equip_slot(self, value):
		self.equip_slot = value

	def init_compatible_classes(self, value):
		self.compatible_classes = value

	def init_armor_value(self, value):
		self.armor_value = value

# ATTRIBUTES
NAME = "name"
EQUIP_SLOT = "equip_slot"
COMPATIBLE_CLASSES = "compatible_classes"
ARMOR_VALUE = "armor_value"

ARMOR_ATTRIBUTES = [NAME, EQUIP_SLOT, COMPATIBLE_CLASSES, ARMOR_VALUE]
INIT_METHODS = {
	NAME:Armor.init_name,
	EQUIP_SLOT:Armor.init_equip_slot,
	COMPATIBLE_CLASSES:Armor.init_compatible_classes,
	ARMOR_VALUE:Armor.init_armor_value
}

#party classes
WIZARD = "wizard"
PALADIN = "paladin"
NECROMANCER = "necromancer"
WARRIOR = "warrior"
KNIGHT = "knight"
BEASTMASTER = "beastmaster"
RANGER = "ranger"
DRUID = "druid"
ROGUE = "rogue"

DEFAULT = "default"
#RIGHT HAND
#LEFT HAND
#HEAD
GRASS_HEADBAND = "grass_headband"
ENCHANTED_LEAF_HELMET = "enchanted_leaf_helmet"
#TORSO
#CLOAK
LEATHER_CLOAK = "leather_cloak"
SPIKED_CLOAK = "spiked_cloak"	
#LEGS
#FEET
LEATHER_BOOTS = "leather_boots"
#RING RIGHT
#RING LEFT

ARMOR_DATA_MAP = {
	DEFAULT:{
		NAME:None,
		EQUIP_SLOT:None,
		COMPATIBLE_CLASSES:[WIZARD, PALADIN, NECROMANCER, WARRIOR, KNIGHT, BEASTMASTER, RANGER, DRUID, ROGUE],
		ARMOR_VALUE:0
	},
	#RIGHT HAND
	#LEFT HAND
	#HEAD
	GRASS_HEADBAND:{
		NAME:"Grass Headband",
		EQUIP_SLOT:HEAD,
		COMPATIBLE_CLASSES:[ROGUE, WIZARD, WARRIOR, RANGER, BEASTMASTER],
		ARMOR_VALUE:0
	},
	ENCHANTED_LEAF_HELMET:{
		NAME:"Enchanted Leaf Helmet",
		EQUIP_SLOT:HEAD,
		COMPATIBLE_CLASSES:[RANGER, BEASTMASTER, WARRIOR],
		ARMOR_VALUE:2
	},
	#TORSO
	#CLOAK
	LEATHER_CLOAK:{
		NAME:"Leather Cloak",
		EQUIP_SLOT:CLOAK,
		COMPATIBLE_CLASSES:[WIZARD, BEASTMASTER, RANGER, ROGUE, WARRIOR],
		ARMOR_VALUE:1
	},
	SPIKED_CLOAK:{
		NAME:"Spiked Cloak",
		EQUIP_SLOT:CLOAK,
		COMPATIBLE_CLASSES:[WIZARD, BEASTMASTER, RANGER, ROGUE],
		ARMOR_VALUE:3
	},
	#LEGS
	#FEET
	LEATHER_BOOTS:{
		NAME:"Leather Boots",
		EQUIP_SLOT:FEET,
		ARMOR_VALUE:1
	}
	#RING RIGHT
	#RING LEFT
}