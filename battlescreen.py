from gamescreen import GameScreen, WHITE, BLACK, RED, BLUE, ORANGE
from camera import WIN_WIDTH, WIN_HEIGHT
from battlecontrols import SELECT_ACTION, SELECT_TARGET, SELECT_SPELL, SELECT_ITEM, EXECUTE_ACTIONS
import pygame
from pygame import Surface, Color, font

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

MONSTER_FLOOR_Y = 300

UI_X, UI_Y = 0, WIN_HEIGHT*2/3
PARTY_DATA_X, PARTY_DATA_Y = UI_X, UI_Y
PARTY_DATA_WIDTH, PARTY_DATA_HEIGHT = 300, WIN_HEIGHT - UI_Y
ACTION_OPTIONS_WIDTH, ACTION_OPTIONS_HEIGHT = 110, PARTY_DATA_HEIGHT
MISC_DATA_WIDTH, MISC_DATA_HEIGHT = WIN_WIDTH - PARTY_DATA_WIDTH - ACTION_OPTIONS_WIDTH, PARTY_DATA_HEIGHT

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
		self.assign_monster_letters()
		self.bg = self.generate_bg(tile)
		self.ui_font = font.Font("./fonts/FreeSansBold.ttf", 16)
		self.mode = SELECT_ACTION
		self.action_index = 0
		self.target_index = 0
		self.item_select_index = 0
		self.party_turn_index = 0
		self.pending_action = None
		self.turn_manager = TurnManager(self)
		self.misc_message = None
		self.victory_flag = False

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
		#TODO: generate bg based on tile
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

			hp_text = "HP: " + str(p.hitpoints[0]) + "/" + str(p.hitpoints[1])
			hp_image = self.ui_font.render(hp_text, True, ORANGE)
			data_pane.blit(hp_image, (110, y_offset))

			mp_text = "MP: " + str(p.mana[0]) + "/" + str(p.mana[1])
			mp_image = self.ui_font.render(mp_text, True, BLUE)
			data_pane.blit(mp_image, (220, y_offset))

			y_offset += 40
		pygame.draw.lines(data_pane, WHITE, True, [(0, 0), (PARTY_DATA_WIDTH - 2, 0), (PARTY_DATA_WIDTH - 2, PARTY_DATA_HEIGHT - 2), (0, PARTY_DATA_HEIGHT - 2)], 2)
		pane.blit(data_pane, (0, 0))

	def draw_action_options(self, pane):
		data_pane = Surface((ACTION_OPTIONS_WIDTH, ACTION_OPTIONS_HEIGHT))
		for i in xrange(len(ACTION_OPTION_LIST)):
			text = ACTION_OPTION_LIST[i]
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
		pointer = Surface((16, 16))
		if self.mode == SELECT_ACTION: pygame.draw.polygon(pointer, WHITE, [(0, 0), (16, 8), (0, 16)])
		else: pygame.draw.polygon(pointer, WHITE, [(0, 0), (16, 8), (0, 16)], 2)
		pane.blit(pointer, (4, 8 + 40*self.action_index))

	def draw_item_pointer(self, pane):
		pointer = Surface((16, 16))
		pygame.draw.polygon(pointer, WHITE, [(0, 0), (16, 8), (0, 16)])
		pane.blit(pointer, (4, 8 + 40*self.item_select_index))

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
		if self.party_turn_index >= self.player.party_member_count(): 
			self.begin_executing()
		else:
			self.mode = SELECT_ACTION

	def begin_executing(self):
		self.mode = EXECUTE_ACTIONS
		self.party_turn_index = 0
		self.turn_manager.set_up_queue(self.monsters.monsters, self.player.party)
		self.turn_manager.select_actor(0)

	def select_attack(self):
		self.mode = SELECT_TARGET

	def select_item(self):
		self.mode = SELECT_ITEM

	def target_count(self):
		return len(self.monsters.monsters)

	def item_count(self):
		return self.player.inventory.item_count()

	def exit_battle(self):
		#TODO: calculate experience, gold, item drops, etc. here
		self.screen_manager.switch_to_world_screen(self.player)

TURN_TICKS = 100

class TurnManager:
	def __init__(self, screen):
		self.screen = screen
		self.turn_queue = []
		self.current_actor = None
		self.actor_counter = 0
		self.time_counter = 0

	def set_up_queue(self, monsters, party):
		for m in monsters: self.turn_queue.append((m.speed, m))
		for p in party: self.turn_queue.append((p.speed, p))
		self.turn_queue = sorted(self.turn_queue)
		self.turn_queue.reverse()

	def update(self):
		self.time_counter += 1
		if self.time_counter > TURN_TICKS:
			self.time_counter = 0
			#TODO: check to see if there are any more actors. if there are not but monsters are still alive, the player goes back to choosing actions.
			
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
				self.screen.misc_message = m.battle_name + " was slain!"
				return True
			#TODO: check party member deaths, too
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

	def remove_monster(self, monster):
		self.screen.monsters.monsters.remove(monster)
		self.screen.target_index = 0
		for t in self.turn_queue:
			if t[1] == monster:
				self.turn_queue.remove(t)
				return

ATTACK = "Attack"
SPELLS = "Spells"
ITEMS = "Items"
RUN = "Run"

ACTION_OPTION_LIST = [ATTACK, SPELLS, ITEMS, RUN]
ACTION_OPTION_MAP = {
	ATTACK:BattleScreen.select_attack,
	ITEMS:BattleScreen.select_item
}

MISC_DRAW_MAP = {
	SELECT_TARGET:BattleScreen.misc_draw_select_target,
	EXECUTE_ACTIONS:BattleScreen.misc_draw_message,
	SELECT_ITEM:BattleScreen.misc_draw_select_item
}