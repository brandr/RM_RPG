from gamescreen import GameScreen, WHITE, BLACK, RED, BLUE, ORANGE, DARK_RED
from camera import WIN_WIDTH, WIN_HEIGHT
from battlecontrols import SELECT_ACTION, SELECT_TARGET, SELECT_SPELL, SELECT_ITEM, EXECUTE_ACTIONS
#from spell import SINGLE, ATTACK
import pygame
from pygame import Surface, Color, font
import math

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

MONSTER_FLOOR_Y = 300

UI_X, UI_Y = 0, WIN_HEIGHT*2/3
PARTY_DATA_X, PARTY_DATA_Y = UI_X, UI_Y
PARTY_DATA_WIDTH, PARTY_DATA_HEIGHT = 300, WIN_HEIGHT - UI_Y
ACTION_OPTIONS_WIDTH, ACTION_OPTIONS_HEIGHT = 110, PARTY_DATA_HEIGHT
MISC_DATA_WIDTH, MISC_DATA_HEIGHT = WIN_WIDTH - PARTY_DATA_WIDTH - ACTION_OPTIONS_WIDTH, PARTY_DATA_HEIGHT
MENU_SPACING_WIDTH, MENU_SPACING_HEIGHT = 110, 40

class BattleScreen(GameScreen):
	""" MainGameScreen( ControlManager, Player ) -> MainGameScreen

	The main game screen is used when the game is not paused and the player is doing
	stuff or a cutscene is playing.

	Attributes:

	player: The player affected by this screen.
	"""
	def __init__(self, control_manager, player, monsters, tile):
		GameScreen.__init__(self, control_manager)
		self.width, self.height = WIN_WIDTH, WIN_HEIGHT
		self.player = player
		self.monsters = monsters
		self.init_active_party()
		self.assign_monster_letters()
		self.bg = self.generate_bg(tile)
		self.ui_font = font.Font("./fonts/FreeSansBold.ttf", 16)
		self.mode = SELECT_ACTION
		self.action_index = 0
		self.target_index = 0
		self.item_select_index = 0
		self.spell_index_x, self.spell_index_y = 0, 0
		self.pending_action = None
		self.turn_manager = TurnManager(self)
		self.misc_message = None
		self.victory_flag = False

	def init_active_party(self):
		self.active_party = []
		for p in self.player.party:
			if p.hitpoints[0] > 0: self.active_party.append(p)
		self.reset_party_turn_index()

	def assign_monster_letters(self):
		alphabet_index = 0
		existing_names = []
		for m in self.monsters.monsters:
			name = m.name + " " + ALPHABET[alphabet_index]
			while (name in existing_names):
				alphabet_index += 1
				name = m.name + " " + ALPHABET[alphabet_index]
			existing_names.append(name)
			m.battle_name = name
			alphabet_index = 0 

	def update(self):
		""" mgs.update( ) -> None

		Call update methods related to the game.
		"""
		self.screen_image.blit(self.bg, (0, 0))
		self.draw_monsters()
		self.draw_ui()
		if self.mode == EXECUTE_ACTIONS: self.execute_update()

	def execute_update(self):
		self.turn_manager.update()

	def generate_bg(self, tile):
		bg = Surface((WIN_WIDTH, WIN_HEIGHT))
		bg.fill(tile.bg_color)
		return bg

	def draw_monsters(self):
		x_offset = 20
		for m in self.monsters.monsters:
			self.screen_image.blit(m.image, (x_offset, MONSTER_FLOOR_Y - m.image.get_height()))
			x_offset += 100
		if self.mode == SELECT_TARGET: self.draw_target_pointer()

	def draw_target_pointer(self):
		target = self.monsters.monsters[self.target_index]
		width, height =  target.image.get_width(), target.image.get_height()
		monster_offset = (20 + 100*self.target_index, height)
		pointer_x, pointer_y = monster_offset[0] + width/2 - 8, MONSTER_FLOOR_Y - height - 20
		pointer = Surface((16, 16))
		pointer.set_colorkey(BLACK)
		pygame.draw.polygon(pointer, RED, [(0, 0), (16, 0), (8, 16)])
		self.screen_image.blit(pointer, (pointer_x, pointer_y))

	def draw_ui(self):
		ui_pane = Surface((WIN_WIDTH, WIN_HEIGHT - UI_Y))
		self.draw_party_data(ui_pane)
		self.draw_action_options(ui_pane)
		self.draw_misc_data(ui_pane)
		self.screen_image.blit(ui_pane, (UI_X, UI_Y))

	def draw_party_data(self, pane):	#TEMP. CHange this if party structure changes.
		data_pane = Surface((PARTY_DATA_WIDTH, PARTY_DATA_HEIGHT))
		y_offset = 8
		for i in xrange(len(self.player.party)):
			p = self.player.party[i]
			name_color = WHITE
			if not self.mode == EXECUTE_ACTIONS and i == self.party_turn_index: name_color = ORANGE
			name = p.name
			name_image = self.ui_font.render(name, True, name_color)
			data_pane.blit(name_image, (8, y_offset))

			if p.hitpoints[0] > 0:
				hp_text = "HP: " + str(p.hitpoints[0]) + "/" + str(p.hitpoints[1])
				hp_image = self.ui_font.render(hp_text, True, ORANGE)
			else:
				hp_text = "DEAD"
				hp_image = self.ui_font.render(hp_text, True, DARK_RED)
			data_pane.blit(hp_image, (110, y_offset))

			mp_text = "MP: " + str(p.mana[0]) + "/" + str(p.mana[1])
			mp_image = self.ui_font.render(mp_text, True, BLUE)
			data_pane.blit(mp_image, (220, y_offset))

			y_offset += 40

		for i in xrange(len(self.player.summons)):
			s = self.player.summons[i]
			name_color = WHITE
			if not self.mode == EXECUTE_ACTIONS and i + len(self.player.party) == self.party_turn_index: name_color = ORANGE
			name = s.name
			name_image = self.ui_font.render(name, True, name_color)
			data_pane.blit(name_image, (8, y_offset))

			if s.hitpoints[0] > 0:
				hp_text = "HP: " + str(s.hitpoints[0]) + "/" + str(s.hitpoints[1])
				hp_image = self.ui_font.render(hp_text, True, ORANGE)
			else:
				hp_text = "DEAD"
				hp_image = self.ui_font.render(hp_text, True, DARK_RED)
			data_pane.blit(hp_image, (110, y_offset))

			mp_text = "MP: " + str(s.mana[0]) + "/" + str(s.mana[1])
			mp_image = self.ui_font.render(mp_text, True, BLUE)
			data_pane.blit(mp_image, (220, y_offset))

			y_offset += 40
		pygame.draw.lines(data_pane, WHITE, True, [(0, 0), (PARTY_DATA_WIDTH - 2, 0), (PARTY_DATA_WIDTH - 2, PARTY_DATA_HEIGHT - 2), (0, PARTY_DATA_HEIGHT - 2)], 2)
		pane.blit(data_pane, (0, 0))

	def draw_action_options(self, pane):
		data_pane = Surface((ACTION_OPTIONS_WIDTH, ACTION_OPTIONS_HEIGHT))
		for i in xrange(len(ACTION_OPTION_LIST)):
			text = ACTION_OPTION_LIST[i].capitalize()
			text_image = self.ui_font.render(text, True, WHITE)
			data_pane.blit(text_image, (28, 8 + 40*i))
		pygame.draw.lines(data_pane, WHITE, True, [(0, 0), (ACTION_OPTIONS_WIDTH - 2, 0), (ACTION_OPTIONS_WIDTH - 2, ACTION_OPTIONS_HEIGHT - 2), (0, ACTION_OPTIONS_HEIGHT - 2)], 2)
		if not self.mode == EXECUTE_ACTIONS: self.draw_action_pointer(data_pane)
		pane.blit(data_pane, (PARTY_DATA_WIDTH, 0))

	def draw_misc_data(self, pane):
		data_pane = Surface((MISC_DATA_WIDTH, MISC_DATA_HEIGHT))
		if self.mode in MISC_DRAW_MAP:
			draw_method = MISC_DRAW_MAP[self.mode]
			draw_method(self, data_pane)
		pygame.draw.lines(data_pane, WHITE, True, [(0, 0), (MISC_DATA_WIDTH - 2, 0), (MISC_DATA_WIDTH - 2, MISC_DATA_HEIGHT - 2), (0, MISC_DATA_HEIGHT - 2)], 2)
		pane.blit(data_pane, (PARTY_DATA_WIDTH + ACTION_OPTIONS_WIDTH, 0))

	def misc_draw_select_target(self, pane):
		target = self.monsters.monsters[self.target_index]
		text = target.battle_name
		text_image = self.ui_font.render(text, True, WHITE)
		pane.blit(text_image, (8, 8))

	def misc_draw_select_spell(self, pane):
		spells = self.active_party_member().spells
		for i in xrange(len(spells)):
			s = spells[i]
			x, y = i%3, i/3
			spell_name_image = self.ui_font.render(s.name(), True, WHITE)
			spell_cost_image = self.ui_font.render(str(s.mp_cost()), True, BLUE)
			pane.blit(spell_name_image, (28 + x*MENU_SPACING_WIDTH, 8 + y*MENU_SPACING_HEIGHT))
			pane.blit(spell_cost_image, (32 + x*MENU_SPACING_WIDTH + spell_name_image.get_width(), 8 + y*MENU_SPACING_HEIGHT))
		self.draw_spell_pointer(pane)

	def misc_draw_message(self, pane):
		text_image = self.ui_font.render(self.misc_message, True, WHITE)
		pane.blit(text_image, (8, 8))	

	def misc_draw_select_item(self, pane):
		items = self.player.inventory.items
		for i in xrange(len(items)):
			item = items[i]
			text_image = self.ui_font.render(item.name, True, WHITE)
			pane.blit(text_image, (28, 8 + 40*i))
		self.draw_item_pointer(pane)

	def draw_action_pointer(self, pane):
		pointer = self.right_pointer(WHITE, self.mode == SELECT_ACTION)
		pane.blit(pointer, (4, 8 + 40*self.action_index))

	def draw_item_pointer(self, pane):
		pointer = self.right_pointer()
		pane.blit(pointer, (4, 8 + 40*self.item_select_index))

	def draw_spell_pointer(self, pane):
		pointer = self.right_pointer()
		pane.blit(pointer, (4 + MENU_SPACING_WIDTH*self.spell_index_x, 8 + MENU_SPACING_HEIGHT*self.spell_index_y))

	def right_pointer(self, color = WHITE, filled = True):
		pointer = Surface((16, 16))
		if filled: pygame.draw.polygon(pointer, color, [(0, 0), (16, 8), (0, 16)])
		else: pygame.draw.polygon(pointer, WHITE, [(0, 0), (16, 8), (0, 16)], 2)
		return pointer

	def pause_update(self):
		""" mgs.pause_update( ) -> None

		Update the game in its paused state.
		"""
		pass

	def clear(self):
		""" mgs.level_update( ) -> None

		Revert the screen's contents to a black rectangle.
		"""
		self.contents = Surface((self.width, self.height))

	def select_current_action(self):
		action_key = ACTION_OPTION_LIST[self.action_index]
		self.pending_action = action_key
		action = ACTION_OPTION_MAP[action_key]
		action(self)

	def confirm_current_action(self):
		self.player.enqueue_action(self.party_turn_index, self.pending_action, self.monsters.monsters[self.target_index])
		self.party_turn_index += 1
		while self.party_turn_index < self.party_member_count() and self.active_party_member().hitpoints[0] <= 0: 
			self.party_turn_index += 1
		if self.party_turn_index >= self.party_member_count(): 
			self.begin_executing()
		else:
			self.mode = SELECT_ACTION

	def select_current_spell(self):
		index = self.spell_index_y*3 + self.spell_index_x
		spell = self.active_party_member().spells[int(index)]
		if spell.mp_cost() > self.active_party_member().mana[0]: return
		self.active_party_member().pending_spell = spell
		spell_type, targeting = spell.spell_type(), spell.targeting()
		if spell_type == ATTACK and targeting == SINGLE:	#TODO: many other cases, such as healing party members
			self.mode = SELECT_TARGET
		else:
			self.confirm_current_action()

	def begin_executing(self):
		self.mode = EXECUTE_ACTIONS
		self.turn_manager.set_up_queue(self.monsters.monsters, self.active_party, self.player.summons)
		self.turn_manager.select_actor(0)

	def reset_party_turn_index(self):
		self.party_turn_index = 0
		while self.party_turn_index < self.party_member_count() and self.active_party_member().hitpoints[0] <= 0: 
			self.party_turn_index += 1

	def select_attack(self):
		self.mode = SELECT_TARGET

	def select_spells(self):
		if self.active_party_member().has_spells(): 
			self.spell_index_x, self.spell_index_y = 0, 0
			self.mode = SELECT_SPELL

	def select_item(self):
		self.mode = SELECT_ITEM

	def party_member_count(self):
		return self.player.party_member_count() + self.player.summon_count()

	def active_party_member(self):	# TODO: allow summons
		count = self.player.party_member_count()
		if self.party_turn_index >= count: return self.player.summons[self.party_turn_index - count]
		return self.player.party[self.party_turn_index]

	def target_count(self):
		return len(self.monsters.monsters)

	def item_count(self):
		return self.player.inventory.item_count()

	def current_spell_cols(self):
		spell_count = self.active_party_member().spell_count()
		if self.spell_index_y == spell_count/3: return spell_count%3
		return 3

	def current_spell_rows(self):
		spell_count = self.active_party_member().spell_count()
		end_cols = spell_count%3
		rows = math.ceil(spell_count/3.0)
		if end_cols != 0 and end_cols <= self.spell_index_x: rows -= 1				
		return rows

	def exit_battle(self):
		#TODO: calculate experience, gold, item drops, etc. here
		self.player.remove_summons()
		self.screen_manager.switch_to_world_screen(self.player)

TURN_TICKS = 100

class TurnManager:
	def __init__(self, screen):
		self.screen = screen
		self.turn_queue = []
		self.current_actor = None
		self.actor_counter = 0
		self.time_counter = 0

	def set_up_queue(self, monsters, party, summons):
		for m in monsters: self.turn_queue.append((m.speed, m))
		for p in party:	self.turn_queue.append((p.speed, p))
		for s in summons: self.turn_queue.append((s.speed, s))
		self.turn_queue = sorted(self.turn_queue)
		self.turn_queue.reverse()

	def update(self):
		self.time_counter += 1
		if self.time_counter > TURN_TICKS:
			self.time_counter = 0
			if self.death_check(): return
			if self.victory_check(): return
			if self.actor_counter + 1 >= len(self.turn_queue): 
				self.finish_executing()
				return
			self.actor_counter += 1
			self.select_actor()
			
	def death_check(self):
		for m in self.screen.monsters.monsters:
			if m.hitpoints[0] <= 0:
				self.remove_monster(m)
				self.screen.misc_message = m.battle_name + " was slain!"	#TODO: add to exp and gold rewards here
				return True
		for p in self.screen.active_party:
			if p.hitpoints[0] <= 0:
				self.screen.misc_message = p.name + " fell in battle!"
				self.set_party_member_dead(p)
				return True
		for s in self.screen.player.summons:
			if s.hitpoints[0] <= 0:
				self.screen.misc_message = s.name + " was destroyed!"
				self.remove_summon(s)
				return True
		return False

	def victory_check(self):
		if len(self.screen.monsters.monsters) == 0:
			self.screen.misc_message = "Victory!"
			if self.screen.victory_flag: self.screen.exit_battle()
			self.screen.victory_flag = True
			return True
		return False

	def select_actor(self, index = None):
		if not index: index = self.actor_counter
		self.current_actor = self.turn_queue[index][1]
		self.time_counter = 0
		self.current_actor.execute_action(self.screen)

	def finish_executing(self):
		self.turn_queue = []
		self.current_actor = None
		self.actor_counter = 0
		self.time_counter = 0
		self.screen.mode = SELECT_ACTION
		self.screen.reset_party_turn_index()

	def remove_monster(self, monster):
		self.screen.monsters.monsters.remove(monster)
		self.screen.target_index = 0
		for t in self.turn_queue:
			if t[1] == monster:
				self.turn_queue.remove(t)
				return

	def set_party_member_dead(self, party_member):
		self.screen.active_party.remove(party_member)
		for p in self.turn_queue:
			if p[1] == party_member:
				self.turn_queue.remove(p)
				return				

	def remove_summon(self, summon):
		self.screen.player.summons.remove(summon)
		for s in self.turn_queue:
			if s[1] == summon:
				self.turn_queue.remove(s)
				return

# spell constants
SINGLE = "single"

ATTACK = "attack"
SPELLS = "spells"
ITEMS = "items"
RUN = "run"

ACTION_OPTION_LIST = [ATTACK, SPELLS, ITEMS, RUN]
ACTION_OPTION_MAP = {
	ATTACK:BattleScreen.select_attack,
	SPELLS:BattleScreen.select_spells,
	ITEMS:BattleScreen.select_item
}

MISC_DRAW_MAP = {
	SELECT_TARGET:BattleScreen.misc_draw_select_target,
	SELECT_SPELL:BattleScreen.misc_draw_select_spell,
	EXECUTE_ACTIONS:BattleScreen.misc_draw_message,
	SELECT_ITEM:BattleScreen.misc_draw_select_item
}