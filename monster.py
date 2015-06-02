from gameimage import GameImage
from battleeffect import STUN
import random
import math

class Monster(GameImage):
	def __init__(self, key):
		GameImage.__init__(self)
		self.key = key
		self.active_effects = []

	def name(self):
		return self.battle_name

	def execute_action(self, screen):
		if self.stun_check(screen): return
		target = self.choose_target(screen.player)
		damage = self.roll_damage(target)
		if damage > 0:	screen.misc_message = self.battle_name + " attacked " + target.name + " for " + str(damage) + " damage!"
		else: screen.misc_message = self.battle_name + " attacked " + target.name + ", but they were unfazed."
		target.take_damage(damage)
		#TODO: apply active effects here by having them execute

	def choose_target(self, player):
		active_party = []
		for p in player.party:
			if p.hitpoints[0] > 0: active_party.append(p)
		for s in player.summons:
			if s.hitpoints[0] > 0: active_party.append(s)
		roll = random.randint(0, len(active_party) - 1)
		return active_party[roll]

	def roll_damage(self, target):
		base_attack = self.base_attack_damage
		offset = max(1, base_attack/5.0)
		damage = max(1, random.randint(round(base_attack - offset), round(base_attack + offset)))
		damage = max(0, damage - target.armor_value())
		return damage

	def take_damage(self, damage):
		self.hitpoints[0] = max(0, self.hitpoints[0] - damage)

	def add_effects(self, effects):
		for e in effects: self.active_effects.append(e)

	def armor_value(self):
		return 0

	def stun_check(self, screen):
		for e in self.active_effects:
			if e.key == STUN:
				screen.misc_message = self.battle_name + " cannot move!"
				e.decrement_duration(self)
				return True
		return False