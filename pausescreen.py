from gamescreen import GameScreen, WHITE
from camera import WIN_WIDTH, WIN_HEIGHT
from equipmentset import DEFAULT_EQUIPMENT_NAMES
import pygame
from pygame import Surface, font

MAIN_OPTIONS_WIDTH, MAIN_OPTIONS_HEIGHT = WIN_WIDTH/5, WIN_HEIGHT
MAIN_OPTIONS_X, MAIN_OPTIONS_Y = 4*WIN_WIDTH/5, 0
EQUIPMENT_WIDTH, EQUIPMENT_HEIGHT = WIN_WIDTH/5, WIN_HEIGHT
EQUIPMENT_X, EQUIPMENT_Y = 3*WIN_WIDTH/5, 0
EQUIPMENT_LABEL_WIDTH, EQUIPMENT_LABEL_HEIGHT = EQUIPMENT_WIDTH, 36
EQUIPMENT_PARTY_WIDTH, EQUIPMENT_PARTY_HEIGHT = EQUIPMENT_WIDTH, 160
EQUIPMENT_PARTY_X, EQUIPMENT_PARTY_Y = 0, EQUIPMENT_LABEL_HEIGHT
EQUIPMENT_SLOT_WIDTH, EQUIPMENT_SLOT_HEIGHT = EQUIPMENT_WIDTH, WIN_HEIGHT - EQUIPMENT_LABEL_HEIGHT - EQUIPMENT_PARTY_HEIGHT
EQUIPMENT_SLOT_X, EQUIPMENT_SLOT_Y = EQUIPMENT_X, EQUIPMENT_LABEL_HEIGHT + EQUIPMENT_PARTY_HEIGHT
EQUIPMENT_ITEM_WIDTH, EQUIPMENT_ITEM_HEIGHT = WIN_WIDTH/5, WIN_HEIGHT
EQUIPMENT_ITEM_X, EQUIPMENT_ITEM_Y = 2*WIN_WIDTH/5, 0

class PauseScreen(GameScreen):
	def __init__(self, control_manager, player):
		GameScreen.__init__(self, control_manager)
		self.width, self.height = WIN_WIDTH, WIN_HEIGHT
		self.bg = Surface((WIN_WIDTH, WIN_HEIGHT))
		self.player = player
		self.ui_font = font.Font("./fonts/FreeSansBold.ttf", 16)
		self.main_options_index = 0
		self.equipment_party_index = 0
		self.equipment_slot_index = 0
		self.mode = MAIN

	def update(self):
		""" mgs.update( ) -> None

		Call update methods related to the game.
		"""
		self.screen_image.blit(self.bg, (0, 0))
		self.draw_border(self.screen_image)
		self.draw_panes(self.screen_image)

	def draw_panes(self, pane):
		pane_data = PAUSE_SCREEN_MASTER_MAP[self.mode][OPEN_PANES]
		for d in pane_data:
			if DRAW_METHOD in PAUSE_SCREEN_MASTER_MAP[d]:
				draw_method = PAUSE_SCREEN_MASTER_MAP[d][DRAW_METHOD]
				draw_method(self, pane)
				continue
			dimensions, coordinates = PAUSE_SCREEN_MASTER_MAP[d][DIMENSIONS], PAUSE_SCREEN_MASTER_MAP[d][COORDINATES]
			width, height, x, y = dimensions[0], dimensions[1], coordinates[0], coordinates[1]
			p = Surface((width, height))
			self.draw_border(p)
			self.draw_pane_names(p, d)
			index_method = PAUSE_SCREEN_MASTER_MAP[d][INDEX_METHOD]
			index = index_method(self)
			self.draw_pane_pointer(p, index, self.mode == d)
			pane.blit(p, (x, y))

	def draw_pane_names(self, pane, key, offset = (0, 0) ):
		names = []
		data_map = PAUSE_SCREEN_MASTER_MAP[key][COMPONENTS]
		for d in data_map: names.append(data_map[d][NAME])
		for i in xrange(len(names)): 
			n = names[i]
			text_image = self.ui_font.render(n, True, WHITE)
			pane.blit(text_image, (28, 8 + 40*i))

	def draw_pane_pointer(self, pane, index, filled = True):
		pointer = self.right_pointer(WHITE, filled)
		pane.blit(pointer, (4, 8 + 40*index))

	def right_pointer(self, color = WHITE, filled = True):
		pointer = Surface((16, 16))
		if filled: pygame.draw.polygon(pointer, color, [(0, 0), (16, 8), (0, 16)])
		else: pygame.draw.polygon(pointer, WHITE, [(0, 0), (16, 8), (0, 16)], 2)
		return pointer

	def draw_player_party(self, pane):
		names = []
		for p in self.player.party: names.append(p.name)
		for i in xrange(len(names)):
			n = names [i]
			text_image = self.ui_font.render(n, True, WHITE)
			pane.blit(text_image, (28, 8 + 40*i))

	# equipment draw methods
	def draw_equipment(self, pane):
		equip_pane = Surface((EQUIPMENT_WIDTH, EQUIPMENT_HEIGHT))
		self.draw_border(equip_pane)
		self.draw_equipment_label(equip_pane)
		party_pane = Surface((EQUIPMENT_PARTY_WIDTH, EQUIPMENT_PARTY_HEIGHT))
		self.draw_border(party_pane)
		self.draw_player_party(party_pane)
		self.draw_pane_pointer(party_pane, self.equipment_party_index, self.mode == EQUIPMENT)
		equip_pane.blit(party_pane, (EQUIPMENT_PARTY_X, EQUIPMENT_PARTY_Y))
		pane.blit(equip_pane, (EQUIPMENT_X, EQUIPMENT_Y))

		#TODO: actually show equipment

	def draw_equipment_label(self, pane):
		equipment_label = Surface((EQUIPMENT_LABEL_WIDTH, EQUIPMENT_LABEL_HEIGHT))
		self.draw_border(equipment_label)
		label_image = self.ui_font.render("Equipment", True, WHITE)
		equipment_label.blit(label_image, (8, 8))
		pane.blit(equipment_label, (0, 0))

	# equipment slot draw methods
	def draw_equipment_slot(self, pane):
		equip_slot_pane = Surface((EQUIPMENT_SLOT_WIDTH, EQUIPMENT_SLOT_HEIGHT))
		self.draw_border(equip_slot_pane)
		names = []
		for e in DEFAULT_EQUIPMENT_NAMES: 
			names.append(e)
			#TODO: add the actual equipped item here too
		for i in xrange(len(names)):
			n = names[i]
			text_image = self.ui_font.render(n, True, WHITE)
			equip_slot_pane.blit(text_image, (28, 8 + 40*i))
		self.draw_pane_pointer(equip_slot_pane, self.equipment_slot_index, self.mode == EQUIPMENT_SLOT)
		pane.blit(equip_slot_pane, (EQUIPMENT_SLOT_X, EQUIPMENT_SLOT_Y))

	# equipment item draw methods
	def draw_equipment_item(self, pane):
		equip_item_pane = Surface((EQUIPMENT_ITEM_WIDTH, EQUIPMENT_ITEM_HEIGHT))
		self.draw_border(equip_item_pane)
		#TODO: show valid items, make scrollable with arrow keys
		# only show items in the correct slot that the selected player can equip, and which are not already equipped
		pane.blit(equip_item_pane, (EQUIPMENT_ITEM_X, EQUIPMENT_ITEM_Y))


	# misc
	def unpause(self):
		self.screen_manager.switch_to_world_screen(self.player)

	# screen openers
	def open_inventory_pane(self):
		self.mode = EQUIPMENT

	# cursor movement
	def move_cursor(self, direction):
		data_map = PAUSE_SCREEN_MASTER_MAP[self.mode]
		if MOVE_METHOD not in data_map: return
		move_method = data_map[MOVE_METHOD]
		move_method(self, direction)

	def main_move_method(self, direction):
		count = len(PAUSE_SCREEN_MASTER_MAP[self.mode][COMPONENTS])
		self.main_options_index = (self.main_options_index + direction[1])%count

	def equipment_slot_move(self, direction):
		count = len(DEFAULT_EQUIPMENT_NAMES)
		self.equipment_slot_index = (self.equipment_slot_index + direction[1])%count

	# pressing enter
	def press_enter(self):
		data_map = PAUSE_SCREEN_MASTER_MAP[self.mode]
		if ENTER_METHOD not in data_map: return
		enter_method = data_map[ENTER_METHOD]
		enter_method(self)

	def main_enter_method(self):
		map_list = []
		data_map = PAUSE_SCREEN_MASTER_MAP[MAIN][COMPONENTS]
		for o in data_map: map_list.append(data_map[o])
		option_map = map_list[self.main_options_index]
		open_method = option_map[OPEN_PANE_METHOD]
		open_method(self)

	def equipment_select_party(self):
		self.selected_party_member = self.player.party[self.equipment_party_index]
		self.mode = EQUIPMENT_SLOT

	def equipment_select_slot(self):
		self.mode = EQUIPMENT_ITEM

	# pressing escape
	def press_escape(self):
		data_map = PAUSE_SCREEN_MASTER_MAP[self.mode]
		if ESCAPE_METHOD not in data_map: return
		escape_method = PAUSE_SCREEN_MASTER_MAP[self.mode][ESCAPE_METHOD]
		escape_method(self)

	def return_to_main_mode(self):
		self.mode = MAIN

	def return_to_equipment_mode(self):
		self.mode = EQUIPMENT

	def return_to_equipment_slot_mode(self):
		self.mode = EQUIPMENT_SLOT

	# index methods
	def get_main_index(self):
		return self.main_options_index

# attributes
NAME = "name"
COMPONENTS = "components"
DIMENSIONS = "dimensions"
COORDINATES = "coordinates"
MOVE_METHOD = "move_method"
ENTER_METHOD = "enter_method"
ESCAPE_METHOD = "escape_method"
INDEX_METHOD = "index_method"
OPEN_PANE_METHOD = "open_pane_method"
OPEN_PANES = "open_panes"
DRAW_METHOD = "draw_method"

# modes/panes
MAIN = "main"
EQUIPMENT = "equipment"
EQUIPMENT_SLOT = "equipment_slot"
EQUIPMENT_ITEM = "equipment_item"

# main options
ITEMS = "items"
EQUIPMENT = "equipment"

PAUSE_SCREEN_MASTER_MAP = {	
	MAIN:{
		COMPONENTS:{
			ITEMS:{
				NAME:"Items",
				OPEN_PANE_METHOD:None
			},
			EQUIPMENT:{
				NAME:"Equipment",
				OPEN_PANE_METHOD:PauseScreen.open_inventory_pane
			}
		},
		DIMENSIONS:(MAIN_OPTIONS_WIDTH, MAIN_OPTIONS_HEIGHT),
		COORDINATES:(MAIN_OPTIONS_X, MAIN_OPTIONS_Y),
		MOVE_METHOD:PauseScreen.main_move_method,
		ENTER_METHOD:PauseScreen.main_enter_method,
		ESCAPE_METHOD:PauseScreen.unpause,
		INDEX_METHOD:PauseScreen.get_main_index,
		OPEN_PANES:[MAIN]
	},
	EQUIPMENT:{
		COMPONENTS:{

		},
		DIMENSIONS:(EQUIPMENT_WIDTH, EQUIPMENT_HEIGHT),
		COORDINATES:(EQUIPMENT_X, EQUIPMENT_Y),
		#TODO

		#TODO
		ENTER_METHOD:PauseScreen.equipment_select_party,
		ESCAPE_METHOD:PauseScreen.return_to_main_mode,
		OPEN_PANES:[MAIN, EQUIPMENT],
		DRAW_METHOD:PauseScreen.draw_equipment
	},
	EQUIPMENT_SLOT:{
		COMPONENTS:{

		},
		DIMENSIONS:(EQUIPMENT_SLOT_WIDTH, EQUIPMENT_SLOT_HEIGHT),
		COORDINATES:(EQUIPMENT_SLOT_X, EQUIPMENT_SLOT_Y),
		#TODO

		#TODO
		MOVE_METHOD:PauseScreen.equipment_slot_move,
		ENTER_METHOD:PauseScreen.equipment_select_slot,
		ESCAPE_METHOD:PauseScreen.return_to_equipment_mode,
		OPEN_PANES:[MAIN, EQUIPMENT, EQUIPMENT_SLOT],
		DRAW_METHOD:PauseScreen.draw_equipment_slot
	},
	EQUIPMENT_ITEM:{
		COMPONENTS:{

		},
		DIMENSIONS:(EQUIPMENT_ITEM_WIDTH, EQUIPMENT_ITEM_HEIGHT),
		COORDINATES:(EQUIPMENT_ITEM_X, EQUIPMENT_ITEM_Y),
		ESCAPE_METHOD:PauseScreen.return_to_equipment_slot_mode,
		OPEN_PANES:[MAIN, EQUIPMENT, EQUIPMENT_SLOT, EQUIPMENT_ITEM],
		DRAW_METHOD:PauseScreen.draw_equipment_item
	}
}