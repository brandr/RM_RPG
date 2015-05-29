from gameimage import GameImage
import random
import math

class Monster(GameImage):
	def __init__(self, key):
		GameImage.__init__(self)
		self.key = key

	def name(self):
		return self.battle_name

	def execute_action(self, screen):
		target = self.choose_target(screen.player)
		damage = self.roll_damage(target)
		if damage > 0:	screen.misc_message = self.battle_name + " attacked " + target.name + " for " + str(damage) + " damage!"
		else: screen.misc_message = self.battle_name + " attacked " + target.name + ", but they were unfazed."
		target.take_damage(damage)

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

	def armor_value(self):
		return 0