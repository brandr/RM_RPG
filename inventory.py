from armor import Armor
from weapon import Weapon
#from item import Item


class Inventory:
	def __init__(self):
		self.items = [self.create_sword()] #TEMP
		for i in xrange(20):
			self.items.append(Armor("leather_cloak"))

	def item_count(self):
		return len(self.items)

	def items_of_type(self, item_type):
		item_list = []
		for i in self.items: 
			if isinstance(i, item_type): item_list.append(i)
		return item_list

	def create_sword(self):
		return Weapon()

	def add_item(self, item):
		self.items.append(item)