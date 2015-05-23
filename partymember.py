from battlescreen import ATTACK, SPELLS, ITEMS, RUN
import random

class PartyMember:
	def __init__(self, name, hitpoints, mana = 1, speed = 1):
		self.name = name			#TEMP
		self.hitpoints = [hitpoints, hitpoints]	#TEMP
		self.mana = [mana, mana]
		self.attack_stat = 3
		self.speed = speed
		self.pending_action = None
		self.pending_target = None

	def enqueue_action(self, key, target = None):
		self.pending_action = ACTION_MAP[key]
		self.pending_target = target

	def execute_action(self, screen):
		self.pending_action(self, screen)

	def basic_attack(self, screen):
		#TODO: check to see if the target is already dead
		damage = self.roll_damage(self.pending_target)
		screen.misc_message = self.name + " attacked " + self.pending_target.battle_name + " for " + str(damage) + " damage!"
		self.pending_target.take_damage(damage)

	def roll_damage(self, target):
		base_attack = self.attack_stat #TODO: calculate differently once weapons are added
		offset = max(1, base_attack/5.0)
		return max(1, random.randint(round(base_attack - offset), round(base_attack + offset)))

	def take_damage(self, damage):
		self.hitpoints[0] = max(0, self.hitpoints[0] - damage)

ACTION_MAP = {
	ATTACK:PartyMember.basic_attack,
	SPELLS:None,
	ITEMS:None,
	RUN:None
}		