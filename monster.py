from gameimage import GameImage
import random

class Monster(GameImage):
	def __init__(self, key):
		GameImage.__init__(self)
		self.key = key

	def execute_action(self, screen):
		#TEMP. actually have the monster decide an action and make it do something
		target = self.choose_target(screen.player)
		damage = self.roll_damage(target)
		screen.misc_message = self.battle_name + " attacked " + target.name + " for " + str(damage) + " damage!"
		target.take_damage(damage)

	def choose_target(self, player):
		roll = random.randint(0, len(player.party) - 1)
		return player.party[roll]

	def roll_damage(self, target):
		return self.base_attack_damage #TEMP

	def take_damage(self, damage):
		self.hitpoints[0] = max(0, self.hitpoints[0] - damage)