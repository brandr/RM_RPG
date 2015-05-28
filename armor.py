from equipment import Equipment
from equipmentset import HEAD

class Armor(Equipment):
	def __init__(self): #TODO: figure out init
		Equipment.__init__(self)
		self.name = "Iron Helmet" #TEMP
		self.equip_slot = HEAD
		self.armor_value = 2 #TEMP
		self.compatible_classes = [] # WIZARD, SOLDIER, etc.

