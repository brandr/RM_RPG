from item import Item

class Inventory:
	def __init__(self):
		self.items = [Item(), Item(), Item()] #TEMP

	def item_count(self):
		return len(self.items)