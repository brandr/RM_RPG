from equipment import * #Equipment, DEFAULT, WEAPON_DATA_MAP, NAME, EQUIP_SLOT, COMPATIBLE_CLASSES, ATTACK_VALUE, ARMOR_VALUE, MAX_MANA_VALUE
from equipmentset import RIGHT_HAND, LEFT_HAND

class Weapon(Equipment):
	def __init__(self, key): #TODO: figure out init
		Equipment.__init__(self)
		self.equip_key = key
		for a in WEAPON_ATTRIBUTES: self.init_attribute(a)

	def init_attribute(self, key):
		data_map = WEAPON_DATA_MAP[self.equip_key]
		init_method = INIT_METHODS[key]
		if key in data_map: value = data_map[key]
		else: value = WEAPON_DATA_MAP[DEFAULT][key]
		init_method(self, value)

	def equippable_in_slot(self, slot):
		if slot == LEFT_HAND and self.dual_wield: return True
		return self.equip_slot == slot

	def equip_tag(self):
		if self.left_equipped: return " [L]"
		return " [E]"
		
	def init_name(self, value):
		self.name = value		

	def init_equip_slot(self, value):
		self.equip_slot = value

	def init_compatible_classes(self, value):
		self.compatible_classes = value

	def init_attack_value(self, value):
		self.attack_value = value

	def init_armor_value(self, value):
		self.armor_value = value

	def init_speed_value(self, value):
		self.speed_value = value

	def init_magic_value(self, value):
		self.magic_value = value

	def init_max_hp_value(self, value):
		self.max_hp_value = value

	def init_max_mana_value(self, value):
		self.max_mana_value = value

	def init_dual_wield(self, value):
		self.dual_wield = value

WEAPON_ATTRIBUTES = [ NAME, EQUIP_SLOT, COMPATIBLE_CLASSES, ARMOR_VALUE, ATTACK_VALUE, SPEED_VALUE, MAGIC_VALUE, MAX_HP_VALUE, MAX_MANA_VALUE, DUAL_WIELD ]
INIT_METHODS = {
	NAME:Weapon.init_name,
	EQUIP_SLOT:Weapon.init_equip_slot,
	COMPATIBLE_CLASSES:Weapon.init_compatible_classes,
	ATTACK_VALUE:Weapon.init_attack_value,
	ARMOR_VALUE:Weapon.init_armor_value,
	SPEED_VALUE:Weapon.init_speed_value,
	MAGIC_VALUE:Weapon.init_magic_value,
	MAX_HP_VALUE:Weapon.init_max_hp_value,
	MAX_MANA_VALUE:Weapon.init_max_mana_value,
	DUAL_WIELD:Weapon.init_dual_wield
}