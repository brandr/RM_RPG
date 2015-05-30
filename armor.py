from equipment import *

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

	def init_attack_value(self, value):
		self.attack_value = value

	def init_speed_value(self, value):
		self.speed_value = value

	def init_max_hp_value(self, value):
		self.max_hp_value = value

	def init_max_mana_value(self, value):
		self.max_mana_value = value

	def init_magic_value(self, value):
		self.magic_value = value

ARMOR_ATTRIBUTES = [ NAME, EQUIP_SLOT, COMPATIBLE_CLASSES, ARMOR_VALUE, ATTACK_VALUE, SPEED_VALUE, MAGIC_VALUE, MAX_HP_VALUE, MAX_MANA_VALUE ]
INIT_METHODS = {
	NAME:Armor.init_name,
	EQUIP_SLOT:Armor.init_equip_slot,
	COMPATIBLE_CLASSES:Armor.init_compatible_classes,
	ARMOR_VALUE:Armor.init_armor_value,
	ATTACK_VALUE:Armor.init_attack_value,
	SPEED_VALUE:Armor.init_speed_value,
	MAGIC_VALUE:Armor.init_magic_value,
	MAX_HP_VALUE:Armor.init_max_hp_value,
	MAX_MANA_VALUE:Armor.init_max_mana_value
}