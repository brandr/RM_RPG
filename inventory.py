from armor import Armor
from weapon import Weapon


class Inventory:
	def __init__(self):
		self.items = [Weapon("shepherds_stick")] 

	def item_count(self):
		return len(self.items)

	def items_of_type(self, item_type):
		item_list = []
		for i in self.items: 
			if isinstance(i, item_type): item_list.append(i)
		return item_list

	def add_item(self, item):
		self.items.append(item)