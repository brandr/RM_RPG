from item import Item
from equipmentset import RIGHT_HAND, LEFT_HAND, HEAD, TORSO, CLOAK, LEGS, FEET, RING_RIGHT, RING_LEFT

class Equipment(Item):	# abstract class for weapons and armor to inherit from
	def __init__(self): #TODO: figure out init
		Item.__init__(self)
		self.compatible_classes = [] # WIZARD, SOLDIER, etc.
		self.equipped = False

	def toggle_equip(self, target):
		if self.equipped: self.unequip(target)
		else: self.equip(target)

	def equip(self, target):
		self.equipped = True
		target.equipment_set.unequip_item_in_slot(self.equip_slot)
		target.equipment_set.equipment[self.equip_slot] = self
		self.apply_equip_effects(target)

	def unequip(self, target):
		self.equipped = False
		target.equipment_set.equipment[self.equip_slot] = None
		self.apply_equip_effects(target, True)

	def apply_equip_effects(self, target, remove = False):
		sign = 1
		if remove: sign = -1
		target.speed += sign*self.speed_value
		target.magic += sign*self.magic_value
		target.mana[1] += sign*self.max_mana_value
		target.hitpoints[1] += sign*self.max_hp_value

# ATTRIBUTES
NAME = "name"
EQUIP_SLOT = "equip_slot"
COMPATIBLE_CLASSES = "compatible_classes"
ARMOR_VALUE = "armor_value"
ATTACK_VALUE = "attack_value"
SPEED_VALUE = "speed_value"
MAGIC_VALUE = "magic_value"
MAX_HP_VALUE = "max_hp_value"
MAX_MANA_VALUE = "max_mana_value"

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
WOODEN_SHORT_SWORD = "wooden_short_sword"
SHEPHERDS_STICK = "shepherds_stick"
RUSTY_DAGGER = "rusty_dagger"
WOODEN_SHORT_BOW = "wooden_short_bow"
SHARP_CHARCOAL = "sharp_charcoal"
CHARRED_STAFF = "charred_staff"
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

WEAPON_DATA_MAP = {
	DEFAULT:{
		NAME:None,
		EQUIP_SLOT:RIGHT_HAND,
		COMPATIBLE_CLASSES:[WIZARD, PALADIN, NECROMANCER, WARRIOR, KNIGHT, BEASTMASTER, RANGER, DRUID, ROGUE],
		ATTACK_VALUE:0,
		ARMOR_VALUE:0,
		SPEED_VALUE:0,
		MAGIC_VALUE:0,
		MAX_HP_VALUE:0,
		MAX_MANA_VALUE:0
	},
	#RIGHT_HAND
	WOODEN_SHORT_SWORD:{
		NAME:"Wooden Short Sword",
		COMPATIBLE_CLASSES:[WARRIOR, KNIGHT, BEASTMASTER, PALADIN],
		ATTACK_VALUE:2
	},
	SHEPHERDS_STICK:{
		NAME:"Shepherd's Stick",
		COMPATIBLE_CLASSES:[WIZARD, BEASTMASTER, NECROMANCER],
		ATTACK_VALUE:1,
		MAX_MANA_VALUE:1
	},
	RUSTY_DAGGER:{
		NAME:"Rusty Dagger",
		COMPATIBLE_CLASSES:[ROGUE, RANGER, NECROMANCER],
		ATTACK_VALUE:2
	},
	WOODEN_SHORT_BOW:{
		NAME:"Wooden Short Bow",
		COMPATIBLE_CLASSES:[RANGER, ROGUE],
		ATTACK_VALUE:2
	},
	SHARP_CHARCOAL:{
		NAME:"Sharp Charcoal",
		COMPATIBLE_CLASSES:[ROGUE, NECROMANCER, BEASTMASTER],
		ATTACK_VALUE:1
	},
	CHARRED_STAFF:{
		NAME:"Charred Staff",
		COMPATIBLE_CLASSES:[WIZARD, NECROMANCER],
		ATTACK_VALUE:1,
		MAGIC_VALUE:5
	}
}

ARMOR_DATA_MAP = {
	DEFAULT:{
		NAME:None,
		EQUIP_SLOT:None,
		COMPATIBLE_CLASSES:[WIZARD, PALADIN, NECROMANCER, WARRIOR, KNIGHT, BEASTMASTER, RANGER, DRUID, ROGUE],
		ATTACK_VALUE:0,
		ARMOR_VALUE:0,
		SPEED_VALUE:0,
		MAGIC_VALUE:0,
		MAX_HP_VALUE:0,
		MAX_MANA_VALUE:0
	},
	#RIGHT HAND
	#LEFT HAND
	#HEAD
	GRASS_HEADBAND:{
		NAME:"Grass Headband",
		EQUIP_SLOT:HEAD,
		COMPATIBLE_CLASSES:[ROGUE, WIZARD, WARRIOR, RANGER, BEASTMASTER],
		ARMOR_VALUE:0,
		SPEED_VALUE:1
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