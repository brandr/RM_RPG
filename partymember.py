from battlescreen import ATTACK, SPELLS, ITEMS, RUN
from equipmentset import EquipmentSet
import random

class PartyMember:
	def __init__(self, key = None, party_map = None, spell_factory = None):
		self.key = key
		self.party_map = party_map
		if not party_map or not key in party_map: return
		data_map = party_map[key]
		self.name = data_map[NAME]
		self.battle_name = self.name
		self.party_class = data_map[PARTY_CLASS]
		hitpoints = data_map[HITPOINTS]
		self.hitpoints = [hitpoints, hitpoints]	#TEMP
		mana = data_map[MANA]
		self.mana = [mana, mana]
		spells = data_map[SPELLS]
		self.spells = []
		for key in spells: self.spells.append(spell_factory.generate_spell(key))
		self.attack_stat = data_map[DAMAGE]
		self.defense = data_map[DEFENSE]
		self.speed = data_map[SPEED]
		self.magic = data_map[MAGIC]
		self.equipment_set = EquipmentSet()
		self.pending_action = None
		self.pending_target = None
		self.pending_spell = None

	def name(self):
		return self.battle_name

	def enqueue_action(self, key, target = None):
		self.pending_action = ACTION_MAP[key]
		self.pending_target = target

	def execute_action(self, screen):
		self.pending_action(self, screen)

	def basic_attack(self, screen):
		#TODO: check to see if the target is already dead
		damage = self.roll_damage(self.pending_target)
		if damage > 0:	screen.misc_message = self.name + " attacked " + self.pending_target.battle_name + " for " + str(damage) + " damage!"
		else: screen.misc_message = self.name + " attacked " + self.pending_target.battle_name + ", but they were unfazed."
		self.pending_target.take_damage(damage)

	def cast_spell(self, screen):
		self.pending_spell.cast(self, screen)

	def roll_damage(self, target):
		base_attack = self.attack_stat + self.equipment_damage()
		offset = max(1, base_attack/5.0)
		damage = max(1, random.randint(round(base_attack - offset), round(base_attack + offset)))
		damage = max(0, damage - target.armor_value())
		return damage

	def equipment_damage(self):
		return self.equipment_set.equipment_damage()

	def take_damage(self, damage):
		self.hitpoints[0] = max(0, self.hitpoints[0] - damage)

	def restore_mana(self, mana):
		self.mana[0] = min(self.mana[1], self.mana[0] + mana)

	def armor_value(self):
		return self.equipment_set.armor_value()

	def lose_mp(self, mp):
		self.mana[0] = max(0, self.mana[0] - mp)

	def has_spells(self):
		return len(self.spells) > 0

	def spell_count(self):
		return len(self.spells)		

ACTION_MAP = {
	ATTACK:PartyMember.basic_attack,
	SPELLS:PartyMember.cast_spell,
	ITEMS:None,
	RUN:None
}		

#attributes
NAME = "name"
PARTY_CLASS = "party_class"
HITPOINTS = "hitpoints"
MANA = "mana"
DAMAGE = "damage"
DEFENSE = "defense"
SPEED = "speed"
MAGIC = "magic"
SPELLS = "spells"