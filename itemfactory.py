from armor import *

def generate_item(key):
	constructor = None
	for i in ITEM_TYPE_LIST:
		if key in i[1]: constructor = ITEM_TYPE_MAP[i[0]]
	if not constructor: return None
	return constructor(key)

# Item types
ARMOR = "armor"
WEAPON = "weapon"

# Item list
ALL_ARMOR_LIST = [GRASS_HEADBAND, ENCHANTED_LEAF_HELMET, LEATHER_CLOAK, SPIKED_CLOAK, LEATHER_BOOTS]
ALL_WEAPON_LIST = []
#TODO: other item types

ITEM_TYPE_LIST = [(ARMOR, ALL_ARMOR_LIST), (WEAPON, ALL_WEAPON_LIST)]


ITEM_TYPE_MAP = {
	ARMOR:Armor
}