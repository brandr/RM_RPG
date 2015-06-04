from battlescreen import ATTACK, SPELLS, ITEMS, RUN
from equipmentset import EquipmentSet
import random

EXP_CAP = 20

class PartyMember:
	def __init__(self, key = None, party_map = None, spell_factory = None):
		self.key = key
		self.party_map = party_map
		if not party_map or not key in party_map: return
		data_map = party_map[key]
		self.spell_factory = spell_factory
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
		self.magic_resist = data_map[MAGIC_RESIST]
		self.speed = data_map[SPEED]
		self.magic = data_map[MAGIC]
		self.equipment_set = EquipmentSet()
		self.level_up_data = data_map[LEVEL_UP_DATA]
		self.experience = [0, EXP_COST_MAP[2]]
		self.exp_level = 1
		self.pending_action = None
		self.pending_target = None
		self.pending_spell = None
		self.new_spells_flag = False
		self.new_spells = []
		self.new_spell_index = 0

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

	def restore_hitpoints(self, hp):
		self.hitpoints[0] = min(self.hitpoints[1], self.hitpoints[0] + hp)

	def restore_mana(self, mana):
		self.mana[0] = min(self.mana[1], self.mana[0] + mana)

	def armor_value(self):
		return self.defense + self.equipment_set.armor_value()

	def magic_resist_value(self):
		return self.magic_resist + self.equipment_set.magic_resist_value()

	def lose_mp(self, mp):
		self.mana[0] = max(0, self.mana[0] - mp)

	def has_spells(self):
		return len(self.spells) > 0

	def spell_count(self):
		return len(self.spells)		

	def new_spells_check(self):
		if self.new_spells:
			if self.new_spell_index < len(self.new_spells): return True		
			return False
		return False

	def new_spells_update(self, screen):
		if not self.new_spells: return
		s = self.spell_factory.generate_spell(self.new_spells[self.new_spell_index])
		screen.misc_message = self.name + " learned " + s.name() + "!"
		self.new_spell_index += 1

	def level_up_check(self):
		if self.experience[0] < self.experience[1]: return False
		while self.experience[0] >= self.experience[1]:
			self.exp_level += 1
			if self.exp_level >= EXP_CAP: self.experience[1] = 999999999
			else: self.experience[1] += EXP_COST_MAP[self.exp_level + 1]
			if not self.exp_level in self.level_up_data: return
			data_map = self.level_up_data[self.exp_level]
			self.hitpoints[1] += data_map[HITPOINTS]
			self.mana[1] += data_map[MANA]
			self.attack_stat += data_map[DAMAGE]
			self.defense += data_map[DEFENSE]
			self.magic_resist += data_map[MAGIC_RESIST]
			self.speed += data_map[SPEED]
			self.magic += data_map[MAGIC]
			if SPELLS in data_map: 
				self.learn_spells(data_map[SPELLS])
				for d in data_map[SPELLS]: self.new_spells.append(d)
			#return True
		return True

	def learn_spells(self, spell_keys):
		for k in spell_keys: self.spells.append(self.spell_factory.generate_spell(k))

	def reset_flags(self):
		self.new_spells = []
		self.new_spells_flag = False
		self.new_spell_index = 0
		self.pending_action = None
		self.pending_target = None
		self.pending_spell = None

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
MAGIC_RESIST = "magic_resist"
SPEED = "speed"
MAGIC = "magic"
SPELLS = "spells"
LEVEL_UP_DATA = "level_up_data"

EXP_COST_MAP = {
	2:20,
	3:30,
	4:45,
	5:60,
	6:75,
	7:90,
	8:100,
	9:120,
	10:180,
	11:200,
	12:230,
	13:250,
	14:280,
	15:300,
	16:350,
	17:450,
	18:600,
	19:800,
	20:1000
}