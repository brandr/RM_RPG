from armor import Armor
from weapon import Weapon
#from item import Item


class Inventory:
	def __init__(self):
		self.items = [self.create_sword(), self.create_helmet()] #TEMP

	def item_count(self):
		return len(self.items)

	def create_helmet(self):
		return Armor() #TEMP

	def create_sword(self):
		return Weapon()