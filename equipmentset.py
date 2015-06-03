class EquipmentSet:
	def __init__(self):
		self.init_equipment()

	def init_equipment(self):
		self.equipment = {RIGHT_HAND:None, LEFT_HAND:None, HEAD:None, TORSO:None, CLOAK:None, LEGS:None, FEET:None, RING_RIGHT:None, RING_LEFT:None}

	def equipment_damage(self):
		value = 0
		for i in self.equipment:
			e = self.equipment[i]
			if e: value += e.attack_value
		return value

	def armor_value(self):
		value = 0
		for i in self.equipment:
			e = self.equipment[i]
			if e: value += e.armor_value
		return value

	def magic_resist_value(self):
		value = 0
		for i in self.equipment:
			e = self.equipment[i]
			if e: value += e.magic_resist
		return value

	def weapon(self):
		return self.equipment[RIGHT_HAND]

	def unequip_item_in_slot(self, slot):
		if not self.equipment[slot]: return
		self.equipment[slot].equipped = False
		self.equipment[slot] = None

RIGHT_HAND = "right_hand"
LEFT_HAND = "left_hand"
HEAD = "head"
TORSO = "torso"
CLOAK = "cloak"
LEGS = "legs"
FEET = "feet"
RING_RIGHT = "ring_right"
RING_LEFT = "ring_left"

DEFAULT_EQUIPMENT_SET = {RIGHT_HAND:None, LEFT_HAND:None, HEAD:None, TORSO:None, CLOAK:None, LEGS:None, FEET:None, RING_RIGHT:None, RING_LEFT:None}
DEFAULT_EQUIPMENT_KEYS = [RIGHT_HAND, LEFT_HAND, HEAD, TORSO, CLOAK, LEGS, FEET, RING_RIGHT, RING_LEFT]
DEFAULT_EQUIPMENT_NAMES = ["RH", "LH", "Head", "Torso", "Cloak", "Legs", "Feet", "RingR", "RingL"]