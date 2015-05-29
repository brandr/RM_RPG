from item import Item
from equipmentset import HEAD

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

	def unequip(self, target):
		self.equipped = False
		target.equipment_set.equipment[self.equip_slot] = None