from item import Item
from equipmentset import HEAD

class Equipment(Item):	# abstract class for weapons and armor to inherit from
	def __init__(self): #TODO: figure out init
		Item.__init__(self)
		self.compatible_classes = [] # WIZARD, SOLDIER, etc.
		self.equipped = False