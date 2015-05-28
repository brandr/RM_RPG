class EquipmentSet:
	def __init__(self):
		self.init_equipment()

	def init_equipment(self):
		self.equipment = {RIGHT_HAND:None, LEFT_HAND:None, HEAD:None, TORSO:None, CLOAK:None, LEGS:None, FEET:None, RING_RIGHT:None, RING_LEFT:None}

	def weapon(self):
		return self.equipment[RIGHT_HAND]

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
DEFAULT_EQUIPMENT_NAMES = ["RH", "LH", "Head", "Torso", "Cloak", "Legs", "Feet", "RingR", "RingL"]