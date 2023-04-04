from typing import Dict, Set, Optional
from BaseClasses import MultiWorld
from .Options import is_option_enabled, get_option_value
from .NPCs import get_npc_names
from .Locations import get_locations_by_region

class LaMulanaWorldState:
	world: MultiWorld
	player: int
	transition_rando: bool
	include_oneways: bool
	door_rando: bool
	transition_map: Optional[Dict[str,str]] = None
	door_map: Optional[Dict[str,str]] = None
	door_rando_boss: bool
	door_rando_nonboss: bool
	npc_rando: bool
	include_dracuet: bool
	vanilla_transitions: bool
	npc_mapping: Dict[str,str]
	cursed_chests: Set[str]

	def __init__(self, world: MultiWorld, player: int):
		self.world = world
		self.player = player
		self.transition_rando = is_option_enabled(world, player, "RandomizeTransitions")
		self.include_oneways = get_option_value(world, player, "RandomizeTransitions") == 2
		self.door_rando = is_option_enabled(world, player, "RandomizeBacksideDoors")
		self.npc_rando = is_option_enabled(world, player, "RandomizeNPCs")
		self.include_dracuet = is_option_enabled(world, player, "RandomizeDracuetsShop")
		self.randomize_cursed_chests = is_option_enabled(world, player, "RandomizeCursedChests")
		self.include_coin_chests = is_option_enabled(world, player, "RandomizeCoinChests")
		self.include_trap_items = is_option_enabled(world, player, "RandomizeTrapItems")

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
		for surface_npc in ['Nebur', 'Sidro', 'Modro', 'Moger', 'Hiner']:
			if mapping[surface_npc] == 'Elder Xelpud':
				return False
		if mapping['Yiear Kungfu'] == 'Yiegah Kungfu':
			return False
		if 'Tailor Dracuet' in mapping and mapping['Tailor Dracuet'] in ['Mulbruk', 'Fairy Queen', 'Elder Xelpud']:
			return False
		return True

	def build_npc_mapping(self):
		npc_names = get_npc_names(self.include_dracuet)
		mapping = self.randomize_npcs(npc_names)
		while not self.npc_rando_checks_passed():
			mapping = self.randomize_npcs(npc_names)
		self.npc_mapping = mapping

	def set_cursed_chests(self):
		if self.randomize_cursed_chests:
			possible_cursed_chests = []
			locations_by_region = get_locations_by_region(self.world, self.player, self)
			for locationlist in locations_by_region.values():
				for location in locationlist:
					if not location.is_event and location.is_cursable:
						possible_cursed_chests.append(location.name)
			self.cursed_chests = set(self.world.random.choices(possible_cursed_chests, k=4))
		else:
			#4 vanilla cursed chests
			self.cursed_chests = {'Crystal Skull Chest', 'Dimensional Key Chest', 'Djed Pillar Chest', 'Magatama Jewel Chest'}