from equipment import Equipment
from equipmentset import RIGHT_HAND

class Weapon(Equipment):
	def __init__(self): #TODO: figure out init
		Equipment.__init__(self)
		self.name = "Iron Sword" #TEMP
		self.equip_slot = RIGHT_HAND
		self.damage = 2 #TEMP
		self.compatible_classes = [] # WIZARD, SOLDIER, etc.
