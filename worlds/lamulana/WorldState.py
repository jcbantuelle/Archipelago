from typing import List, Dict, Set, Optional, Callable, Tuple, NamedTuple
from BaseClasses import MultiWorld, CollectionState
from .Options import is_option_enabled, get_option_value, starting_location_ids
from .Locations import get_locations_by_region
from .LogicShortcuts import LaMulanaLogicShortcuts

class LaMulanaTransition(NamedTuple):
	region: str
	vanilla_destination: str
	enter_logic: Optional[Callable] = None
	exit_logic: Optional[Callable] = None
	is_oneway: bool = False

class LaMulanaDoor(NamedTuple):
	region: str
	vanilla_destination: str
	vanilla_requirement: str
	is_oneway: bool = False
	is_nonboss: bool = False

class LaMulanaWorldState:
	world: MultiWorld
	player: int
	transition_rando: bool
	include_oneways: bool
	door_rando: bool
	include_nonboss: bool
	transition_map: Optional[Dict[str,str]] = None
	door_map: Optional[Dict[str,Tuple[str,str]]] = None
	npc_rando: bool
	include_dracuet: bool
	npc_mapping: Dict[str,str]
	cursed_chests: Set[str]
	is_surface_start: bool

	def __init__(self, world: MultiWorld, player: int):
		self.world = world
		self.player = player
		self.transition_rando = is_option_enabled(world, player, "RandomizeTransitions")
		self.include_oneways = get_option_value(world, player, "RandomizeTransitions") == 2
		self.door_rando = is_option_enabled(world, player, "RandomizeBacksideDoors")
		self.include_nonboss = get_option_value(world, player, "RandomizeBacksideDoors") == 2
		self.npc_rando = is_option_enabled(world, player, "RandomizeNPCs")
		self.include_dracuet = is_option_enabled(world, player, "RandomizeDracuetsShop")
		self.randomize_cursed_chests = is_option_enabled(world, player, "RandomizeCursedChests")
		self.include_coin_chests = is_option_enabled(world, player, "RandomizeCoinChests")
		self.include_trap_items = is_option_enabled(world, player, "RandomizeTrapItems")
		self.is_surface_start = get_option_value(world, player, "StartingLocation") == starting_location_ids['surface']

		self.set_cursed_chests()
		if self.transition_rando:
			self.randomize_transitions()
		if self.door_rando:
			self.randomize_doors()
		if self.npc_rando:
			self.build_npc_mapping()

	def randomize_transitions(self):
		#BIIIIIG TODO - just implement entrance rando lol
		pass

	def randomize_doors(self):
		#TODO this one shouldn't be as bad
		pass

	def randomize_npcs(self, npc_list: List[str]) -> Dict[str,str]:
		randomized_list = npc_list.copy()
		self.world.random.shuffle(randomized_list)
		return {npc_list[i]: randomized_list[i] for i in range(len(npc_list))}

	def npc_rando_checks_passed(self) -> bool:
		if self.is_surface_start and not (self.npc_mapping['Elder Xelpud'] == 'Elder Xelpud' or self.npc_mapping['Former Mekuri Master'] == 'Elder Xelpud'):
			return False
		for surface_npc in {'Nebur', 'Sidro', 'Modro', 'Moger', 'Hiner'}:
			if self.npc_mapping[surface_npc] == 'Elder Xelpud':
				return False
		if self.npc_mapping['Yiear Kungfu'] == 'Yiegah Kungfu':
			return False
		if 'Tailor Dracuet' in self.npc_mapping and self.npc_mapping['Tailor Dracuet'] in {'Mulbruk', 'Fairy Queen', 'Elder Xelpud'}:
			return False
		return True

	def get_npc_names(self):
		npc_names = ['Elder Xelpud', 'Nebur', 'Sidro', 'Modro', 'Hiner', 'Moger', 'Former Mekuri Master', 'Priest Zarnac', 'Penadvent of Ghost', 'Priest Xanado', 'Greedy Charlie', 'Mulbruk', 'Shalom III', 'Usas VI', 'Kingvalley I', 'Priest Madomo', 'Priest Hidlyda', 'Philosopher Giltoriyo', 'Mr. Fishman (Original)', 'Mr. Fishman (Alt)', 'Priest Gailious', 'Hot-blooded Nemesistwo', 'Priest Romancis', 'Priest Aramo', 'Priest Triton', 'Operator Combaker', 'Yiegah Kungfu', 'Yiear Kungfu', 'Arrogant Sturdy Snake', 'Arrogant Metagear', 'Priest Jaguarfiv', 'Fairy Queen', 'Affected Knimare', 'duplex', 'Mr. Slushfund', 'Priest Alest', 'Mover Athleland', 'Giant Mopiran', 'Giant Thexde', 'Philosopher Alsedana', 'Samieru', 'Kingvalley II', 'Philosopher Samaranta', 'Naramura', 'Energetic Belmont', 'Priest Laydoc', 'Mechanical Efspi', 'Priest Ashgine', 'Mudman Qubert', 'Philosopher Fobos', '8-bit Elder']
		if self.include_dracuet:
			npc_names.append('Tailor Dracuet')
		return npc_names

	def build_npc_mapping(self):
		npc_names = self.get_npc_names()
		self.npc_mapping = self.randomize_npcs(npc_names)
		while not self.npc_rando_checks_passed():
			self.npc_mapping = self.randomize_npcs(npc_names)

	def set_cursed_chests(self):
		if self.randomize_cursed_chests:
			possible_cursed_chests = []
			locations_by_region = get_locations_by_region(self.world, self.player, self)
			for locationlist in locations_by_region.values():
				for location in locationlist:
					if not location.is_event and location.is_cursable:
						possible_cursed_chests.append(location.name)
			curse_count = min(len(possible_cursed_chests), get_option_value(self.world, self.player, 'CursedChestCount'))
			self.cursed_chests = set(self.world.random.sample(possible_cursed_chests, curse_count))
		else:
			#4 vanilla cursed chests
			self.cursed_chests = {'Crystal Skull Chest', 'Dimensional Key Chest', 'Djed Pillar Chest', 'Magatama Jewel Chest'}

	def get_transitions(self):
		s = LaMulanaLogicShortcuts(self.world, self.player)
		transitions = {
			'left': {
				'Guidance L1': 		LaMulanaTransition('Gate of Guidance [Main]', 'Surface R1'),
				'Mausoleum L1': 	LaMulanaTransition('Mausoleum of the Giants', 'Endless R1'),
				'Sun L1': 			LaMulanaTransition('Temple of the Sun [West]', 'Inferno R1', enter_logic = lambda state: state.has('Buer Defeated', self.player)),
				'Graveyard L1': 	LaMulanaTransition('Graveyard of the Giants [West]', 'Ruin R2'),
				'Moonlight L1': 	LaMulanaTransition('Temple of Moonlight [Lower]', 'Pipe R1', enter_logic = lambda state: False, exit_logic = lambda state: state.has('Holy Grail', self.player) or (s.moonlight_face(state) and s.attack_below(state))),
				'Goddess L1':		LaMulanaTransition('Tower of the Goddess [Spaulder]', 'Illusion R1', enter_logic = lambda state: state.has('Plane Model', self.player) and s.state_mobility(state), exit_logic = lambda state: state.has('Holy Grail', self.player) or (state.has('Plane Model', self.player) and s.state_mobility(state))),
				'Goddess L2':		LaMulanaTransition('Tower of the Goddess [Lower]', 'Ruin R1', enter_logic = lambda state: state.has('Plane Model', self.player)),
				'Ruin L1':			LaMulanaTransition('Tower of Ruin [Illusion]', 'Illusion R2', enter_logic = lambda state: False),
				'Extinction L1':	LaMulanaTransition('Chamber of Extinction [Left Main]', 'Sun R1', enter_logic = lambda state: s.state_extinction_light(state), exit_logic = lambda state: s.state_extinction_light(state)),
				'Extinction L2':	LaMulanaTransition('Chamber of Extinction [Map]', 'Sun R2', enter_logic = lambda state: s.state_extinction_light(state), exit_logic = lambda state: s.state_extinction_light(state)),
				'Birth L1':			LaMulanaTransition('Chamber of Birth [Southeast]', 'Birth R1'),
				'Endless L1':		LaMulanaTransition('Endless Corridor [1F]', 'Endless R1', enter_logic = lambda state: state.has('Holy Grail', self.player), is_oneway=True),
				'Retroguidance L1':	LaMulanaTransition('Gate of Time [Guidance]', 'Retrosurface R1'),
				'Pipe L1':			LaMulanaTransition('Tower of the Goddess [Pipe]', 'Graveyard R1')
			},
			'right': {
				'Surface R1':		LaMulanaTransition('Surface [Main]', 'Guidance L1', enter_logic = lambda state: state.has('NPC: Xelpud', self.player) or s.glitch_raindrop(state), exit_logic = lambda state: False),
				'Illusion R1':		LaMulanaTransition('Gate of Illusion [Pot Room]', 'Goddess L1', exit_logic = lambda state: state.has('Illusion Unlocked', self.player)),
				'Illusion R2':		LaMulanaTransition('Gate of Illusion [Ruin]', 'Ruin L1', enter_logic = lambda state: state.has('Illusion Unlocked', self.player) or s.glitch_raindrop(state), exit_logic = lambda state: state.has('Illusion Unlocked', self.player)),
				'Graveyard R1':		LaMulanaTransition('Graveyard of the Giants [Grail]', 'Pipe L1'),
				'Sun R1':			LaMulanaTransition('Temple of the Sun [East]', 'Extinction L1', enter_logic = lambda state: state.has_all({'Flooded Temple of the Sun', 'Origin Seal'}, self.player) and s.state_mobility(state), exit_logic = lambda state: s.glitch_raindrop(state) or (s.glitch_lamp(state) and state.has('Holy Grail', self.player))),
				'Sun R2':			LaMulanaTransition('Temple of the Sun [East]', 'Extinction L2', enter_logic = lambda state: state.has_all({'Flooded Temple of the Sun', 'Origin Seal'}, self.player) or (s.glitch_lamp(state) and state.has('Holy Grail', self.player)), exit_logic = lambda state: s.glitch_raindrop(state)),
				'Inferno R1':		LaMulanaTransition('Inferno Cavern [Main]', 'Sun L1'),
				'Ruin R1':			LaMulanaTransition('Tower of Ruin [Medicine]', 'Goddess L2'),
				'Ruin R2':			LaMulanaTransition('Tower of Ruin [Southeast]', 'Graveyard L1'),
				'Birth R1':			LaMulanaTransition('Chamber of Birth [Skanda]', 'Birth L1', enter_logic = lambda state: state.has('Skanda Defeated', self.player) or s.glitch_raindrop(state), exit_logic = lambda state: state.has('Skanda Defeated', self.player)),
				'Endless R1':		LaMulanaTransition('Endless Corridor [1F]', 'Mausoleum L1'),
				'Retrosurface R1':	LaMulanaTransition('Gate of Time [Surface]', 'Retroguidance L1'),
				'Pipe R1':			LaMulanaTransition('Tower of the Goddess [Pipe]', 'Moonlight L1')
			},
			'up': {
				'Guidance U1':		LaMulanaTransition('Gate of Guidance [Main]', 'Spring D1'),
				'Mausoleum U1':		LaMulanaTransition('Mausoleum of the Giants', 'Guidance D1'),
				'Graveyard U1':		LaMulanaTransition('Graveyard of the Giants [West]', 'Illusion D1', enter_logic = lambda state: s.attack_chest(state), exit_logic = lambda state: state.has('Holy Grail', self.player) or s.attack_chest(state)),
				'Graveyard U2':		LaMulanaTransition('Graveyard of the Giants [East]', 'Goddess D1'),
				'Sun U1':			LaMulanaTransition('Temple of the Sun [Top Entrance]', 'Guidance D2'),
				'Moonlight U1':		LaMulanaTransition('Temple of Moonlight [Eden]', 'Illusion D2'),
				'Moonlight U2':		LaMulanaTransition('Temple of Moonlight [Upper]', 'Twin D2', exit_logic = lambda state: s.glitch_raindrop(state)),
				'Goddess U1':		LaMulanaTransition('Tower of the Goddess [Lamp]', 'Birth D1', enter_logic = lambda state: state.has('Plane Model', self.player), exit_logic = lambda state: state.has('Plane Model', self.player)),
				'Goddess W1':		LaMulanaTransition('Tower of the Goddess [Lamp]', 'Retromausoleum D1', enter_logic = lambda state: False, exit_logic = lambda state: state.has('Holy Grail', self.player), is_oneway=True),
				'Inferno U1':		LaMulanaTransition('Inferno Cavern [Main]', 'Twin D1'),
				'Inferno U2':		LaMulanaTransition('Inferno Cavern [Spikes]', 'Surface D1'),
				'Extinction U1':	LaMulanaTransition('Chamber of Extinction [Main]', 'Shrine D1', enter_logic = lambda state: s.state_extinction_light(state), exit_logic = lambda state: s.state_extinction_light(state)),
				'Extinction U2':	LaMulanaTransition('Chamber of Extinction [Magatama Right]', 'Surface D2', enter_logic = lambda state: s.attack_chest(state) and state.has('Feather', self.player), exit_logic = lambda state: state.has('Holy Grail', self.player) or (s.attack_chest(state) and state.has('Feather', self.player))),
				'Extinction U3':	LaMulanaTransition('Chamber of Extinction [Ankh Upper]', 'Inferno W1', is_oneway=True),
				'Birth U1':			LaMulanaTransition('Chamber of Birth [Northeast]', 'Graveyard D1'),
				'Twin U1':			LaMulanaTransition('Twin Labyrinths [Loop]', 'Mausoleum D1'),
				'Twin U2':			LaMulanaTransition('Twin Labyrinths [Poison 2]', 'Shrine D3', enter_logic = lambda state: state.has('Twin Poison Cleared', self.player), exit_logic = lambda state: state.has_any({'Holy Grail' 'Twin Statue'}, self.player)),
				'Twin U3':			LaMulanaTransition('Twin Labyrinths [Poseidon]', 'Dimensional D1', enter_logic = lambda state: state.has_all({'Crystal Skull', 'Feather'}, self.player), exit_logic = lambda state: state.has('Holy Grail', self.player) or state.has_all({'Crystal Skull', 'Feather'}, self.player), is_oneway=True),
				'Endless U1':		LaMulanaTransition('Endless Corridor [2F]', 'Shrine D2', enter_logic = lambda state: state.has('NPC: Philosopher Giltoriyo', self.player), exit_logic = lambda state: state.has_any({'Holy Grail', 'NPC: Philosopher Giltoriyo'}, self.player)),
				'Shrine U1':		LaMulanaTransition('Shrine of the Mother [Main]', 'Endless D1'),
				'Retromausoleum U1':LaMulanaTransition('Gate of Time [Mausoleum Upper]', 'Retroguidance D1')
			},
			'down': {
				'Surface D1':		LaMulanaTransition('Surface [Ruin Path Lower]', 'Inferno U2'),
				'Surface D2':		LaMulanaTransition('Surface [Ruin Path Upper]', 'Extinction U2'),
				'Guidance D1':		LaMulanaTransition('Gate of Guidance [Main]', 'Mausoleum U1'),
				'Guidance D2':		LaMulanaTransition('Gate of Guidance [Main]', 'Sun U1'),
				'Illusion D1':		LaMulanaTransition('Gate of Illusion [Lower]', 'Graveyard U1', enter_logic = lambda state: state.has('Illusion Unlocked', self.player), exit_logic = lambda state: state.has('Illusion Unlocked', self.player)),
				'Illusion D2':		LaMulanaTransition('Gate of Illusion [Eden]', 'Moonlight U1'),
				'Mausoleum D1':		LaMulanaTransition('Mausoleum of the Giants', 'Twin U1'),
				'Graveyard D1':		LaMulanaTransition('Graveyard of the Giants [East]', 'Birth U1'),
				'Spring D1':		LaMulanaTransition('Spring in the Sky [Main]', 'Guidance U1'),
				'Goddess D1':		LaMulanaTransition('Tower of the Goddess [Grail]', 'Graveyard U2', enter_logic = lambda state: state.has('Plane Model', self.player) or s.glitch_raindrop(state), exit_logic = lambda state: False),
				'Inferno W1':		LaMulanaTransition('Inferno Cavern [Lava]', 'Extinction U3', enter_logic = lambda state: False, exit_logic = lambda state: state.has('Holy Grail', self.player)),
				'Birth D1':			LaMulanaTransition('Chamber of Birth [West Entrance]', 'Goddess U1'),
				'Twin D1':			LaMulanaTransition('Twin Labyrinths [Lower]', 'Inferno U1'),
				'Twin D2':			LaMulanaTransition('Twin Labyrinths [Lower]', 'Moonlight U2'),
				'Endless D1':		LaMulanaTransition('Endless Corridor [5F]', 'Shrine U1', enter_logic = lambda state: state.has('Backbeard & Tai Sui Defeated', self.player), exit_logic = lambda state: state.has('Holy Grail', self.player) or s.glitch_raindrop(state)),
				'Dimensional D1':	LaMulanaTransition('Dimensional Corridor [Lower]', 'Twin U3', enter_logic = lambda state: state.has_all({'Feather', 'Holy Grail'}, self.player), exit_logic = lambda state: s.glitch_raindrop(state), is_oneway=True),
				'Shrine D1':		LaMulanaTransition('Shrine of the Mother [Lower]', 'Extinction U1', exit_logic = lambda state: False),
				'Shrine D2':		LaMulanaTransition('Shrine of the Mother [Seal]', 'Endless U1'),
				'Shrine D3':		LaMulanaTransition('Shrine of the Mother [Map]', 'Twin U2'),
				'Retromausoleum D1':LaMulanaTransition('Gate of Time [Mausoleum Lower]', 'Goddess W1', enter_logic = lambda state: s.attack_below(state) or s.attack_bomb(state) or s.attack_earth_spear(state) or s.attack_rolling_shuriken(state) or s.glitch_raindrop(state), exit_logic = lambda state: state.has('Holy Grail', self.player) or s.attack_below(state) or s.attack_bomb(state) or s.attack_earth_spear(state) or s.attack_rolling_shuriken(state) or s.glitch_raindrop(state), is_oneway=True),
				'Retroguidance D1':	LaMulanaTransition('Gate of Time [Guidance]', 'Retromausoleum U1')
			}
		}
		return transitions

	def door_requirement_logic(self, s: LaMulanaLogicShortcuts) -> Dict[str,Optional[Callable[CollectionState,bool]]]:
		door_requirements = {
			'Amphisbaena': lambda state: state.has_all({'Bronze Mirror', 'Amphisbaena Defeated'}, self.player),
			'Sakit': lambda state: state.has_all({'Bronze Mirror', 'Sakit Defeated'}, self.player),
			'Ellmac': lambda state: state.has_all({'Bronze Mirror', 'Ellmac Defeated'}, self.player),
			'Bahamut': lambda state: state.has_all({'Bronze Mirror', 'Bahamut Defeated'}, self.player),
			'Viy': lambda state: state.has_all({'Bronze Mirror', 'Viy Defeated'}, self.player),
			'Palenque': lambda state: state.has_all({'Bronze Mirror', 'Palenque Defeated'}, self.player),
			'Baphomet': lambda state: state.has_all({'Bronze Mirror', 'Baphomet Defeated'}, self.player),
			'Open': None,
			'Key': lambda state: s.state_key_fairy_access(state)
		}
		return door_requirements

	def get_doors(self):
		doors  = {
			'Guidance Door':			LaMulanaDoor('Gate of Guidance [Door]', 'Illusion Door', 'Amphisbaena', is_oneway=True),
			'Mausoleum Door':			LaMulanaDoor('Mausoleum of the Giants', 'Graveyard Door', 'Sakit'),
			'Sun Door':					LaMulanaDoor('Temple of the Sun [Main]', 'Moonlight Door', 'Ellmac'),
			'Inferno Viy Door':			LaMulanaDoor('Inferno Cavern [Viy]', 'Ruin Lower Door', 'Bahamut'),
			'Surface Door':				LaMulanaDoor('Surface [Main]', 'Goddess Door', 'Viy'),
			'Extinction Magatama Door':	LaMulanaDoor('Chamber of Extinction [Magatama Left]', 'Birth Door', 'Palenque'),
			'Inferno Spikes Door':		LaMulanaDoor('Inferno Cavern [Spikes]', 'Ruin Top Door', 'Baphomet'),
			'Illusion Door':			LaMulanaDoor('Gate of Illusion [Grail]', 'Guidance Door', 'Amphisbaena'),
			'Graveyard Door':			LaMulanaDoor('Graveyard of the Giants [West]', 'Mausoleum Door', 'Sakit'),
			'Moonlight Door':			LaMulanaDoor('Temple of Moonlight [Lower]', 'Sun Door', 'Ellmac'),
			'Ruin Lower Door':			LaMulanaDoor('Tower of Ruin [Southwest Door]', 'Inferno Viy Door', 'Bahamut'),
			'Goddess Door':				LaMulanaDoor('Tower of the Goddess [Lower]', 'Surface Door', 'Viy'),
			'Birth Door':				LaMulanaDoor('Chamber of Birth [Northeast]', 'Extinction Magatama Door', 'Palenque'),
			'Ruin Top Door':			LaMulanaDoor('Tower of Ruin [Top]', 'Inferno Spikes Door', 'Baphomet'),
			'Dimensional Door':			LaMulanaDoor('Dimensional Corridor [Grail]', 'Endless One-way Exit', 'Open', is_nonboss=True),
			'Endless One-way Exit':		LaMulanaDoor('Endless Corridor [1F]', 'Dimensional Door', 'Open', is_oneway=True, is_nonboss=True),
			'Extinction Key Door':		LaMulanaDoor('Chamber of Extinction [Main]', 'Retromausoleum Door', 'Key', is_nonboss=True),
			'Retromausoleum Door':		LaMulanaDoor('Gate of Time [Mausoleum Lower]', 'Extinction Key Door', 'Key', is_nonboss=True)
		}
		return doors