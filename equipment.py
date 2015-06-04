from item import Item
from equipmentset import RIGHT_HAND, LEFT_HAND, HEAD, TORSO, CLOAK, LEGS, FEET, RING_RIGHT, RING_LEFT

class Equipment(Item):	# abstract class for weapons and armor to inherit from
	def __init__(self): #TODO: figure out init
		Item.__init__(self)
		self.compatible_classes = [] # WIZARD, SOLDIER, etc.
		self.equipped = False
		self.left_equipped = False

	def toggle_equip(self, target, left = False):
		if self.equipped: self.unequip(target)
		else: self.equip(target, left)

	def equip(self, target, left = False):
		self.equipped = True
		self.left_equipped = left
		equip_slot = self.equip_slot
		if left: equip_slot = LEFT_HAND
		target.equipment_set.unequip_item_in_slot(equip_slot)
		target.equipment_set.equipment[equip_slot] = self
		self.apply_equip_effects(target)

	def unequip(self, target):
		#left = self.equip_slot == LEFT_HAND
		self.equipped = False
		self.left_unequipped = False
		#if left: target.equipment_set.equipment[LEFT_HAND] = None
		target.equipment_set.equipment[self.equip_slot] = None
		self.apply_equip_effects(target, True)

	def apply_equip_effects(self, target, remove = False):
		sign = 1
		if remove: sign = -1
		target.speed += sign*self.speed_value
		target.magic += sign*self.magic_value
		target.hitpoints[1] = max(1, target.hitpoints[1] + sign*self.max_hp_value)
		target.hitpoints[0] = min(target.hitpoints[0], target.hitpoints[1])
		target.mana[1] = max(1, target.mana[1] + sign*self.max_mana_value)
		target.mana[0] = min(target.mana[0], target.mana[1])
		
	def equippable_in_slot(self, slot):
		return self.equip_slot == slot

	def equip_tag(self):
		return " [E]"

# ATTRIBUTES
NAME = "name"
EQUIP_SLOT = "equip_slot"
COMPATIBLE_CLASSES = "compatible_classes"
ARMOR_VALUE = "armor_value"
MAGIC_RESIST = "magic_resist"
ATTACK_VALUE = "attack_value"
SPEED_VALUE = "speed_value"
MAGIC_VALUE = "magic_value"
MAX_HP_VALUE = "max_hp_value"
MAX_MANA_VALUE = "max_mana_value"
DUAL_WIELD = "dual_wield"

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
#RIGHT HAND (weapon)
WOODEN_SHORT_SWORD = "wooden_short_sword"
SHEPHERDS_STICK = "shepherds_stick"
RUSTY_DAGGER = "rusty_dagger"
WOODEN_SHORT_BOW = "wooden_short_bow"
SHARP_CHARCOAL = "sharp_charcoal"
CHARRED_STAFF = "charred_staff"
CHARRED_SHORT_SWORD = "charred_short_sword"
SPIKED_STAFF = "spiked_staff"
FIRERIDER = "firerider"
BLADE_BOW = "blade_bow"
BADGERSPIKE_DAGGER = "badgerspike_dagger"
EMBER_STAFF = "ember_staff"
WOODEN_STAFF = "wooden_staff"
DARK_SCEPTER = "dark_scepter"
DARK_REAPER = "dark_reaper"
#LEFT HAND
BRANCH_SHIELD = "branch_shield"
CHARRED_SHIELD = "charred_shield"
ORB_OF_PLAINS = "orb_of_plains"
ORB_OF_SHADOWS = "orb_of_shadows"
#HEAD
GRASS_HEADBAND = "grass_headband"
ENCHANTED_LEAF_HELMET = "enchanted_leaf_helmet"
#TORSO
LEATHER_VEST = "leather_vest"
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
		MAGIC_RESIST:0,
		SPEED_VALUE:0,
		MAGIC_VALUE:0,
		MAX_HP_VALUE:0,
		MAX_MANA_VALUE:0,
		DUAL_WIELD:False
	},
	#RIGHT_HAND
	WOODEN_SHORT_SWORD:{
		NAME:"Wooden Shortsword",
		COMPATIBLE_CLASSES:[WARRIOR, KNIGHT, BEASTMASTER, PALADIN],
		ATTACK_VALUE:2
	},
	SHEPHERDS_STICK:{
		NAME:"Shepherd's Stick",
		COMPATIBLE_CLASSES:[WIZARD, BEASTMASTER, NECROMANCER, DRUID],
		ATTACK_VALUE:1,
		MAX_MANA_VALUE:1
	},
	RUSTY_DAGGER:{
		NAME:"Rusty Dagger",
		COMPATIBLE_CLASSES:[ROGUE, RANGER, NECROMANCER],
		ATTACK_VALUE:2
	},
	WOODEN_SHORT_BOW:{
		NAME:"Wooden Shortbow",
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
	},
	CHARRED_SHORT_SWORD:{
		NAME:"Charred Shortsword",
		COMPATIBLE_CLASSES:[WARRIOR],
		ATTACK_VALUE:6
	},
	SPIKED_STAFF:{
		NAME:"Spiked Staff",
		COMPATIBLE_CLASSES:[WIZARD, NECROMANCER, DRUID],
		ATTACK_VALUE:3,
		MAGIC_VALUE:2
	},
	FIRERIDER:{
		NAME:"Firerider",
		COMPATIBLE_CLASSES:[RANGER],
		ATTACK_VALUE:10,
		MAGIC_VALUE:3,
		ARMOR_VALUE:1,
		SPEED_VALUE:1
	},
	BLADE_BOW:{
		NAME:"Blade Bow",
		COMPATIBLE_CLASSES:[RANGER, WARRIOR, ROGUE, DRUID],
		ATTACK_VALUE:5,
		SPEED_VALUE:1,
		ARMOR_VALUE:1,
		MAGIC_VALUE:1,
		MAX_MANA_VALUE:-2
	},
	BADGERSPIKE_DAGGER:{
		NAME:"Badgerspike Dagger",
		COMPATIBLE_CLASSES:[ROGUE, BEASTMASTER, WARRIOR],
		ATTACK_VALUE:4,
		DUAL_WIELD:True
	},
	EMBER_STAFF:{
		NAME:"Ember Staff",
		COMPATIBLE_CLASSES:[WIZARD, NECROMANCER],
		ATTACK_VALUE:2,
		MAX_MANA_VALUE:-2,
		MAGIC_VALUE:8
	},
	WOODEN_STAFF:{
		NAME:"Wooden Staff",
		COMPATIBLE_CLASSES:[WIZARD, DRUID, NECROMANCER, BEASTMASTER],
		ATTACK_VALUE:2,
		MAX_MANA_VALUE:2
	},
	DARK_SCEPTER:{
		NAME:"Dark Scepter",
		COMPATIBLE_CLASSES:[WIZARD, NECROMANCER],
		ATTACK_VALUE:2,
		MAGIC_VALUE:10,
		MAX_MANA_VALUE:-2,
		MAX_HP_VALUE:-2,
		SPEED_VALUE:1
	},
	DARK_REAPER:{
		NAME:"Dark Reaper",
		COMPATIBLE_CLASSES:[WARRIOR, NECROMANCER],
		ATTACK_VALUE:10,
		MAGIC_VALUE:5,
		MAX_HP_VALUE:-5,
		SPEED_VALUE:2
	}
}

ARMOR_DATA_MAP = {
	DEFAULT:{
		NAME:None,
		EQUIP_SLOT:None,
		COMPATIBLE_CLASSES:[WIZARD, PALADIN, NECROMANCER, WARRIOR, KNIGHT, BEASTMASTER, RANGER, DRUID, ROGUE],
		ATTACK_VALUE:0,
		ARMOR_VALUE:0,
		MAGIC_RESIST:0,
		SPEED_VALUE:0,
		MAGIC_VALUE:0,
		MAX_HP_VALUE:0,
		MAX_MANA_VALUE:0
	},
	#RIGHT HAND
	#LEFT HAND
	BRANCH_SHIELD:{
		NAME:"Branch Shield",
		EQUIP_SLOT:LEFT_HAND,
		COMPATIBLE_CLASSES:[WARRIOR, BEASTMASTER, DRUID],
		ARMOR_VALUE:2
	},
	CHARRED_SHIELD:{
		NAME:"Charred Shield",
		EQUIP_SLOT:LEFT_HAND,
		COMPATIBLE_CLASSES:[WARRIOR, BEASTMASTER],
		ARMOR_VALUE:3,
		SPEED_VALUE:-1,
		MAGIC_RESIST:2
	},
	ORB_OF_PLAINS:{
		NAME:"Orb of Plains",
		EQUIP_SLOT:LEFT_HAND,
		COMPATIBLE_CLASSES:[WIZARD, DRUID],
		MAGIC_VALUE:-1,
		MAGIC_RESIST:-1,
		SPEED_VALUE:1,
		MAX_MANA_VALUE:10
	},
	ORB_OF_SHADOWS:{
		NAME:"Orb of Shadows",
		EQUIP_SLOT:LEFT_HAND,
		COMPATIBLE_CLASSES:[WIZARD, NECROMANCER],
		MAGIC_VALUE:10,
		MAX_HP_VALUE:-10,
		SPEED_VALUE:-1
	},
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
		COMPATIBLE_CLASSES:[RANGER, BEASTMASTER, WARRIOR, DRUID],
		ARMOR_VALUE:2,
		MAGIC_RESIST:3
	},
	#TORSO
	LEATHER_VEST:{
		NAME:"Leather Vest",
		EQUIP_SLOT:TORSO,
		COMPATIBLE_CLASSES:[WARRIOR, KNIGHT, BEASTMASTER],
		ARMOR_VALUE:2,
		MAGIC_VALUE:-1,
		MAX_MANA_VALUE:-1
	},
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